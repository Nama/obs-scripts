# OBS-Studio python scripts
* [Speedtest](#speedtest)
* [Check Log](#check-log)

## General info
OBS seems to crash a lot if you reload scripts. Even if your scripts run fine(?). Try to reload, if it crashes, test your script with restarting OBS.

## Scripts
### Speedtest
Makes a speedtest upon starting OBS or changing the scene to make sure your internet connection is fine before you start your stream.

* Requires the module `speedtest` in your python installation
* May freeze OBS while doing the speedtest, just give it half a minute
* The results are shown on a text source which needs to be set first
* Text source will be hidden if a recording starts and visible again if recording stops

### Check Log
Checks the current log for the string which is set in the settings and notifies the user on the set text source.
Text source will be empty if nothing found.
