# SecureData
A library that allows for easy reading/writing of settings across repositories, as well as logging.

## Author
- Tyler Woodfin
    - [GitHub](https://www.github.com/tylerjwoodfin)
    - [Website](http://tyler.cloud)

## Disclaimers
- This is an early stage project. There are still some things to tweak, and although I've done quite a bit of testing, I can't guarantee everything that works on my machine will work on yours. Always back up your data to multiple places to avoid data loss.
- If you find any issues, please contact me... or get your hands dirty and raise a PR!

## Structure

- Data is stored in `settings.json` (in `~/securedata` by default)
- Logs are written to `~/securedata/log` by default

## Installation

```bash
  python3 -m pip install securedata
```
## Configuration
- To choose where `settings.json` is stored, use
```
securedata config
```

- To choose where logs will be stored, edit `settings.json` and set `path_log` to the full path to the log folder.

## Examples

### `setItem`
```
from securedata import securedata

securedata.setItem("employee", "Tyler", "salary", 100000)
```

results in this structure in settings.json:

```
{
    "employee": {
        "Tyler": {
            "salary": 100000
        }
    }
}
```

### `getItem`
```
# test.py

from securedata import securedata

print(securedata.getItem("employee", "Tyler", "salary")) # given example settings.json above
```

```
> python3 test.py
> 100000
```

## Dependencies
- Python >= 3.6