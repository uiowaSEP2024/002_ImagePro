from weasyprint import HTML, CSS


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


def generate_pdf(file_path):
    # HTML Content
    html_string = """
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
            <p>This is a light version producing empty report.</p>
        </section>

    </body>

    </html>
    """
    # Convert HTML and CSS to PDF
    HTML(string=html_string).write_pdf(file_path, stylesheets=[CSS(string=css_string)])


def generate_report(
    docs_dir: str,
) -> str:
    # Generate the report
    report_path = f"{docs_dir}/report.pdf"
    generate_pdf(
        file_path=report_path,
    )

    return report_path
