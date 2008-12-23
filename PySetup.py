#! /usr/bin/env python

# Some of this script is from Pete Shinners pygame2exe script.
# (data copying and pygame icon changing) Special thanks to him!


# import modules
from distutils.core import setup
import sys, os, shutil, pygame
import py2exe


#########################
### Variables to edit ###
#########################

script = "cheeseboys.py"  # Starting .py or .pyw script
dest_file = "cheeseboys"   # Final name of .exe file
dest_folder = "bin" # Final folder for the files
icon_file = "data/images/cheese_icon.ico"  # Icon file. Leave blank for the pygame icon.
extra_data = ["data","docs"]        # Extra data to copy in the final folder
extra_modules = []      # Extra modules to be included in the .exe (leave blank if no extra modules)
dll_excludes = []       # excluded dlls ["w9xpopen.exe", "msvcr71.dll"]

# Stuff to show who made it, etc.
name = "Cheese Boys"
license = "GPL"
author = "Keul"
author_email = "lucafbb@gmail.com"
company = "Keul Software"
version = "0.1.1"
keywords = ['arcade', '2d', 'rpg', 'adventure', 'roleplaying', 'engine', 'humor', 'keul', ]
description = u"A humor arcade and roleplaying game played in a future, post-apocalypse world"

##################################################################
### Below if you edit variables, you could mess up the program ###
##################################################################


# Run the script if no commands are supplied 
if len(sys.argv) == 1:
    sys.argv.append("py2exe")
    sys.argv.append("-q")


# Use the pygame icon if there's no icon designated
if icon_file is '':
    path = os.path.split(pygame.__file__)[0]
    icon_resources = '' + os.path.join(path, 'pygame.ico') 


# Copy extra data files
def installfile(name):
    dst = os.path.join(dest_folder)
    print 'copying', name, '->', dst
    if os.path.isdir(name):
        dst = os.path.join(dst, name)
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        shutil.copytree(name, dst)
    elif os.path.isfile(name):
        shutil.copy(name, dst)
    else:
        print 'Warning, %s not found' % name
        

##############################
### Distutils setup script ###
##############################

# Set some variables for the exe
class Target:
    def __init__(self, **kw):
        self.__dict__.update(kw)
        self.icon_file = icon_file

# Set some more variables for the exe
target = Target(
    script = script,
    icon_resources = [(1, icon_file)],
    dest_base = dest_file,
    company_name=company,
    extra_modules = extra_modules
    )


# Run the setup script!
setup(
    options = {"py2exe": {"compressed": 1,
                          "optimize": 2,
                          "bundle_files": 1,
                          "dll_excludes": dll_excludes,
                          "dist_dir": dest_folder}},
    zipfile = None,
    windows = [target],
    name = name,
    description = description,
    keywords = keywords,
    author = author,
    author_email = author_email,
    version = version,
    license = license,
    )


# install extra data files
print '\n' # Just a space to make it look nicer :)
for d in extra_data:
    installfile(d)

# If everything went okay, this should come up.
print '\n\n\nConversion successful!'
