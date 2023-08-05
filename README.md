#Rollershutter-Raspi

Raspi for controlling a rollershutter for integration with
OpenHAB using a MQTT binding.


# Installation
+ Prepare a raspi with a fresh raspian
+ `apt-get -y install python3-pip`
+ Install the dependencies using ` python3 -m pip install -r requirements.txt `
+ Run manually using `python3 rollershutter.py `

# Wiring
+ PIN Down: BCM 23 (PIN 18)
+ PIN Up: BCM 24 (PIN 16)
 