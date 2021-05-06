# cowin-ping
Ping CoWin API backend for appointment details

USAGE: 

```
python cowin-ping.py <city> <minimum_age> <minimum_slots>
City: Choose from Mumbai, Delhi or Bengaluru
Age: 18 or 45
```

Use with the watch binary for refreshed results

```
watch -n 1 python cowin_ping.py Delhi 18 1
```

Or use the built in refresher. Enable it by setting `REFRESH_RESULTS` in the script to `True`
