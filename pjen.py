import os
import shutil
import sys
import re

class pjen:
	def __init__(self, name=None, path=None):
		"""
		By default, the path will be set to the current working directory, 
		or the path can be specified using the 'path' keyword parameter.

		By default, the name of the project will be set to 'website', 
		or can be specified using the 'name' keyword parameter.
		"""

		#if a path has been supplied use it, or else use the current working directory
		self.path = path if path else os.getcwd()

		#if a name has been supplied append it to the path, or else use the default "/website"
		self.path += ("/" + name) if name else "/website"

	def _create_file_structure(self, overwrite=False):
		"""
		Creates the following file structure:

		website/'name'
		  |-> templates
			  |-> group1
  	      |-> images
		  |-> scss
	      |-> css
	      |-> scripts

	    If overwrite=True then any existing file structe will be overwritten.  
		"""

		#if overwrite=True then remove the existing files
		if overwrite:
			shutil.rmtree(self.path)

		project_folders = (
			"/templates/group1",
			"/images",
			"/scss",
			"/css",
			"/scripts",
        )

		for folder in project_folders:
			os.makedirs(self.path + folder)

		print("Created project in {}".format(self.path))

	def create_project(self):
		"""
		Creates the initial file structure for a project. If a directory already exists
		at the location then it will ask if the user wants to overwrite the existing directory. 
		"""

		#check if a project already exists, if so give option to overwrite
		if os.path.exists(self.path):

			print("A directory already exists at: {}".format(self.path))
			response = raw_input("Do you want to overwrite? (y/n)\n")

			if response == "y" or response == "Y":
				print("Overwriting existing file structure")
				self._create_file_structure(overwrite=True)

			elif response == "n" or response == "N":
				print("Exiting...")
				sys.exit()

			else:
				print("Not a valid input. Exiting...")

		#if there is no existing project then create one.
		else:
			self._create_file_structure()

	def _count_indent(self, string, tab_equiv=4):
		"""
		Returns the number of leading spaces. A tab is counted as 'tab_equiv' spaces.
		"""

		i = 0
		count = 0

		while(string[i] == " " or string[i] == "\t"):

			if string[i] == " ":
				count += 1
			elif string[i] == "\t":
				count += 4

			i += 1

		return count

	def _sanatise_file_list(self, file_list, fname=None):
		"""
		Removes blacklisted files from the input list 'file_list'. In addition, a file with 
		the name 'fname' can also be removed.
		"""

		blacklist = (".DS_Store", fname)

		for item in blacklist:
			try:
				file_list.remove(item)
			except ValueError:
				pass

	def _extract_tag_data(self, f):
		"""
		Extracts the tag data from the file 'f'.

		Returns a dictionary of tag data. The keys are the names of the tags and the values are lists of lines, with empty
		lines removed from the start and end of the lists.

		For example:

		For a file that contains the follwing (note: period/full-stop represents a whitespace character):

			.\n
			.\n
			<div>
			....<p>This is a paragraph</p>
			</div>
			.\n
		

		the dictionary below will be returned:

		{ "html" : ["<div>", "....<p>This is a paragraph</p>", "</div>"] }

		"""

		#dictionary to store data
		tag_data = {}

		#flag to determine the section of the input file
		tag = None

		#iterate through the input file and set the appropriate flag
		for line in f.readlines():

			#look for tags
			match = re.search("\{\{(.*?)\}\}", line)

			#if there is a tag
			if match:

				#extract the tag name
				tag = re.search("(\w)+", match.group(0)).group(0)

				#add an empty string to the dictionary
				tag_data[tag] = ""

			else:

				if tag:
					tag_data[tag] += line

		#split the data for each tag into a list of lines
		for key in tag_data.keys():
			tag_data[key] = [line + "\n" for line in tag_data[key].split("\n")]

			#remove any empty lines from the start and end of the tag data
			i = 0
			while tag_data[key][i].isspace() is True:
				i += 1

			j = -1
			while tag_data[key][j].isspace() is True:
				j -= 1

			if i > 0:
				tag_data[key] = tag_data[key][i:]

			if j<-1:
				tag_data[key] = tag_data[key][:j+1]

		return tag_data

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
						with open(self.path + "/templates/" + group + "/" + f, "r") as template_input:

							#extract the tag data from the template input
							tag_data = self._extract_tag_data(template_input)

							#reset the file pointer as the template can be read many times
							template.seek(0)

							#iterate through the template file
							for line in template.readlines():

								#look for tags
								match = re.search("\{\{(.*?)\}\}", line)

								#if there is a tag
								if match:

									#extract the tag name
									tag = re.search("(\w)+", match.group(0)).group(0)

									#check if there is data to be inserted for this tag
									if tag in tag_data.keys():

										indent = self._count_indent(line)

										for insert_line in tag_data[tag]:

											page.write(" "*indent + insert_line)


								#otherwise copy the template text
								else:
									page.write(line)


if __name__ == "__main__":
	p = pjen()
	#p.create_project()
	p.generate()

