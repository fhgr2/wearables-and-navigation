# wearables-and-navigation

## Setup

The installation is based on Raspbian Stretch 2017-11-29.

Change keyboard layout:

```bash
sudo dpkg-reconfigure keyboard-configuration # reboot afterwards
```

Set timezone:

```bash
sudo raspi-config # -> Localisation Options -> Change Timezone -> Europe -> Zurich
```

Enable SSH:

```bash
sudo raspi-config # -> 5 Interfacing Options -> P2 SSH -> Yes
```

Change password to "***REMOVED***":
```
passwd
```

Block the kernel module responsible for the internal soundcard to improve chances that a Bluetooth speaker will be reconnected to after a reboot: Create a file `/etc/modprobe.d/blacklist.conf` with the following content:

```
blacklist snd_bcm2835
```

Allow flask to use port 5000 (without root privileges) and at the same time users to connect on http default port 80, by redirecting traffic directed to port 80 onto port 5000:

```bash
sudo iptables -A PREROUTING -t nat -p tcp --dport 80 -j REDIRECT --to-ports 5000 # port redirection for outsiders
sudo iptables -t nat -A OUTPUT -o lo -p tcp --dport 80 -j REDIRECT --to-port 5000 # port redirection for localhost, see https://askubuntu.com/a/579540
sudo mkdir /etc/iptables
sudo sh -c 'sudo iptables-save > /etc/iptables/rules.v4' # iptables rules are ephemeral, save them into a file, from https://stackoverflow.com/a/82278
```

Load iptables rules at network startup by creating the file `/etc/network/if-pre-up.d/iptablesload` with the following content:

```bash
#!/bin/sh
iptables-restore < /etc/iptables/rules.v4
exit 0
```

make it executable by issuing:

```bash
sudo chmod +x /etc/network/if-pre-up.d/iptablesload
```

(Sources: https://askubuntu.com/q/444729 , https://serverfault.com/q/246829, https://www.thomas-krenn.com/de/wiki/Iptables_Firewall_Regeln_dauerhaft_speichern , https://help.ubuntu.com/community/IptablesHowTo#Saving_iptables )

Enable serial interface:

```bash
sudo raspi-config # -> 5 Interfacing Options -> P6 Serial -> login shell: no -> serial port hardware: yes
```

Connect to WiFi (ideally an Android Hotspot) using GUI (see top-right corner)

Install necessary software:

```bash
sudo apt-get update
sudo apt install vim gpsbabel python-espeak libgeos-dev gpsd gpsd-clients python-gps colordiff tcpdump # install OS packages
pip3 install gpsd-py3 tenacity openrouteservice Flask gpiozero shapely pyproj pyttsx3 # install python packages
```

Configure gpsd, by ensuring that the following settings are present in `/etc/default/gpsd`:

```
USBAUTO="false"
GPSD_OPTIONS="/dev/serial0"
GPSD_SOCKET="/var/run/gpsd.sock"
```

Enable and start gpsd daemon:

```bash
sudo systemctl enable gpsd.socket
sudo systemctl start gpsd.socket
```

Clone git repo:

```bash
cd ~; git clone https://github.com/htwchur/wearables-and-navigation.git
```

Configure gpsd configuration:

TODO

Setup autostart:

```bash
sudo cp ~/wearables-and-navigation/src/init/wan-router /etc/init.d/wan-router
sudo chmod +x /etc/init.d/wan-router
sudo update-rc.d wan-router defaults
```

Start software for the first time (this will happen automatically with future boots):

```bash
sudo /etc/init.d/wan-router start
```


## src

### Summary

`/etc/init.d/wan-router start` --> `start-flask-dev.sh` --> `flask-app.py` --> `main.py`

### Operation

The application will be installed and used as a daemon. The daemon control script is at `/etc/init.d/wan-router`. It expects the code to be at `/home/pi/wearables-and-navigation/src/`. Specifically, it will launch `start-flask-dev.sh` which then starts the [Flask](https://de.wikipedia.org/wiki/Flask) application `flask-app.py` including a webserver, which in turn starts a new process of `main.py` for every newly requested destination. The setup is a bit atypically for a web application because the calculations (routing) will only just have started when Flask returns an HTTP response. The routing (main.py) will be started asynchronously as a new process. If a new routing request or the ressource `/kill` is called, the old routing process will be terminated and a new process will be started.

In `src/config.py` you'll find some configurable values, among these are:

- `routing`: When and how exactly to make routing announcements
- `vibration`: Timings for vibration
- `announcers`: What types of announcers to be used
- `gpsd`: Where to read GPS information (ip and port of a gpsd daemon, may be on localhost)

Point your browser at `x.x.x.x:5000` (replace x.x.x.x with actual IP address) to reach the GUI. If you're using an Android Hotspot, you can get the IP addresses of connected clients using the app [Termux](https://play.google.com/store/apps/details?id=com.termux) and issuing the command `ip neigh`.

### Development

#### Starting `main.py` directly:

    cd src/; export GPIOZERO_PIN_FACTORY=mock; ./main.py --lat 46.85449 --lon 9.52864

Explanation:

- Setting `GPIOZERO_PIN_FACTORY` is necessary (only) on a system that is not a Raspberry Pi
- `--lat` and `--lon` are the destination coordinates (these are necessary)

#### Working with Flask

In order for signal handling in the Flask application to work, unfortunately one needs to disable auto-reloading of files by setting `FLASK_DEBUG=1` in `start-flask-dev.sh`. When changing a file, one needs to stop Flask by pressing `Ctrl-c` or calling `sudo /etc/init.d/wan-router stop` and then restart it.

The HTML code for the GUI can be found in `src/templates/`, which uses [Jinja2](http://jinja.pocoo.org/docs) templates.

#### Faking the GPS position

Instead of using a hardware GPS, we can also inject faked GPS data. For this we need either a `.nmea` file or a `.gpx` file that will be converted to NMEA format. You can find a converter in `utils/`. Usage:

```bash
./gpx2nmea.sh infile.gpx outfile.nmea
```

Note that the GPX file name must not contain umlauts.

To inject the faked position call:

```bash
gpsfake -c 1 -P 55555 feldis-brambrueesch-2011-09-03-161919.nmea
```

To test gpsd, call:

    cgps localhost:55555 # for fake gps

or

    cgps localhost:2947 # for hardware gps

To increase the processing speed, decrement both

- `gpsfake` paramenter `-c`
- `config.py` --> `routing['main_poll_interval']`

to a value of `0.1` (seconds).


#### Class diagram

![Class diagram](https://raw.githubusercontent.com/htwchur/wearables-and-navigation/master/doc/klassendiagramm.png?token=AEgeBcwyK-BGEYOd-_7Hbdl9AD3iPqvnks5bENfjwA%3D%3D "Class diagram")

The class diagram was rendered using http://plantuml.com/ .

## Links

- https://docs.google.com/document/d/***REMOVED***/edit


## Accounts

### OpenRouteService

```
htw:***REMOVED***

API-Key:
***REMOVED***
```


