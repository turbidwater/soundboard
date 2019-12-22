# soundboard
Python soundboard with configurable sets

to run, in the CLI navigate to the project directory. Then:
* to run on linux: `sudo python3 startup.py`
* to run on windows: `py startup.py`

to setup startup of the service on the Pi, follow the instructions here: https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/#systemd
to disable startup of the service, run `sudo systemctl disable custom.service`
to enable startup of the service once it has been disabled, run `sudo systemctl enable custom.service`
