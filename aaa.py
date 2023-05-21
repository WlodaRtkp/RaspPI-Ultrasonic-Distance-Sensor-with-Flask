import RPi.GPIO as GPIO
import time
from gpiozero import LED
from flask import Flask, render_template, jsonify

app = Flask(__name__)

red = LED(17)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
TRIG = 23
ECHO = 24
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

def measure_distance():
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG,GPIO.LOW)
    
    pulse_start = 0
    pulse_end = 0
    
    while GPIO.input(ECHO)==GPIO.LOW:
        pulse_start = time.time()
    while GPIO.input(ECHO)==GPIO.HIGH:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    return (distance)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/distance')
def distance():
    return render_template('jazdunia.html', distance=distance)
        
@app.route('/get_distance')
def get_distance():
        distance = measure_distance()
        red.off()
        if distance < 10.00:
            red.blink()
            time.sleep(0.5)
        if distance < 5.00:
            red.on()
            time.sleep(0.5)
        return jsonify(distance=float(distance))
    
if __name__ == '__main__':
    app.run()

