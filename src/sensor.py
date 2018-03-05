# ADXL345 Python library for Raspberry Pi
#
# author:  Jonathan Williamson
# license: BSD, see LICENSE.txt included in this package
#
# This is a Raspberry Pi Python implementation to help you get started with
# the Adafruit Triple Axis ADXL345 breakout board:
# http://shop.pimoroni.com/products/adafruit-triple-axis-accelerometer

import smbus, os, math,csv
from flask import Flask
from time import sleep

app = Flask(__name__)



bus = smbus.SMBus(1)

power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68       # This is the address value read via the i2cdetect command

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)

def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

def getData():
    gx= read_word_2c(0x43)/131
    gy= read_word_2c(0x45)/131
    gz= read_word_2c(0x47)/131
    
    accel_xout = read_word_2c(0x3b)
    accel_yout = read_word_2c(0x3d)
    accel_zout = read_word_2c(0x3f)

    ax = accel_xout / 16384.0
    ay= accel_yout / 16384.0
    az= accel_zout / 16384.0
    
    return [ax,ay,az,gx,gy,gz]

@app.route("/")
def hello():

    return 'Success'

i=0
with open('testData.csv','wb') as csvfile:
    writer= csv.writer(csvfile)
    while (i<1000) :
        data=getData()
        print data
        writer.writerow(data)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
