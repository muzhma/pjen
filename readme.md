# **pjen** - simple static webpage generator

**pjen** is a simple and lightweight static webpage generator written in Python.

## Usage

	p = pjen()
	p.create_project()

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

**pjen** works by iterating through each directoy, which can have any name, within the **templates** directory. Each directory needs to have a file called **templates.html**. This file is a normal html file, but can have the following tags:

```
{{ css }}
{{ html }}
{{ scripts }}
```