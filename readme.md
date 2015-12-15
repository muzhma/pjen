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

The generator is run using the following commands:
```
p = pjen()
p.generate()
```

When the generator is run, it will create the files **article1.html** and **article2.html** within the **website** directory.

The **template.html** file is a normal html file but can contain any of the following tags:

```
{{ css }}
{{ html }}
{{ scripts }}
```

These tags will be replaced with the contents following the tags in the input files, with the indentation matched.

TODO:
[ ] Deal with empty lines within template input files
[ ] Specify name of project
[ ] Ability to add multiple of each type/custom tags