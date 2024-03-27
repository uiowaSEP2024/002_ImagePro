import os


def generate_rst_for_specified_module(file_location, module_name, rst_output_location):
    """
    Generates an .rst file for a specified module, using the given module name and output location.

    :param file_location: The file path of the Python module. This is used to ensure the file exists.
    :param module_name: The importable name of the module, as it should be referenced in the documentation.
    :param rst_output_location: The directory path where the .rst file should be created.
    """
    # Check if the specified Python file exists
    if not os.path.isfile(file_location):
        raise FileNotFoundError(
            f"The specified Python file was not found: {file_location}"
        )

    # Create the full path for the .rst file
    rst_filename = os.path.join(rst_output_location, f"{module_name}.rst")

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(rst_filename), exist_ok=True)

    # Get module path to fill in the .rst file content
    rst_content_path = (
        file_location.split("002_ImagePro")[1].replace("/", ".").replace(".py", "")[1:]
    )
    # rst_content_path gets the path to module starting from the root directory, replacing '/' with '.' and removing '.py'

    # Define the content of the .rst file
    rst_content = f"{module_name}\n" + "=" * len(module_name) + "\n\n"
    rst_content += f".. automodule:: {rst_content_path}\n   :members:\n   :undoc-members:\n   :show-inheritance:\n"

    # Write the content to the .rst file
    with open(rst_filename, "w") as rst_file:
        rst_file.write(rst_content)

    print(f"Generated .rst documentation at: {rst_filename}")


# Example usage:
# Assuming this script is run from the project_root/scripts/ directory
# Navigate up one directory to the project root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

file_location = os.path.join(project_root, "sphinx_docs", "rst_autogenerate.py")
module_name = "rst_autogenerate"
rst_output_location = os.path.join(project_root, "sphinx_docs", "source", "sphinx")
generate_rst_for_specified_module(file_location, module_name, rst_output_location)
