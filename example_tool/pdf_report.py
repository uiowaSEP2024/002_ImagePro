import itk
from scipy.ndimage import label, center_of_mass
from skimage.measure import find_contours
from weasyprint import HTML, CSS
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64


# CSS Content
css_string = """
    @page {
        margin: 0;
    }

    body {
        font-family: Tahoma, sans-serif;
        color: #2C3E50; /* Dark Blue */
        margin: 0;
        padding: 0;
    }

    header {
        text-align: center;
        padding: 30px 0;
        margin: 0;
        width: 100%;
        background: linear-gradient(to bottom, #5CACEE, white); /* Gradient from light blue to white */
    }

    header h1 {
        margin: 0;
        font-size: 32pt;
        color: #2C3E50; /* Dark Blue */
    }

    section {
        padding: 20px 40px;
    }

    h2 {
        font-size: 16pt;
        font-weight: bold;
        margin-bottom: 10px;
    }

    hr {
        border: none;
        border-top: 1px solid #2C3E50; /* Dark Blue */
        margin-top: 10px;
        margin-bottom: 30px;
    }

    p {
        font-size: 12pt; /* Font size 12 for the new content */
    }
    """


def generate_image(im_path, mask_path):
    # 1. Load the nifti MRI images
    axis = 0
    itk_im = itk.imread(im_path, itk.F)
    itk_mask = itk.imread(mask_path, itk.UC)

    # 2. Convert to numpy arrays
    im_arr = itk.array_from_image(itk_im)
    mask_arr = itk.array_from_image(itk_mask)

    # 3. Find the center of the largest blob
    labeled, n_components = label(mask_arr)
    sizes = [np.sum(labeled == i) for i in range(1, n_components + 1)]
    largest_blob_index = np.argmax(sizes) + 1
    center = center_of_mass(labeled == largest_blob_index)

    # 4. Extract 2D slice
    slice_index = int(center[axis])
    im_slice = np.flipud(im_arr[slice_index, :, :])
    mask_slice = np.flipud(mask_arr[slice_index, :, :])

    # 4.5 Flip the images vertically
    im_slice = np.flipud(im_slice)
    mask_slice = np.flipud(mask_slice)

    # 5. Draw red boundary
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.imshow(im_slice, cmap="gray")
    contours = find_contours(mask_slice, 0.5)
    for contour in contours:
        ax.plot(contour[:, 1], contour[:, 0], color="red")
    ax.axis("off")

    # 6. Generate image byte with higher dpi
    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=300)  # Increase dpi for higher resolution
    buf.seek(0)

    # Encode the bytes to base64
    image_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")

    plt.close(fig)

    return image_base64


def generate_pdf(brain_volume, image_base64, file_path):
    # HTML Content
    html_string = f"""
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>NeuroPred Report</title>
    </head>

    <body>
        <header>
            <h1>BrainyBarrier</h1>
        </header>

        <section>
            <h2>Study Description</h2>
            <hr>
            <p>Study Date: XXX</p>
            <p>SubjectID: XXX</p>
        </section>

        <section>
            <h2>Brain Volume Analysis</h2>
            <hr>
            <div style="display: flex; justify-content: space-between;">
                <p>Brain Volume: {brain_volume} cm<sup>3</sup></p>
                <img src="data:image/png;base64,{image_base64}" alt="Brain Analysis Image" style="max-height: 300px;">
            </div>
        </section>

    </body>

    </html>
    """
    # Convert HTML and CSS to PDF
    HTML(string=html_string).write_pdf(file_path, stylesheets=[CSS(string=css_string)])


def compute_brain_volume(mask_path: str) -> float:
    # 1. Load the mask using ITK
    mask_itk = itk.imread(mask_path, itk.UC)

    # 2. Extract the spacing information
    spacing = mask_itk.GetSpacing()

    # 3. Convert the ITK image to a numpy array
    mask_array = itk.array_from_image(mask_itk)

    # 4. Count the number of positive voxels
    num_positive_voxels = mask_array.sum()

    # 5. Compute the volume of a single voxel
    voxel_volume_mm3 = spacing[0] * spacing[1] * spacing[2]

    # Calculate the total volume in mm³ and convert to cm³
    total_volume = num_positive_voxels * voxel_volume_mm3 / 1000.0

    # round to 2 decimal places
    total_volume = round(total_volume, 2)

    return total_volume


def generate_report(
    im_path: str,
    mask_path: str,
    docs_dir: str,
) -> str:
    # 1. Compute the brain volume
    brain_volume = compute_brain_volume(mask_path)

    # 2. Generate the image
    image_base64 = generate_image(im_path, mask_path)

    # 3. Generate the outcome message

    # 4. Generate the report
    report_path = f"{docs_dir}/report.pdf"
    generate_pdf(
        brain_volume=brain_volume,
        image_base64=image_base64,
        file_path=report_path,
    )

    return report_path
