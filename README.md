# SecureData
A library that allows for easy reading/writing of settings across repositories, as well as mail and logging.

## Author
- Tyler Woodfin
    - [GitHub](https://www.github.com/tylerjwoodfin)
    - [Website](http://tyler.cloud)

## Features
- Get/Set data within a JSON file in the location of your choice
- Using rclone, automatically sync to/from directories as needed
- Log to a file/directory of your choice without having to configure `logger` each time
- Send/receive mail using Gmail

## Structure

- Data is stored in `settings.json` (in `~/securedata` by default)
- Logs are written to `~/securedata/log` by default

## Installation and Setup

```bash
  python3 -m pip install securedata
```

### mail
- You will need to enable "less secure apps" for the Gmail account you use. [See this article](https://support.google.com/accounts/answer/6010255?hl=en).
    - Because you're storing your password in plaintext and because your account is "less secure", I HIGHLY recommend using a "throwaway" account.
    - It's never a good idea to reduce security on an account you regularly use.
- In `settings.json`, add the `email` object to make your settings file look like this example:
```
{
    "email": {
        "from": "throwaway@gmail.com",
        "from_pw": "example",
        "from_name": "Raspberry Pi",
        "to": "destination@protonmail.com"
    }
}
```

### Configuration
- To choose where `settings.json` is stored, use
```
securedata config
```

- To choose where logs will be stored, edit `settings.json` and set `path_log` to the full path to the log folder.

## Examples

### `setItem`
```
from securedata import securedata

securedata.setItem("employee", "Tyler", "salary", 7.25)
```

results in this structure in settings.json:

```
{
    "employee": {
        "Tyler": {
            "salary": 7.25
        }
    }
}
```

### `getItem`
```
from securedata import securedata

print(securedata.getItem("employee", "Tyler", "salary")) # given example settings.json above
```

```
> python3 test.py
> 7.25
```

### `mail`
```
from securedata import mail

mail.send('Test Subject', 'Test Body')
```

### `log`
```
from securedata import securedata

# writes to a file named LOG_DAILY YYYY-MM-DD in the default log folder (or securedata.getItem('path_log')) inside a YYYY-MM-DD folder
securedata.log("Dear Diary...")
securedata.log("This function hit a breakpoint", level="debug")
securedata.log("Looks like the server is on fire", level="critical")
securedata.log("This is fine", level="info")

# writes to a file named LOG_TEMPERATURE
securedata.log("30", logName="LOG_TEMPERATURE")

# writes to a file named LOG_TEMPERATURE in /home/pi/weather
securedata.log("30", logName="LOG_TEMPERATURE", filePath="/home/pi/weather")

    # format
    # 2021-12-29 19:29:27,896 — INFO — 30

```

## Dependencies
- Python >= 3.6
- [Rclone](https://rclone.org)
    - optional, used to sync data to/from cloud providers
    - support for customizing this with `securedata.config` in a future update

## Disclaimers
- This is an early stage project. There are still some things to tweak, and although I've done quite a bit of testing, I can't guarantee everything that works on my machine will work on yours. Always back up your data to multiple places to avoid data loss.
- If you find any issues, please contact me... or get your hands dirty and raise a PR!