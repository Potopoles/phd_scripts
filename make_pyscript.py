#!/usr/bin/env python
#title           :pyscript.py
#description     :This will create a header for a python script.
#author          :bgw
#date            :20110930
#version         :0.4
#usage           :python pyscript.py
#notes           :
#python_version  :2.6.6  
#==============================================================================

# Import the modules needed to run the script.
from os.path import exists
from time import strftime
import os
import subprocess

python_version = subprocess.run(['python', '--version'], stdout=subprocess.PIPE).stdout.decode('utf-8')
print()
print(python_version)
print()
quit()

title = input("Enter a title for your script: ")
script_number = input("Script number: ")

# Add .py to the end of the script.
short_title = title + '.py'
title = script_number + '_' + title + '.py'

# Convert all letters to lower case.
title = title.lower()
short_title = short_title.lower()

# Remove spaces from the title.
title = title.replace(' ', '_')
short_title = short_title.replace(' ', '_')

# Check to see if the file exists to not overwrite it.
if exists(title):
    print("\nA script with this name already exists.")
    exit(1)

descrpt = input("Enter a description: ")
#name = input("Enter your name: ")
name = 'Christoph Heim'
#ver = input("Enter the version number: ")
ver = '1.00'
div = '======================================='

# Create a file that can be written to.
filename = open(title, 'w')

# Set the date automatically.
date = strftime("%Y%m%d")

# Write the data to the file. 
filename.write('#!/usr/bin/python')
filename.write('\n# -*- coding: utf-8 -*-')
filename.write('\n#title\t\t\t:' + short_title)
filename.write('\n#description\t:' + descrpt)
filename.write('\n#author\t\t\t:' + name)
filename.write('\n#date\t\t\t:' + date)
filename.write('\n#version\t\t:' + ver)
filename.write('\n#usage\t\t\t:' + 'python ' + short_title)
filename.write('\n#notes\t\t\t:')
filename.write('\n#python_version\t:3.7.6')
filename.write('\n#' + div * 2 + '\n')
filename.write('\n')
filename.write('\n')

# Close the file after writing to it.
filename.close()

# Clear the screen. This line of code will not work on Windows.
os.system("clear") 

def select_editor():
    '''Open the file with either the Vim or Emacs editor.'''
    editor = input("Select an number:\n\n1 for Vim.\n2 for Emacs.\n")
    if editor == "1" or editor == "2":
        if editor == "1":
            os.system("vim +12 " + title)
            exit()
        elif editor == "2":
            os.system("emacs +12 " + title)
            exit()
    else:
        os.system("clear")
        print("\nI do not understand your answer.\n")
        print("Press <Ctrl + C> to quit.\n")
        return select_editor()

select_editor()
