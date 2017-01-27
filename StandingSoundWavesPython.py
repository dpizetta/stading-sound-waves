#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Program to move a step motor throuth serial computer.

:author: Daniel Cosmo Pizetta, Adilson Wanderley Barros
:contact: daniel.pizetta@usp.br, adilson.wanderley@usp.br
:site: https://github.com/dpizetta/stading-sound-waves

If you are using this, please cite us:
Revista Brasileira de Ensino de Física
Title: An experimental evaluation of standing sound waves in pipes
Authors: Daniel Cosmo Pizetta, Adilson Barros Wanderley, Valmor Roberto Mastelaro, Fernando Fernandes Paiva
DOI: 10.1590/1806-9126-RBEF-2016-0264

http://people.csail.mit.edu/hubert/pyaudio/

If you have problems with jackd in Linux, try:
sudo apt-get intall jack
dpkg-reconfigure -p high jack

"""

import serial
import pyaudio
import wave
import time

CHUNK = 1024
FORMAT = pyaudio.paInt32  # Type of data
CHANNELS = 1              # Stereo or mono
RATE = 20000              # Samples per second

MEASURE_TIME = 0.5        # Measuring time per step
FILENAME = 'measure_name' # File name without extension

STEPS_PER_REVOLUTION = 100
SPEED = 20                  # rpm

INITIAL_LENGHT = 0.0        # mm
FINAL_LENGHT = 300.0        # mm
STEP = 1.4                  # mm 

ACQ_NUMBER = int((FINAL_LENGHT-INITIAL_LENGHT)/STEP)

flag = ''
START = 1
WALK = 2
STOP = 3

# choose the arduino serial name, find it in your computer (ttyUSB0, ttyACM0, etc.)
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1);

# starts pyaudio
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK)
stream.stop_stream()
frames = []

def record():
    """Record the sound."""
	stream.start_stream()
	for i in range(0,int(RATE/CHUNK*MEASURE_TIME)):
			data = stream.read(CHUNK)
			frames.append(data)
	stream.stop_stream()

flag=arduino.readline()

while flag != 'READY':
	print("Waiting to be ready... ")
	flag=arduino.readline()
    print(flag, type(flag))

for measure in range(0,ACQ_NUMBER):

	flag=arduino.readline()

	if flag == 'READY': 
	    print("Start recording...")
	    record()
	    print("Pause recording...")

	    print("Start walking...")
        arduino.write(byte(str(START)+','+str(SPEED)+','+str(STEPS_PER_REVOLUTION)))
	    print("Stop walking...")

arduino.write('STOP')
print("Ending measurements...")

# closing everything
arduino.close()
audio.terminate()
stream.close()

# writing wave file
wf = wave.open(FILENAME+'.wav', 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(audio.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()


