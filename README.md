# SecureData
A library that allows for easy reading/writing of settings across repositories, as well as logging.

## Author
- Tyler Woodfin
    - [GitHub](https://www.github.com/tylerjwoodfin)
    - [Website](http://tyler.cloud)

## Structure

- Data is stored in `{thisDirectory}/settings.json`
- Logs are written to `{thisDirectory}/log/{logName}`

## Installation

```bash
  pip install securedata
```

## Examples

### `setItem`
```
import securedata

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

import securedata

print(securedata.getItem("employee", "Tyler", "salary")) # given example settings.json above
```

```
> python3 test.py
> 100000
```