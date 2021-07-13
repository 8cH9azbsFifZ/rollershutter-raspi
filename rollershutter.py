import time
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import logging

logging.basicConfig(level=logging.DEBUG, format='Rollershutter(%(threadName)-10s) %(message)s')

class Rollershutter():
    def __init__(self, TimeUpwards = 10. , TimeDownwards = 10., MQTThostname = "t20", RollershutterName="Test1", PIN_BCM_Up = 17, PIN_BCM_Down = 27):
        self.Name = RollershutterName

        # Configure PINS
        self._relais_sw_up_pin = PIN_BCM_Up 
        self._relais_sw_down_pin = PIN_BCM_Down 

        GPIO.setmode(GPIO.BCM)
        time.sleep(1)
        GPIO.setup(self._relais_sw_up_pin, GPIO.OUT) 
        time.sleep(1)
        GPIO.setup(self._relais_sw_down_pin, GPIO.OUT) 
        time.sleep(1)

        # Connect to MQTT broker
        port = 1883
        self._client = mqtt.Client()
        self._client.connect(MQTThostname, port, 60)
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message

        self._samplingrate = 0.01

        # Remote control configuration
        self._sw_press_duration = 1 # 1 second press the buttons before release

    def _on_connect(self, client, userdata, flags, rc):
        """ Connect to MQTT broker and subscribe to control messages """
        logging.debug("Connected with result code " + str(rc))
        self._client.subscribe("rollershutter/control/" + self.Name)

    def _sendmessage(self, topic="/none", message="None"):
        """ Send a message using MQTT """
        ttopic = "rollershutter/" + self.Name + "/" + topic
        mmessage = str(message)
        logging.debug("MQTT>: " + ttopic + " ###> " + mmessage)
        self._client.publish(ttopic, mmessage)

    def _on_message(self, client, userdata, msg):
        """
        Receive MQTT control messages.
        Start with debugging on commandline using:
        mosquitto_pub -h t20 -t rollershutter/control/Test1 -m Down
        """
        logging.debug(">MQTT: " + msg.payload.decode())
        if msg.payload.decode() == "Stop":
            self.Stop()
        if msg.payload.decode() == "Up":
            self.Up()
        if msg.payload.decode() == "Down":
            self.Down()
        if msg.payload.decode() == "Percent": # FIXME
            self.Percent()

    def Down(self):
        logging.debug("Rollershutter: down")
        self._relais_on(self._relais_sw_down_pin)
        time.sleep(self._sw_press_duration)
        self._relais_off(self._relais_sw_down_pin)

    def Up(self):
        logging.debug("Rollershutter: up")
        self._relais_on(self._relais_sw_up_pin)
        time.sleep(self._sw_press_duration)
        self._relais_off(self._relais_sw_up_pin)

    def Stop(self):
        logging.debug("Rollershutter: stop")
        pass

    def Percent(self, percentage):
        logging.debug("Rollershutter: percent")
        pass

    def _relais_on(self, pin):
        GPIO.output(pin, GPIO.LOW)    
        
    def _relais_off(self, pin):
        GPIO.output(pin, GPIO.HIGH)

    def _core_loop(self):
        while True:
            self._client.loop(self._samplingrate) #blocks for 100ms (or whatever variable given, default 1s)


if __name__ == "__main__":
    print ("Run manual")
    r = Rollershutter()
    r._relais_on(r._relais1_pin)
    time.sleep(1)
    r._relais_off(r._relais1_pin)
    time.sleep(1)
    r._relais_on(r._relais2_pin)
    time.sleep(1)
    r._relais_off(r._relais2_pin)
    #r._core_loop()