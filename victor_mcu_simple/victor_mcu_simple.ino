#include <ESP8266WiFi.h>
#include <PID_v1.h>

#include "printf.h"


// Init constants and global variables

#define DEBUG 1

#define WheelSeparation  0.135                              // wheel separation in meters

void motion(int lpwm, int rpwm) {  // move motor at pwm power and change directions flags only when motor cross stop
  bool llevel,rlevel;
  
  if(lpwm<0) llevel=HIGH; 
  else llevel=LOW; 
  if(rpwm<0) rlevel=HIGH; 
  else rlevel=LOW; 
  analogWrite(D1, abs(lpwm));
  analogWrite(D2, abs(rpwm));
  digitalWrite(D3, !llevel);
  digitalWrite(D4, rlevel);
}


void cmdvel( int vel_x, int vel_th){
    double right_vel = 0.0;
    double left_vel = 0.0;

    // turning
    if(vel_x == 0){  
        right_vel = vel_th * WheelSeparation / 2.0;
        left_vel = (-1) * right_vel;
    }
    // forward / backward
    else if(vel_th == 0){ 
        left_vel = right_vel = vel_x;
    }
    // moving doing arcs
    else{ 
        left_vel = vel_x - vel_th * WheelSeparation / 2.0;
        right_vel = vel_x + vel_th * WheelSeparation / 2.0;
    }
    motion(left_vel,right_vel);

#if DEBUG
    printf("cmdvel: %f,%f\n",left_vel,right_vel);
#endif
}

void setup() {
  Serial.begin(115200);

  pinMode(D1, OUTPUT); // 1,2EN aka D1 pwm left
  pinMode(D2, OUTPUT); // 3,4EN aka D2 pwm right

  analogWriteFreq(15000);
  
  pinMode(D3, OUTPUT); // 1A,2A aka D3
  pinMode(D4, OUTPUT); // 3A,4A aka D4

  motion(-1000,1000);
  delay(200);
  motion(1000,-1000);
  delay(200);
  motion(-1000,1000);
  delay(200);
  motion(1000,-1000);
  delay(200);
  motion(0,-0);
}

#define COMMAND_RATE 10 //hz
#define SENSOR_RATE 10 //hz
#define LED_RATE 30 //hz
#define DEBUG_RATE 5

char token;
#define CMD_LEN 20
char *lastCmd = new char[CMD_LEN];
char *newCmd = new char[CMD_LEN];

int lvel,avel;

void loop() {

  static unsigned long prev_sensor_time = 0;
  static unsigned long prev_command_time = 0;
  static unsigned long prev_led_time = 0;


  if ((millis() - prev_sensor_time) >= (1000 / SENSOR_RATE))
  {
    prev_sensor_time = millis();
  }

  if (Serial.available() && (millis() - prev_command_time) >= (1000 / COMMAND_RATE))
  {
    token = Serial.read();

    switch (token) {
      case 'm'://m:100,100,\n 
      {
        //motor command: linear , angular
        String inBuffer = Serial.readStringUntil('\n');
        strcpy(newCmd, &inBuffer[1]);
        lvel = atoi(strtok(newCmd, ","));
        avel = atoi(strtok(NULL, ","));
        cmdvel(lvel,avel);
#ifdef DEBUG
        printf("linear vel=\t%d\tangular vel=\t%d\n",lvel,avel);
#endif
        break;
      }
      default: { 
        break;
      }
    }
    
    prev_command_time = millis();
  }

  if ((millis() - prev_led_time) >= (1000 / LED_RATE))
  { 
    //if (ledCmd > 0)
    {
      //showLed(prev_led_time % 256, (255 - prev_led_time % 256));
    }
    prev_led_time = millis();
  }

}
