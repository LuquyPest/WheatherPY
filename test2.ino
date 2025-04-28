#include <MeUltrasonicSensor.h> // inclusion de la librairie utilisée par la capteur ultrasonique
#include <MeMegaPi.h> // inclusion de la librairie utilisée par la carte MegaPi
#include <Arduino.h>
#include <Wire.h>
#include <SoftwareSerial.h>

MeMegaPiDCMotor motor1(PORT1B); // déclaration des ports du moteur 1 sur la carte 
MeMegaPiDCMotor motor2(PORT2B); // idem pour moteur 2

int motorspeed = 120; // définition de la vitesse d'avance du robot 
int MIN_DISTANCE = 20; // Distance minimale de détection en centimètres

void forward(){ // faire avancer le robot
    motor1.run(-motorspeed);
    motor2.run(motorspeed);
}

void turnright(){ // faire tourner à droite le robot 
    motor1.run(motorspeed);
    motor2.run(motorspeed);
}

void turnleft(){ // faire tourner à gauche le robot 
    motor1.run(-motorspeed);
    motor2.run(-motorspeed);
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
    int distance = ultrasonic.distanceCm(); // création de la variable correspondant à la distance mesurée par le capteur
    if (distance > MIN_DISTANCE) { // si pas d'obstacle à moins de 20cm, le robot avance
        forward();
    } else if (distance < MIN_DISTANCE) { // si obstacle, le robot démarre la procédure d'évitement 
      stopnow();
      delay(500);// pause de 0,5sec
      turnright();
      delay(1500); // déterminé approximativement, de sorte à laisser du temps au robot de tourner à 90 degrés
      stopnow();
      delay(500);// pause de 0,5sec
      forward();
      delay(2000);
      stopnow();
      delay(500);// pause de 0,5sec
      turnleft();
      delay(1400);
      stopnow();
      delay(500);// pause de 0,5sec    
      forward();
      delay(4000);
      stopnow();
      delay(500);// pause de 0,5sec      
      turnleft();
      delay(1400);
      stopnow();
      delay(500);// pause de 0,5sec      
      forward();
      delay(2000);
      stopnow();
      delay(500);// pause de 0,5sec     
      turnright();
      delay(1500);
      stopnow();
      delay(500);// pause de 0,5sec      
      forward();
    }
  }
  stopnow(); // le robot s'arrête en fin de boucle 
}


