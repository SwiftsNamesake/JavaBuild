#
# build.py
# Build script for Java projects
#
# Jonatan H Sundqvist
# December 27 2014
#

# TODO | - Create build system or plugin
#        - High-level API function (generates output directory and config file, compiles and runs the project)

# SPEC | -
#        -

# -- Positive and first negative
# positivity = fst . foldl' (\ (xs, p) x -> (if x >= 0 || p then x:xs else xs, x >= 0 && p) ) ([], True)

import subprocess, os, json #, argparse


template = '''
{{

"dependencies": {dependencies},

// Adjust these variables as necessary
"output":  "{output:<10}// Output directory
"package": "{package:<10}// Package name
"entry":   "{entry:<10}// Class containing main method
	
"arguments": {arguments:<10}// Arguments to main
"prompt":    {prompt:<10}// Prompt user for arguments

}}
'''[1:-1] # Shave off newlines


def compileAndRun(**settings):

	'''
	Compiles and runs a Java project with the specified settings

	Required
	 - Depenendies is a list of directories
	 - Output is the path where the generated class files will be placed
	 - Package is quite simply the name of the package
	 - Entry is the name of the class containing the main method

	Optional
	 - Prompt is a boolean indicating whether the user should be prompted to supply additional command line arguments
	 - Arguments is a list of command line arguments for the main method
	 - Log is a boolean indicating whether build messages should be printed

	'''

	# TODO: Error handling (eg. invalid arguments, javac output)
	# TODO: Handling projects without a package
	# TODO: Omit empty arguments

	if settings.get('log', False):
		def call(command, *args, **kwargs):
			print(*args, **kwargs)
			subprocess.call(command)
	else:
		def call(command, *args, **kwargs):
			subprocess.call(command)

	required = ('dependencies', 'output', 'package', 'entry')
	optional = ('prompt', 'arguments', 'log')

	assert all(key in settings for key in required), 'Unable to compile due to missing settings'

	javac = 'javac -cp "{dependencies}" -d {output} *.java'  		# Structure of javac call
	java  = 'java -cp "{dependencies}" {package}.{entry} {args}' 	# Structure of java call

	dependencies, output, package, entry = (settings[key] for key in required) # Unpack required settings for ease of access
	args = ' '.join(settings.get('arguments', []))

	if settings.get('prompt', False):
		args += input('Arguments: ')

	Compile = javac.format(dependencies=';'.join(dependencies), output=output + ',')
	Invoke  = java.format(dependencies=';'.join(dependencies), package=package + ',', entry=entry + ',', args=args)

	call(Compile, 'Compiling...\n  %s' % Compile) 	# Compile
	call(Invoke, 'Invoking...\n  %s' % Invoke) 		# Run



def stripComments(f):
	
	'''
	Strips C-style comments from a JSON file

	'''

	return '\n'.join(line[:line.index('//') if '//' in line else None] for line in f.readlines()) # sliceable[:None] is equivalent to sliceable[:]



def createJSON(filename='build.json', dependencies=[], output='.', package='?', entry='?', arguments=[], prompt='false'):

	'''
	Generates an empty template for build.json, including comments

	'''

	# TODO: Make this typesafe
	# TODO: Align comments when formatting (...)
	# TODO: Use json.dumps (commentjson)

	contents = template.format(dependencies=dependencies, output=output+'",', package=package+'",', entry=entry+'",', arguments= ('[%s],' % ', '.join(arguments)), prompt=prompt)

	with open(filename, 'w', encoding='utf-8') as out:
		out.write(contents)



def main():
	
	'''
	Docstring goes here

	'''

	createJSON(filename='gen.json')

	with open('build.json', 'r', encoding='utf-8') as f:
		settings = json.loads(stripComments(f), encoding='utf-8')
		compileAndRun(**settings)



if __name__ == '__main__':
	main()