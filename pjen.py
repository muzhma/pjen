import os

class pjen:
	def __init__(self, path=None):
		"""
		By default, the path will be set to the current working directory, 
		or the path can be specified using the 'path' keyword parameter.
		"""

		if path is None:
			self.path = os.getcwd() 
		else:
			self.path = path

		self.path += "/website"

	def create_project(self):
		"""
		Creates an initial file structure for a project at the specified path. 

		An exception is raised if a project already exists in the desired location.

		Creates the following file structure:

		website
		  |-> templates
			  |-> template_###
  	      |-> images
		  |-> scss
	      |-> css
	      |-> scripts

		"""

		if not os.path.exists(self.path):

			#make the root directory
			os.makedirs(self.path)

			os.makedirs(self.path+"/templates")
			os.makedirs(self.path+"/templates/template_###")			
			os.makedirs(self.path+"/images")
			os.makedirs(self.path+"/scss")
			os.makedirs(self.path+"/css")
			os.makedirs(self.path+"/scripts")

			print("Created project in {}".format(self.path))

		else:
			raise IOError("A directory already exists at: {}".format(self.path))


	def _count_indent(self, str, tab_equiv=4):
		"""
		Returns the number of leading spaces. A tab is counted as 'tab_equiv' spaces.
		"""

		i = 0
		count = 0

		while(str[i] == " " or str[i] == "\t"):

			if str[i] == " ":
				count += 1
			if str[i] == "\t":
				count += 4

			i += 1

		return count

	def _sanatise_file_list(self, l, fname=None):
		"""
		Removes blacklisted files from the input list 'l'. In addition, a file with 
		the name 'fname' can also be removed.
		"""

		blacklist = [".DS_Store"]

		if fname:
			blacklist.append(fname)

		for item in blacklist:
			try:
				l.pop(l.index(item))
			except ValueError:
				pass

	def generate(self):
		"""
		Iterates through all the directories in the 'templates' directory, inserting all the 
		inputs into each template. 
		"""

		#get a list of template groups
		static_groups = os.listdir(self.path+"/templates")
		self._sanatise_file_list(static_groups)

		print("Found {} group(s)".format(len(static_groups)))

		#iterate through each of the template groups
		for group in static_groups:

			#get each of the files in the group
			files = os.listdir(self.path+"/templates/"+group)
			
			#remove the template and hidden file
			self._sanatise_file_list(files, "template.html")

			#open the template 
			with open(self.path+"/templates/" + group + "/template.html", "r") as template:

				#iterate though the files that need to be generated
				for f in files:

					#create a new static page
					with open(self.path + "/" + f, "w") as page:

						print("Generating file: {}".format(f))

						#open up the input
						with open(self.path + "/templates/" + group + "/" + f, "r") as my_input:

							#iterate through the input and extract the various sections
							css = ""
							html = ""
							scripts = ""

							#flag to determine the section of the input file
							in_section = None

							#iterate through the input file and set the appropriate flag
							for line in my_input.readlines():
								if line.lstrip().startswith("{{ css }}"):
									in_section = "css"
								elif line.lstrip().startswith("{{ html }}"):
									in_section = "html"
								elif line.lstrip().startswith("{{ scripts }}"):
									in_section = "scripts"
								else:
									if in_section == "css":
										css += line
									if in_section == "html":
										html += line
									if in_section == "scripts":
										scripts += line


							#reset the file pointer as the template can be read many times
							template.seek(0)

							#iterate through the template file
							for line in template.readlines():

								if line.lstrip().startswith("{{ css }}"):

									indent = self._count_indent(line)

									#if there is css in the input file then insert it
									if css != "":

										for insert_line in [x + "\n" for x in css.split("\n")]:

											page.write(" "*indent + insert_line)

								#if there is html in the input file then insert it
								elif line.lstrip().startswith("{{ html }}"):

									indent = self._count_indent(line)

									if html != "":

										for insert_line in [x + "\n" for x in html.split("\n")]:

											page.write(" "*indent + insert_line)

								#if there are script links in the input file then insert them
								elif line.lstrip().startswith("{{ scripts }}"):

									indent = self._count_indent(line)

									if scripts != "":

										for insert_line in [x + "\n" for x in scripts.split("\n")]:

											page.write(" "*indent + insert_line)

								#otherwise copy the template text
								else:
									page.write(line)


if __name__ == "__main__":
	p = pjen()
	p.generate()

