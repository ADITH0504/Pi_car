
#include <AFMotor.h>
#include <SoftwareSerial.h>
#include <Servo.h>

//initial motors pin
AF_DCMotor motor1(1, MOTOR12_1KHZ);
AF_DCMotor motor2(2, MOTOR12_1KHZ);
AF_DCMotor motor3(3, MOTOR34_1KHZ);
AF_DCMotor motor4(4, MOTOR34_1KHZ);

Servo servo1;
Servo servo2;

String command = "";

void setup()
{
    Serial.begin(9600);
    servo1.attach(10);
    servo2.attach(9);
    servo1.write(0);
    servo2.write(180);
}

void loop() {

// CHECK SERIAL AVAILABILITY 

 if (Serial.available() > 0)
 {
  command = Serial.readStringUntil('\n');
  command.trim();
  Serial.print("Arduino: data Recievd");
  Serial.println(command);

  if ( command == "F") { forward() ;}
   else if ( command == "B") { back(); }
     else if ( command ==  "S") { Stop(); }
       else if ( command == "L")  { left(); }
         else if ( command == "R")  { right(); }
           else if ( command == "U") { up(); }
             else if (command == "D") { down(); }
           
 }
  
}

void forward()
{
  motor1.setSpeed(200); 
  motor1.run(FORWARD);  
  motor2.setSpeed(200); 
  motor2.run(FORWARD); 
  motor3.setSpeed(200); 
  motor3.run(FORWARD);  
  motor4.setSpeed(200); 
  motor4.run(FORWARD);  
}

void back()
{
  motor1.setSpeed(200); 
  motor1.run(BACKWARD); 
  motor2.setSpeed(200); 
  motor2.run(BACKWARD); 
  motor3.setSpeed(200);
  motor3.run(BACKWARD); 
  motor4.setSpeed(200);
  motor4.run(BACKWARD); 
}

void left()
{
  motor1.setSpeed(200); 
  motor1.run(BACKWARD);
  motor2.setSpeed(200); 
  motor2.run(BACKWARD); 
  motor3.setSpeed(200);
  motor3.run(FORWARD); 
  motor4.setSpeed(200); 
  motor4.run(FORWARD);  
}

void right()
{
  motor1.setSpeed(200); 
  motor1.run(FORWARD);  
  motor2.setSpeed(200); 
  motor2.run(FORWARD);  
  motor3.setSpeed(200); 
  motor3.run(BACKWARD); 
  motor4.setSpeed(200); 
  motor4.run(BACKWARD); 
}

void Stop()
{
  motor1.setSpeed(0);  
  motor1.run(RELEASE);
  motor2.setSpeed(0); 
  motor2.run(RELEASE); 
  motor3.setSpeed(0);  
  motor3.run(RELEASE); 
  motor4.setSpeed(0);  
  motor4.run(RELEASE);
}

void up()
{
    servo1.write(50);
    servo2.write(130);
}


void down()
{
  int pos1 = servo1.read();
  int pos2 = servo2.read();

  int target1 = 0;
  int target2 = 180;

  while (pos1 != target1 || pos2 != target2) {

    if (pos1 < target1) pos1++;
    else if (pos1 > target1) pos1--;

    if (pos2 < target2) pos2++;
    else if (pos2 > target2) pos2--;

    servo1.write(pos1);
    servo2.write(pos2);

    delay(20);
  }
}
