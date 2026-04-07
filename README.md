# Static-Site-Generator
Static site generator in Python for the corresponding lesson in Boot.dev
This generator converts web pages written in markdown to HTML, allowing a page to be created in markdown but rendered in HTML

## USAGE
*Download and Setup*
Ensure python3 is installed in your client. Once the files are downloaded, use this command to grant run permissions to the main file.
`chmod +x src/main.py`
Once permissions are granted, you can upload whatever website structure you want in .md files into the "content" folder, following the same structure you would for .html files. Images and other static assets (such as .css files) should be put into the "static" folder.

*Run Command*
`python3 src/main.py [destination directory]`
Running the above command will create .html files based on the .md files in the "content" folder, following the same directory patterns.

