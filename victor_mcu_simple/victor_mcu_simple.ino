#include <ESP8266WiFi.h>
#include <PID_v1.h>

#define DEBUG 1

#include "printf.h"
#include "led.h"
#include "motor.h"



void setup() {
  Serial.begin(115200);

  initMotor();
  initLED();
  
#if 0
  motion(-1000,1000);
  delay(200);
  motion(1000,-1000);
  delay(200);
  motion(-1000,1000);
  delay(200);
  motion(1000,-1000);
  delay(200);
  motion(0,-0);
#endif
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
    setLED(0);
    //if (ledCmd > 0)
    {
      //showLed(prev_led_time % 256, (255 - prev_led_time % 256));
    }
    prev_led_time = millis();
  }

}
