#include <Servo.h>
#include <Encoder.h>
#include <Wire.h>
#include <ros.h>
#include <std_msgs/Int16.h>
#include <std_msgs/Float64.h>
#include <std_msgs/Empty.h>


Servo servopotentiometer;
Servo servoencoder;


///Set Encoder Pin
const int PINClk =2;
const int PINDT =3;

const int SW_PIN = 4;
const int homePosition = 0; 
const int stepValue = 5;
const int servo_encoder = 9;
int servoAngel = homePosition;

///Set Potentiometer Pin
int val = 0;
int servo_potentiometer = A3;
int potentiometerPin = A0;

Encoder encoder(PINClk, PINDT);

ros::NodeHandle nh;

// Publisher Encoder Angle
std_msgs::Int16 servo_msg;
ros::Publisher servo_pub("servo_angle", &servo_msg);

// Publisher Potentiometer Angle
std_msgs::Float64 poten_msg;
ros::Publisher poten_pub("poten_angle", &poten_msg);

//Receive encoder angle data from GUI subscriber
void poten_servo(const std_msgs::Float64& cmd_msg)
{
  float value = cmd_msg.data;
  servopotentiometer.write(value);
}

//Receive Potentiometer angle data from GUI subscriber
void encoder_servo(const std_msgs::Float64& cmd_msg)
{
  float value = cmd_msg.data;
  servoencoder.write(value);
}

//Subscriber Encoder Angle for servo
ros::Subscriber<std_msgs::Float64> encoderrun("Encoder_Run", &encoder_servo);

//Subscriber Potentiometer Angle for servo
ros::Subscriber<std_msgs::Float64> potenrun("Poten_Run", &poten_servo);



void setup() {
  pinMode(SW_PIN,INPUT_PULLUP);
  servoencoder.attach(servo_encoder);  

  //potentiometer
  servopotentiometer.attach(servo_potentiometer);
  pinMode(servo_potentiometer,OUTPUT);
  pinMode(potentiometerPin,INPUT);

  nh.initNode();
  nh.advertise(servo_pub);
  nh.advertise(poten_pub);
  nh.subscribe(encoderrun);
  nh.subscribe(potenrun);
  
}


long oldPosition  = -999;

void loop() {
  
  //Potentiometer code to send values between 0 to 180 degrees 
    val = analogRead(potentiometerPin);
    float angle = map(val, 0, 1023, 0, 180);
    poten_msg.data = angle; 
    poten_pub.publish(&poten_msg); //Publisher angle values to GUI
    nh.spinOnce();

  
  //Encoder code to send values between 0 to 180 degrees
  long newPosition = encoder.read();
 
  if(newPosition != oldPosition){
    //Case when the angle decreases by not more than 0 degrees
    if(newPosition >  oldPosition)
    {
    int newStep = abs(newPosition - oldPosition);     
      servoAngel -= stepValue;
      if(servoAngel < 0){
          servoAngel =0;    
      }  
      servo_msg.data = servoAngel;
      servo_pub.publish(&servo_msg); //Publisher angle values to GUI
      nh.spinOnce();


    }

    //Case when the angle increases by not more than 180 degrees
    if(newPosition <  oldPosition )
    {
    int newStep = abs(newPosition - oldPosition);      
      servoAngel += stepValue;
      if(servoAngel > 180)
          servoAngel =180;
      servo_msg.data = servoAngel;
      servo_pub.publish(&servo_msg);//Publisher angle values to GUI
      nh.spinOnce();  

    }
   oldPosition = newPosition;
  }

  nh.spinOnce();
  delay(10);
  
}
