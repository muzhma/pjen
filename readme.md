### pjen - simple static site generator

pjen is a simple and lightweight static site generator written in Python.

## Usage

	p = pjen()
	p.create_project()

This creates the following file structure:
	website
	  |-> templates
		  |-> group1
	  |-> images
	  |-> scss
      |-> css
      |-> scripts

Only the **templates** directory is used by pjen, the others are there for convenience.
