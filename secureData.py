# ReadMe
# Returns files from my SecureData folder (and other folders as needed)
# Dependencies: rclone

from pathlib import Path
import os
import datetime
import pwd

userDir = pwd.getpwuid( os.getuid() )[ 0 ]

# Change this line to modify where your data is stored
securePath = f"/home/{userDir}/SecureData-Data/"

# don't modify these lines directly! These are just defaults. See ReadMe.md in https://github.com/tylerjwoodfin/RaspberryPi-Tasks
piTasksNotesPath = f"/home/{userDir}/Dropbox/Notes"
piTasksCloudProvider = "Dropbox:"
piTasksCloudProviderPath = "Notes"
directory = __file__

# prepares files for other functions
def __initialize(item, path, action="a+"):
    if(path == "notes"):
        path = piTasksNotesPath
    if("/" in path and not path.endswith("/")):
        path += "/"
    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.exists(path + item):
        f = open(path + item, 'w')
        f.write('')
        f.close()

    if(path == piTasksNotesPath):
        # pull from Dropbox
        os.system(f"rclone copyto {piTasksCloudProvider}{piTasksCloudProviderPath}/{item} {path + item}")
    return open(path + item, action)

# reads the first line of a file
def variable(item, path=securePath):
    f = __initialize(item, path)
    f.seek(0,0)
    try:
        return f.read().rstrip().splitlines()[0]
    except:
        log(f"Error: {item} not found in {path}")
        return ''

# override default notes directory
piTasksNotesPath = variable("PiTasksNotesPath") if len(variable("PiTasksNotesPath")) > 0 else piTasksNotesPath
if(piTasksNotesPath[-1] != "/"):
    piTasksNotesPath += "/"

piTasksCloudProvider = variable("PiTasksCloudProvider") if len(variable("PiTasksCloudProvider")) > 0 else piTasksCloudProvider
if(piTasksCloudProvider[-1] != ":"):
    piTasksCloudProvider += ":"

piTasksCloudProviderPath = variable("PiTasksCloudProviderPath") if len(variable("PiTasksCloudProviderPath")) > 0 else piTasksCloudProviderPath

# returns the file as an array
def array(item, path=securePath):
    f = __initialize(item, path)
    f.seek(0,0)
    array = f.read().rstrip().splitlines()
    if(not array):
        log(f"Error: {item} not found in {path}")

    return array

# returns the file as a string without splitting
def file(item, path=securePath):
    f = __initialize(item, path)
    f.seek(0,0)
    return f.read().rstrip()

# writes a file, replacing the contents entirely
def write(item, content, path=securePath):
    f = __initialize(item, path, "w")
    f.write(content)
    f.close()

    # Push to Dropbox
    if(path == piTasksNotesPath or path == "notes"):
        path = piTasksNotesPath
        os.system(f"rclone copyto {path + item} {piTasksCloudProvider}{piTasksCloudProviderPath}/{item}")

# appends to a file where duplicate lines in 'content' will be removed
def appendUnique(item, content, path=securePath):
    content = file(item, path) + '\n' + content
    if(content[0] == '\n'):
        content = content[1:]
    lines = content.splitlines()
    lines = list(dict.fromkeys(lines))
    content = '\n'.join(lines)
    write(item, content, path)

# appends to a daily Log file, sent and reset at the end of each day
def log(content="", logName="LOG_DAILY", clear=False):
    print(f"{datetime.datetime.now().strftime('%H:%M:%S')}: {content}")
    appendUnique(logName, f"{datetime.datetime.now().strftime('%H:%M:%S')}: {content}")

    if(clear):
        print(f"Clearing {logName}")
        write(logName, "")