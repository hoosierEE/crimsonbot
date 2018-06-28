from machine import Pin, time_pulse_us
from time import sleep_us

LOW = 0
HIGH = 1

class Sensor():
    '''
        Class for manipulating an HCSR04 Sensor.

        Example code:
            newSensor = HCSR04.Sensor()
            newSensor.start()
    '''

    def __init__(self, trig = Pin(2, Pin.OUT), echo = Pin(5, Pin.IN)):
        '''
        params:trig, echo: trig and echo take Pin Objects already instantiated
        with the correct PIn

        For reference, default values map to -
            machine.Pin(2) == Pin 4 on the ESP12E Motor Shield.
            machine.Pin(5) == Pin 1 on the ESP12E Motor Shield.

        '''

        self.trigPin = trig
        self.trigPin(0)
        self.echoPin = echo


    def start(self, measurement="CM", log=True):
        '''
        Starts a loop that calls get_distance repeatedly until the program is
        force stopped.

        A user should build their own while loop with getDistance() to get a
        value and their own stop-condition.
        '''

        run = True
        print("| STARTING SENSOR ---------- press ctrl+C to stop. |")
        sleep_us(100000)

        # TODO: Should probably add a stop condition. However this shouldnt be used
        # for control.
        while run:
            sense = self.get_distance_cm(measurement, log)

        return


    def get_distance_cm(self, measurement = "CM", log=True):
        '''
            Calculates a single sensor ping value.

        param:measurement: Defaults to Centimeter conversion. Takes string of either
        "CM" or "IN".
        param:log: Logging defaults to print the distance, set to False to skip.
        '''
        trigPin = self.trigPin
        echoPin = self.echoPin

        # Clears the trigPin
        trigPin(HIGH);
        trigPin(LOW);
        sleep_us(2)

        # Sets the trigPin on HIGH state for 10 micro seconds
        trigPin(HIGH);
        sleep_us(10);
        trigPin(LOW);

        # Reads the echoPin, `time` gets set to the sound wave
        # travel time in microseconds.
        try:
            time = time_pulse_us(echoPin, HIGH, 29000)
        except Exception:
            run = False

        # Calculating the distance in Centimeters
        dist_in_cm = (time / 2.0) / 29
        #Prints the distance on the Serial Monitor
        if log == True:
            print("Distance: ", dist_in_cm, "cm");

        return dist_in_cm

    def calc_CM(self, sensor_pulse_val, log):
        '''
        Currently unused. Ignore until Inch functionality is added.
        '''
        # Calculating the distance in Centimeters
        dist_in_cm = (time / 2.0) / 29
        #Prints the distance on the Serial Monitor
        if log == True:
            print("Distance: ", dist_in_cm, "cm");

        return dist_in_cm
