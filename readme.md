# **pjen** - simple static webpage generator

**pjen** is a simple and lightweight static webpage generator written in Python.

## Usage

To create a project:
```
p = pjen()
p.create_project()
```
This creates the following file structure:
```
website
  |-> templates
	  |-> group1
  |-> images
  |-> scss
  |-> css
  |-> scripts
```
Only the **templates** directory is used by **pjen**, the others are there for your convenience.

Each template needs to be called **template.html** and stored in it's own directory, which can have an arbitary name. The inputs for each template are to be stored in the same directory as the template. The input file name will be the name of the generated page.

If a template directory has the following structure: 
```
blog
  |-> template.html
  |-> article1.html
  |-> article2.html
```

and the generator is run using the following commands:
```
p = pjen()
p.generate()
```

then the files **article1.html** and **article2.html** will be created within the **website** directory.

The **template.html** file is a normal html file but can contain tags of the form:

```
{{ tag_name }}
```
Where the tag names must consist of letters, numbers or underscores only and be unique.

These tags will be replaced with the contents following the matching tags in the input files, with the indentation matched.

TODO:
- [x] Ability to overwrite existing file structure
- [x] Deal with empty lines within template input files
- [x] Specify name of project
- [x] Ability to add multiple of each type/custom tags
