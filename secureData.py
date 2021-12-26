import os
import json
from datetime import datetime
import pathlib

def main():
    global securePath
    global settings
    global logPath

    thisDirectory = pathlib.Path(__file__).parent.resolve()
    os.chdir(thisDirectory)
    
    # initialize settings file if it doesn't exist
    _settingsFile = open('settings.json', 'r+')
    if(len(_settingsFile.read()) == 0):
        _settingsFile.write('{}')
    _settingsFile.close()

    settings = json.load(open('settings.json'))

    # Determines where data is stored, like `securePath = "/home/raspberry/data"`
    securePath = getItem('path_secureData') or setItem(
        'path_secureData', str(thisDirectory), fileName='settings.json')

    logPath = getItem('path_log') or setItem(
        'path_log', securePath + '/log', fileName='settings.json')
    if not os.path.exists(logPath):
        os.makedirs(logPath)
    if not logPath[-1] == '/':
        logPath += '/'
 
def getItem(*attribute):
    """
    Returns a property in settings.json.
    Usage: get('person', 'name')
    """

    global settings
    _settings = settings

    for index, item in enumerate(attribute):
        if item in _settings:
            _settings = _settings[item]
        else:
            print(f"Warning: {item} not found in {_settings if index > 0 else 'settings.json'}")
            return None

    return _settings

def setItem(*attribute, value=None, fileName='settings.json'):
    """
    Sets a property in settings.json (or some other `fileName`).
    Usage: set('person', 'name', 'Tyler')
    The last argument is the value to set, unless value is specified.
    Returns the value set.
    """

    global settings

    if(not value):
        value = attribute[-1]

    _settings = settings if fileName == 'settings.json' else json.load(open(fileName))

    # iterate through entire JSON object and replace 2nd to last attribute with value

    partition = _settings
    for index, item in enumerate(attribute[:-1]):
        if item not in partition:
            partition[item] = value if index == len(attribute) - 2 else {}
            partition = partition[item]
            print(f"Warning: {item} not found in {partition if index > 0 else fileName}")
        else:
            if(index == len(attribute) -2):
                partition[item] = value
            else:
                partition = partition[item]

    with open(fileName, 'w+') as file:
        json.dump(_settings, file, indent=4)

    return value

def getFileAsArray(item, filePath=""):
    """
    Returns the file as an array
    """

    global logPath
    if(filePath == ""):
        filePath = logPath
    elif(filePath == "notes"):
        filePath = getItem('path_tasks_notes')

        if(not filePath[-1] == '/'):
            filePath += '/'

        # pull from cloud
        try:
            os.system(f"rclone copy {getItem('path_cloud_notes')} {filePath}")
        except Exception as e:
            log(f"Could not pull Notes from cloud: {e}")

    try:
        content = open(filePath + item, "r").read()
        return content.split('\n')
    except Exception as e:
        log(f"Error for getFileAsArray: {e}")
        return ""

def writeFile(fileName, filePath="", content="", append=False):
    """
    Writes a file to the specified path and creates subfolders if necessary
    """

    global logPath
    if(filePath == ""):
        filePath = logPath
    elif(filePath == "notes"):
        _filePath = filePath
        filePath = getItem('path_tasks_notes')

    if not os.path.exists(filePath):
        os.makedirs(filePath)

    with open(filePath + "/" + fileName, 'w+' if not append else 'a+') as file:
        file.write(content)

    # push to cloud
    if(_filePath == "notes"):
        try:
            os.system(f"rclone copy {filePath} {getItem('path_cloud_notes')}")
        except Exception as e:
            log(f"Could not sync Notes to cloud: {e}")

def log(content="", logName="LOG_DAILY", clear=False, filePath=""):
    """
    Appends to a log file, or deletes it if clear is True.
    """

    global logPath
    if(filePath == ""):
        filePath = logPath

    logName = logPath + logName

    if not os.path.exists(filePath):
        os.makedirs(filePath)

    if(clear):
        print(f"Clearing {logName}")
        try:
            os.remove(logName)
        except:
            print(f"Error: {logName} not found")
        return

    content = f"{datetime.now().strftime('%H:%M:%S')}: {content}"

    print(content)

    # create file if it doesn't exist
    logFile = pathlib.Path(logName)
    logFile.touch(exist_ok=True)

    with open(logName, 'a+') as file:
        if(os.path.getsize(logName) > 0 and str(file)[-1] != '\n'):
            content = '\n' + content

        file.write(content)

# Initialize
main()