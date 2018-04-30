#!/usr/bin/env python3
import ev3dev.ev3 as ev3
from time import sleep

def go_straight(time, speed):
    m_l = ev3.LargeMotor('outB')
    m_r = ev3.LargeMotor('outC')
    m_l.run_timed(time_sp=time, speed_sp=speed)
    m_r.run_timed(time_sp=time, speed_sp=speed)

def go_right(time, speed):
    m_l = ev3.LargeMotor('outB')
    m_r = ev3.LargeMotor('outC')
    m_l.run_timed(time_sp=time, speed_sp=speed)
    m_r.run_timed(time_sp=time, speed_sp=0)

def go_left(time, speed):
    m_l = ev3.LargeMotor('outB')
    m_r = ev3.LargeMotor('outC')
    m_l.run_timed(time_sp=time, speed_sp=0)
    m_r.run_timed(time_sp=time, speed_sp=speed)

def color_detect(mode, port):
    c_s = ev3.ColorSensor(port)
    if mode == 0:
        col = c_s.reflected_light_intensity
    else:
        col = c_s.color
    return col

def IR_detect(mode):
    ir = ev3.InfraredSensor()
    if mode == 0:
        ir.mode = 'IR-SEEK'
        direction = ir.value()
        print(direction)
    else:
        ir.mode = 'IR-PROX'
        distance = ir.value()
        print(distance)

def speak(statement):
    ev3.Sound.speak(str(statement)).wait()

def right_angle(speed, position):
    m_l = ev3.LargeMotor('outB')
    m_r = ev3.LargeMotor('outC')
    m_l.run_to_rel_pos(position_sp=position, speed_sp=speed, stop_action="hold")
    m_r.run_to_rel_pos(position_sp=-position, speed_sp=speed, stop_action="hold")
    sleep(2)

def left_angle(speed, position):
    m_l = ev3.LargeMotor('outB')
    m_r = ev3.LargeMotor('outC')
    m_l.run_to_rel_pos(position_sp=-position, speed_sp=speed, stop_action="hold")
    m_r.run_to_rel_pos(position_sp=position, speed_sp=speed, stop_action="hold")
    sleep(2)

def forward_angle(speed, position):
    m_l = ev3.LargeMotor('outB')
    m_r = ev3.LargeMotor('outC')
    m_l.run_to_rel_pos(position_sp=position, speed_sp=speed, stop_action="hold")
    m_r.run_to_rel_pos(position_sp=position, speed_sp=speed, stop_action="hold")
    sleep(2)

def turn_right():
    forward_angle(150, 120)
    right_angle(150, 239)
    forward_angle(150, 158)#175

def turn_left():
    forward_angle(150, 111)
    left_angle(150, 234)
    forward_angle(150, 180)

def straight_on():
    forward_angle(150, 265)

def turn_around():
    right_angle(150, 237*2)
    sleep(1)
    forward_angle(150, 60)






