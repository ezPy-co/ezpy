#!usr/bin/env python
from subprocess import call
import urllib2
import os
import sys
import re

CACHED_PATHS = {}

def scan(target_name):
    """
    Return the full file path to a file, including file_name.

    If the file is not found, print 'File or directory not found'
    to the console and return None.
    """
    if CACHED_PATHS[target_name]:
        return CACHED_PATHS[target_name]
    else:
        extension = os.path.splitext(target_name)[1]
        if 'Windows' in os.environ.get('OS'):
            # Assumes the drive letter is C
            walker = os.walk('C:/')
        else:
            walker = os.walk('/')
        if extension:
                # Search for a file
            for directory, sub_dir, files in walker:
                for each_file in files:
                    if re.match(target_name, each_file):
                        return directory + target_name
        else:
            # Search for a directory
            for directory, sub_dir, files in walker:
                if re.search("/{}".format(target_name), directory):
                    return directory
        # If the whole directory has been scanned with
        # no result...
        print 'File or directory not found'
        return None


# For choice Install Pip

# Download and run dl 
url = 'https://bootstrap.pypa.io/get-pip.py'
scan_result = None
not_linux = True



if not_linux and url:
    print "Downloading from {}".format(url)
    response = urllib2.urlopen(url)
    

    if not "" or scan_result:
        with open(file_name, 'w') as f:
            f.write(response.read())

        if os.path.splitext(file_name)[1] == '.py':
            call([sys.executable, file_name])
            
        else:
            run_file = './'+file_name
            print "Running file_name"
            call([run_file])

command_line = "sudo,python,get-pip.py".split(',')
print "Executing " + ' '.join(command_line)
call(command_line)

# For choice Install Git

# Download and run dl 
url = 'https://github.com/msysgit/msysgit/releases/download/Git-1.9.5-preview20150319/Git-1.9.5-preview20150319.exe'
scan_result = None
not_linux = True


# Detect OS and change url accordingly...
if 'win' in sys.platform:
    # The url for git will be the url used for the windows exe
    print 'Windows detected'
elif 'darwin' in sys.platform:
    print 'Mac detected'
    url = None
elif 'linux' in sys.platform:
    print 'Linux detected'
    not_linux = False
else:
    print 'WARNING: Failed to determine OS'


if not_linux and url:
    print "Downloading from {}".format(url)
    response = urllib2.urlopen(url)
    

    if not "" or scan_result:
        with open(file_name, 'w') as f:
            f.write(response.read())

        if os.path.splitext(file_name)[1] == '.py':
            call([sys.executable, file_name])
            
            raw_input('Enter anything to continue when finished installing git.')
            
        else:
            run_file = './'+file_name
            print "Running file_name"
            call([run_file])


elif url is None:
    call(['xcode-select', '--install'])
    raw_input('Enter anything to continue when finished installing xcode and git.')
else:
    # This will prompt user for sudo password
    call(['sudo', 'apt-get', 'install', 'git'])

# For choice Pip Install virtualenvwrapper

# Pip install, assuming the exact name of the package as used for 'pip install [package]'
# is given in the args field for a step
call(['pip', 'install', "virtualenvwrapper"])

# Add a key, value pair for a subsequent call([])
key, val = "WORKON_HOME,$HOME/.virtualens".split(',')
os.putenv(key, val)

# Add a key, value pair for a subsequent call([])
key, val = "PROJECT_HOME,$HOME/projects".split(',')
os.putenv(key, val)

command_line = "source /usr/local/bin/virtualenvwrapper.sh".split(',')
print "Executing " + ' '.join(command_line)
call(command_line)

# For choice Pip Install virtualenv

# Pip install, assuming the exact name of the package as used for 'pip install [package]'
# is given in the args field for a step
call(['pip', 'install', "virtualenv"])

# For choice Add Username to prompt

# Edit a profile
profile_name = os.path.expanduser('~/')+'.profile'
print "Adding 'PS1=&#39;\[\e[00;37m\]\u@\h:\w\\$ \[\e[0m\]&#39;' to file at profile_name"
with open(profile_name, 'a') as f:
    f.write("\n"+"PS1=&#39;\[\e[00;37m\]\u@\h:\w\\$ \[\e[0m\]&#39;")
