# cowin-ping
Ping CoWin API backend for appointment details

## Usage: 

```
python cowin-ping.py [city] [minimum_age]
city: Mumbai, Delhi, Bengaluru (for more options, open district_mapping.yaml)
age: 18, 45
```

The script refreshes every 1 second by default. Disable it by appending `--no-refresh` to the command.

## To-Do:

* Add async support for multiple districts
* Add auth header generation
* Structure program
* Get all district IDs
* Have better way to handle cli commands