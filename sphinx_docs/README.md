**Sphinx Autodocs README**

**About**
Sphinx Autodocs is a tool that generates documentation for python modules using docstrings inside of those python modules. This tool is useful for generating documentation for python modules that are part of a larger project. The documentation is generated in HTML format and can be viewed in a web browser.
Inside of this folder, the source folder contains rst files that are used to generate the documentation. Each python module documented needs its own rst file.
To format the documentation, the source folder structure mirrors our project structure. Each directory needs its own index file which references the rst files of the modules in that directory.
Sub index files must be referenced in the index file of the parent directory.
The build folder contains the generated documentation in HTML format. The build folder is not included in the repository and is generated when the documentation is built.
**To Run**
1. Install Sphinx
```bash
pip install sphinx
```
2. To generate the build folder, run the following command in the terminal inside of the sphinx_docs folder:

```bash
sphinx-build -b html source/ build/
```
The generated documentation can be viewed by opening the index.html file in the build folder in a web browser or other viewer.
