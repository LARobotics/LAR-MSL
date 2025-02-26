from machine import Pin, UART, PWM
import utime
import _thread
import sys

led = Pin("LED", Pin.OUT)

uart = UART(0, baudrate=115200)
#uart.init(bits=8, parity=None, stop=2)

first_Time = True
defend = False

time_to_up = 500
time_to_down = 150
time_stay = 1200 - time_to_up - time_to_down

# motor_H enable forward and reverse pins
motor_en = PWM(Pin(20, Pin.OUT))
motor_fwd = Pin(21, Pin.OUT)
motor_rv = Pin(22, Pin.OUT)

# motor_H pins frequency
motor_en.freq(1000)

# motor_H pins set to low
motor_en.duty_u16(0)
motor_fwd.low()
motor_rv.low()

motor_state = "IDLE"

current_time = utime.ticks_ms()
old_time = current_time

command = "0"
        
def switch():
    global command
    global current_time
    global old_time
    global motor_state
    global motor_en
    global motor_fwd
    global motor_rv
    global first_Time
    if motor_state == "UP":
        motor_en.duty_u16(65535)
        motor_fwd.high()
        motor_rv.low()
        current_time = utime.ticks_ms()
        if current_time - old_time > time_to_up:
            old_time = current_time
            motor_state = "STAY"
            print("State STAY")
    elif motor_state == "STAY":
        motor_en.duty_u16(int((20/100)*65535))
        motor_fwd.high()
        motor_rv.low()
        current_time = utime.ticks_ms()
        if current_time - old_time > time_stay:
            old_time = current_time
            motor_state = "DOWN"
            print("State DOWN")
    elif motor_state == "DOWN":
        motor_en.duty_u16(65535)
        motor_fwd.low()
        motor_rv.high()
        current_time = utime.ticks_ms()
        if current_time - old_time > time_to_down:
            old_time = current_time
            motor_state = "WAIT"
            print("State WAIT")
    elif motor_state == "WAIT":
        motor_en.duty_u16(int((10/100)*65535))
        motor_fwd.high()
        motor_rv.low()
        current_time = utime.ticks_ms()
        if current_time - old_time > 4000:
            old_time = current_time
            motor_state = "IDLE"
            command = "0"
            print("State IDLE")
    elif motor_state == "IDLE":
        motor_en.duty_u16(0)
        motor_fwd.low()
        motor_rv.low()
        first_Time = True
        
        
def th_receive():
    global command
    while True:
        command = input()
        print("hello: ", command)


_thread.start_new_thread(th_receive, ())

while True:
    switch()
    if first_Time and command == "Defend":
        print("State UP")
        current_time = utime.ticks_ms()
        old_time = current_time
        first_Time = False
        motor_state = "UP"
        led.toggle()
        
    

