import RPi.GPIO as GPIO

class ServoControl:
    def __init__(self):
        '''
        '''
        # Set the pinout mapping on the RPi
        GPIO.setmode(GPIO.BCM)

        # Set PIN_18 as GPIO Out (used for PWM):
        GPIO.setup(18, GPIO.OUT)

        # Initialize the PWM:
        PWM_FREQ_Hz = 50
        self.pwm = GPIO.PWM(18, PWM_FREQ_Hz)

    def start(self, duty_cycle):
        ''' 
        '''
        self.pwm.start(duty_cycle)

    def stop(self):
        ''' 
        '''
        self.pwm.stop()

    def change_duty_cycle(self, new_duty_cycle):
        ''' 
        '''
        self.pwm.ChangeDutyCycle(new_duty_cycle)

    def close(self):
        self.pwm.stop()

    def __enter__(self):
        '''
        '''

    def __exit__(self):
        '''
        '''
        self.close()
