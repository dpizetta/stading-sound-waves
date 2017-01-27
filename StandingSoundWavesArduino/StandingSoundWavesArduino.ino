// -*- coding: utf-8 -*-

/* Program to move a step motor throuth serial computer.
 * :author: Daniel Cosmo Pizetta, Adilson Wanderley Barros
 * :contact: daniel.pizetta@usp.br, adilson.wanderley@usp.br
 * :site: https://github.com/dpizetta/stading-sound-waves
 *
 * If you are using this, please cite us:
 * Revista Brasileira de Ensino de Física
 * Title: An experimental evaluation of standing sound waves in pipes
 * Authors: Daniel Cosmo Pizetta, Adilson Barros Wanderley, Valmor Roberto Mastelaro, Fernando Fernandes Paiva
 * DOI: 10.1590/1806-9126-RBEF-2016-0264
 *
 * */

#include <Stepper.h>

const int led = 13;
const int beep = 7;
const int serialSpeed = 9600;           // must be the same in Python
const int stepsPerRevolution = 100;     // steps per revolution

// Python commands
#define START 1
#define WALK 2
#define STOP 3

// initialize the stepper library on pins 8 through 11:
Stepper myStepper(stepsPerRevolution, 8, 9, 10, 11);

// Alerts the start (begin), you have 5 seconds before it starts
void alertStart()
{
	for (int i = 0; i < 3; i++) {
		digitalWrite(led, HIGH);
		tone(beep, 110, 500);
		digitalWrite(led, LOW);
		delay(500 * 1.5);
	}
	digitalWrite(led, HIGH);
	tone(beep, 131, 1000);
	digitalWrite(led, HIGH);
	delay(5000);
}

// Alerts the stop (end)
void alertStop()
{
	digitalWrite(led, HIGH);
	tone(beep, 151, 2000);
	digitalWrite(led, LOW);
}


void setup() {
	// initializes serial and pins
	Serial.begin(9600);
	pinMode(led, OUTPUT);
	pinMode(beep, OUTPUT);

	while (Serial.available() > 0) {

		int flag = Serial.parseInt();             // command
		int motorSpeed = Serial.parseInt();       // motor velocity in RPM
		int motorSteps = Serial.parseInt();       // steps to run

	    if (Serial.read() == '\n') {
	    	// get ready to start
	    	if (flag == START){
				Serial.println("STARTING")
				alertStart();
	    	}
	    	// put in a new position
	    	else if (flag == WALK){
				Serial.println("WALKING")
				myStepper.setSpeed(motorSpeed);
				myStepper.step(motorSteps);
			}
	    	// stops, end the measurement
			else if (flag == STOP){
				Serial.println("STOPING")
				alertStop();
				break;	
			}
	    	// informs the serial to send command
			else {
				Serial.println("READY")
			}
		}
	    
		delay(250); // to not read to much serial
	}
}

void loop() {
}

