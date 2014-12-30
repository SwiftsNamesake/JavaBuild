#
# JavaArgs.py
# Invokes a Java file with the supplied command line arguments
#
# Jonatan H Sundqvist
# December 25 2014
#

# TODO | -
#        -
#
# SPEC | -
#        -


import sys, subprocess


def main():
	
	'''
	Docstring goes here

	'''

	# TODO: Show command line to user
	# TODO: Handle working dir properly
	args = "2.2 3.3 4.4" #input('Arguments: ')
	# subprocess.call('java -classpath')
	print(sys.argv[1])
	subprocess.call(sys.argv[1] + " " + args) # javac arguments supplied as argument to this program


if __name__ == '__main__':
	main()