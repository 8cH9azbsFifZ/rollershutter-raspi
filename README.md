#Rollershutter-Raspi

Raspi for controlling a rollershutter for integration with
OpenHAB using a MQTT binding.


# Installation
+ Prepare a raspi with a fresh raspian
+ Install the dependencies using ` python3 -m pip install -r requirements.txt `
+ Run manually using `python3 rollershutter.py `

# Wiring
+ PIN Down: BCM 17 (PIN 11)
+ PIN Up: BCM 27 (PIN 13)


23 18
24 16