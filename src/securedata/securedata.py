import os
from sys import argv, exit
import json
from datetime import datetime
import pathlib

initialized = False

def main():
    global securePath
    global settings
    global logPath
    global configPath
    global initialized
    settings = None

    if initialized:
        return

    # Determines where data is stored; by default, this is ~/securedata
    securePath = getItem('path_secureData') or f'{os.path.expanduser("~")}/securedata'

    # config file, stored within the package
    configPath = f'{pathlib.Path(__file__).resolve().parent}/config.json'

    # initialize settings file if it doesn't exist
    try:
        with open(f'{securePath}/settings.json', 'r+') as f:
            f.seek(0, os.SEEK_END)
    except:
        if not os.path.exists(securePath):
            os.makedirs(securePath)
        with open(f'{securePath}/settings.json', 'x+') as f:
            print(f"\n\nWarning: settings.json not found; created a blank one in {securePath}")
            print("You can change this location by calling 'securedata config'.\n\n")
            f.write('{}')

    settings = json.load(open(f'{securePath}/settings.json'))

    logPath = getItem('path_log') or setItem(
        'path_log', f"{securePath}/log", fileName='settings.json')
    if not os.path.exists(logPath):
        os.makedirs(logPath)
    if not logPath[-1] == '/':
        logPath += '/'

    initialized = True


def getItem(*attribute):
    """
    Returns a property in settings.json.
    Usage: get('person', 'name')
    """

    global settings
    if settings == None:
        return None

    _settings = settings

    for index, item in enumerate(attribute):
        if item in _settings:
            _settings = _settings[item]
        else:
            print(
                f"Warning: {item} not found in {_settings if index > 0 else f'{securePath}/settings.json'}")
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
    secureFullPath = f"{securePath}/{fileName}"

    if(not value):
        value = attribute[-1]

    _settings = settings if fileName == 'settings.json' else json.load(
        open(secureFullPath))

    # iterate through entire JSON object and replace 2nd to last attribute with value

    partition = _settings
    for index, item in enumerate(attribute[:-1]):
        if item not in partition:
            partition[item] = value if index == len(attribute) - 2 else {}
            partition = partition[item]
            print(
                f"Warning: Adding new key '{item}' to {partition if index > 0 else secureFullPath}")
        else:
            if(index == len(attribute) - 2):
                partition[item] = value
            else:
                partition = partition[item]

    with open(secureFullPath, 'w+') as file:
        json.dump(_settings, file, indent=4)

    return value


def getFileAsArray(item, filePath=None):
    """
    Returns the file as an array
    """

    global logPath
    if(filePath == None):
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


def writeFile(fileName, filePath=None, content=None, append=False):
    """
    Writes a file to the specified path and creates subfolders if necessary
    """

    global logPath
    if filePath == None:
        filePath = logPath
    elif filePath == "notes":
        _filePath = filePath
        filePath = getItem('path_tasks_notes')

    if content == None:
        content = ""

    if not os.path.exists(filePath):
        os.makedirs(filePath)

    with open(filePath + "/" + fileName, 'w+' if not append else 'a+') as file:
        file.write(content)

    # push to cloud
    if _filePath == "notes":
        try:
            os.system(f"rclone copy {filePath} {getItem('path_cloud_notes')}")
        except Exception as e:
            log(f"Could not sync Notes to cloud: {e}")

def getConfigItem(key=None):
    try:
        with open(configPath, 'r+') as file:
            return json.load(file)[key]
    except FileNotFoundError:
        if key == 'securePath':
            setConfigItem(key, str(pathlib.Path(getItem('path_log')).resolve().parent))
            return str(pathlib.Path(getItem('path_log')).resolve().parent)

def setConfigItem(key=None, value=None):
    """
    Updates the internal configuration file
    """

    global configPath

    if value == None:
        print("No changes were made.")
    else:

        # error correction
        if(key == 'securePath' and value[0] != '/'):
            value = f"/{value}"
        if(key == 'securePath' and value[-1] == '/'):
            value = f"{value[:-1]}"
        print(f"\n\nUpdated configuration.")

    try:
        with open(configPath, 'r+') as file:
            config =  json.load(file)
    except FileNotFoundError:
        with open(configPath, 'x+') as f:
            print(f"Warning: existing config file not found; created a new one")
            f.write('{}')
            config = {}
            
    config[key] = value

    with open(f'{pathlib.Path(__file__).resolve().parent}/config.json', 'w+') as file:
        json.dump(config, file, indent=4)

    return value

def log(content=None, logName=None, clear=False, filePath=None):
    """
    Appends to a log file, or deletes it if clear is True.
    """

    global logPath
    if logName == None:
        logName = "LOG_DAILY"

    if(filePath == None):
        filePath = logPath

    logName = logPath + logName

    if not os.path.exists(filePath):
        print(f"Creating {filePath}")
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

if __name__ == "__main__":
    print(f"SecureData is a library not intended to be directly run. See README.md.")

if argv[-1] == 'config':
    setConfigItem('securePath', input("Enter the full path of where you want to store all data:\n"))