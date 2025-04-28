#include <MeUltrasonicSensor.h> // inclusion de la librairie utilisée par la capteur ultrasonique
#include <MeMegaPi.h> // inclusion de la librairie utilisée par la carte MegaPi
#include <Arduino.h>
#include <Wire.h>
#include <SoftwareSerial.h>


#define MIN_DISTANCE 200; // Distance minimale de détection en centimètres


MeMegaPiDCMotor motor1(PORT1B); // déclaration des ports du moteur 1 sur la carte
MeMegaPiDCMotor motor2(PORT2B); // idem pour moteur 2


int motorspeed = 50; // définition de la vitesse d'avance du robot
int motorspeed2 = 10; // défnition d'une vitesse annexe d'avance du robot (si nécessaire)


void forward(){ // faire avancer le robot
  motor1.run(motorspeed);
  motor2.run(-motorspeed);
}

void turnright(){ // faire tourner à droite le robot
  motor1.run(motorspeed);
}

void turnleft(){ // faire tourner à gauche le robot
  motor2.run(-motorspeed);
}
#include <MeUltrasonicSensor.h> // inclusion de la librairie utilisée par la capteur ultrasonique
#include <MeMegaPi.h> // inclusion de la librairie utilisée par la carte MegaPi
#include <Arduino.h>
#include <Wire.h>
#include <SoftwareSerial.h>


#define MIN_DISTANCE 200; // Distance minimale de détection en centimètres


MeMegaPiDCMotor motor1(PORT1B); // déclaration des ports du moteur 1 sur la carte
MeMegaPiDCMotor motor2(PORT2B); // idem pour moteur 2


int motorspeed = 50; // définition de la vitesse d'avance du robot
int motorspeed2 = 10; // défnition d'une vitesse annexe d'avance du robot (si nécessaire)


void forward(){ // faire avancer le robot
  motor1.run(motorspeed);
  motor2.run(-motorspeed);
}


void turnright(){ // faire tourner à droite le robot
  motor1.run(motorspeed);
}


void turnleft(){ // faire tourner à gauche le robot
  motor2.run(motorspeed);
}

void stopnow(){ // faire arrêter le robot
  motor1.run(0);
  motor2.run(0);
}
void setup() { // à l'état initial, le robot est à l'arrêt
  stopnow();

}

void loop() { // boucle du programme
  MeUltrasonicSensor ultrasonic(PORT_8); // déclaration du port du capteur ultrasonique
    while (1) {
    int distance = ultrasonic.distancecm(); // création de la variable correspondant à la distance mesurée par le capteur
    if (distance > MIN_DISTANCE) { // si pas d'obstacle à moins de 20cm, le robot avance
        forward();
    } else if (distance < MIN_DISTANCE) { // si obstacle, le robot démarre la procédure d'évitement
        stopnow();
        turnright();
        delay(2000); // déterminé approximativement, de sorte à laisser du temps au robot de tourner à 90 degrés
        forward();
        delay(200);
        turnleft();
        forward();
        turnleft();
        delay(200);
        forward();
        turnright();
        delay(2000);
        forward();
    }
}
stoppnow(); // le robot s'arrête en fin de boucle
}
void stopnow(){ // faire arrêter le robot
  motor1.run(0);
  motor2.run(0);
}
void setup() { // à l'état initial, le robot est à l'arrêt
  stopnow();

}

void loop() { // boucle du programme
  MeUltrasonicSensor ultrasonic(PORT_8); // déclaration du port du capteur ultrasonique
    while (1) {
    int distance = ultrasonic.distancecm(); // création de la variable correspondant à la distance mesurée par le capteur
    if (distance > MIN_DISTANCE) { // si pas d'obstacle à moins de 20cm, le robot avance
        forward();
    } else if (distance < MIN_DISTANCE) { // si obstacle, le robot démarre la procédure d'évitement
        stopnow();
        turnright();
        delay(2000); // déterminé approximativement, de sorte à laisser du temps au robot de tourner à 90 degrés
        forward();
        delay(200);
        turnleft();
        forward();
        turnleft();
        delay(200);
        forward();
        turnright();
        delay(2000);
        forward();
    }
}
stoppnow(); // le robot s'arrête en fin de boucle
}