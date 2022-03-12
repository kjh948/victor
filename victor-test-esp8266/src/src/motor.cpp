/**********************************************************************************************
 * Arduino PID Library - Version 1.2.1
 * by Brett Beauregard <br3ttb@gmail.com> brettbeauregard.com
 *
 * This Library is licensed under the MIT License
 **********************************************************************************************/

#if ARDUINO >= 100
  #include "Arduino.h"
#else
  #include "WProgram.h"
#endif

#include "motor.h"

#include "lib/PID_V1/PID_v1.h"  

#include "ESP8266TimerInterrupt.h"

#define DEBUG 0

#define TIMER_INTERVAL_MS       1000

// Init ESP8266 timer 1
ESP8266Timer ITimer;

typedef struct
{
  int32_t  counter;

  int32_t  speed;
  int32_t  start_counter;  
  
  double   pwm_out;

  uint8_t  enc_pin[2];
  uint8_t  mot_pin[2];

  int8_t   mot_dir;

  // PID
  double enc_speed;
  double goal_speed;
  double pwm_output;
  PID   *p_pid;  
} motor_cfg_t;


motor_cfg_t motor_cfg[2];


static void motorEncoderLeftISR(void);
static void motorEncoderRightISR(void);
static void motorEncoderUpdate(uint8_t ch);
static void motorUpdateISR(void);





void motorBegin(void)
{
  motor_cfg[L_MOTOR].mot_dir    =-1;  // 1 or -1
  motor_cfg[L_MOTOR].enc_pin[0] = D5;  // Interrupt Pin
  motor_cfg[L_MOTOR].enc_pin[1] = D6;
  motor_cfg[L_MOTOR].mot_pin[0] = D1;
  motor_cfg[L_MOTOR].mot_pin[1] = D3;
  
  
  motor_cfg[R_MOTOR].mot_dir    = 1;  // 1 or -1
  motor_cfg[R_MOTOR].enc_pin[0] = D7;  // Interrupt Pin
  motor_cfg[R_MOTOR].enc_pin[1] = D8;
  motor_cfg[R_MOTOR].mot_pin[0] = D2;
  motor_cfg[R_MOTOR].mot_pin[1] = D4;  

  analogWriteFreq(15000);
  
  for (int i=0; i<2; i++)
  {
    motor_cfg[i].counter = 0;
    motor_cfg[i].speed   = 0;
    motor_cfg[i].pwm_out = 0;
    motor_cfg[i].p_pid   = new PID(&motor_cfg[i].enc_speed, &motor_cfg[i].pwm_output, &motor_cfg[i].goal_speed, 30, 20, 0, DIRECT);
    motor_cfg[i].start_counter = 0;

    pinMode(motor_cfg[i].enc_pin[0], INPUT_PULLUP);
    pinMode(motor_cfg[i].enc_pin[1], INPUT_PULLUP);      

    analogWrite(motor_cfg[i].mot_pin[0], 0);
    //analogWrite(motor_cfg[i].mot_pin[1], 0);   
    
    motor_cfg[i].p_pid->SetSampleTime(10);
    motor_cfg[i].p_pid->SetOutputLimits(-255, 255);
    motor_cfg[i].p_pid->SetMode(AUTOMATIC);    
  }  

  //attachInterrupt(digitalPinToInterrupt(motor_cfg[L_MOTOR].enc_pin[0]), motorEncoderLeftISR, CHANGE);
  //attachInterrupt(digitalPinToInterrupt(motor_cfg[R_MOTOR].enc_pin[0]), motorEncoderRightISR, CHANGE);


  
  ITimer.attachInterruptInterval(TIMER_INTERVAL_MS * 10, motorUpdateISR);


}

int32_t motorGetSpeed(uint8_t ch)
{
  return motor_cfg[ch].speed;
}

int32_t motorGetCounter(uint8_t ch)
{
  return motor_cfg[ch].counter;
}

int32_t motorGetGoalSpeed(uint8_t ch)
{
  return (int32_t)motor_cfg[ch].goal_speed;
}

void motorSetSpeed(uint8_t ch, int16_t speed)
{
  motor_cfg[ch].goal_speed = (double)speed;
}

void motorMoveSpeed(int16_t left_speed, int16_t right_speed)
{
  motor_cfg[L_MOTOR].goal_speed = (double)left_speed;
  motor_cfg[R_MOTOR].goal_speed = (double)right_speed;
}


void motorSetPwm(uint8_t ch, int16_t pwm_data )
{
  uint16_t pwm_out;

  if (pwm_data >= 0)
  {
    pwm_out = pwm_data;
    analogWrite(motor_cfg[ch].mot_pin[0], pwm_out);
    digitalWrite(motor_cfg[ch].mot_pin[1], 0);     
  }
  else
  {
    pwm_out = -pwm_data;
    analogWrite(motor_cfg[ch].mot_pin[0], pwm_out);
    digitalWrite(motor_cfg[ch].mot_pin[1], 1);         
  }  
}

// Motor Update
//
void IRAM_ATTR motorUpdateISR(void)
{
  for (int i=0; i<2; i++)
  {
    motor_cfg[i].speed = motor_cfg[i].counter - motor_cfg[i].start_counter;
    motor_cfg[i].start_counter = motor_cfg[i].counter;
    motor_cfg[i].enc_speed = (double)motor_cfg[i].speed;

    if (motor_cfg[i].p_pid->ComputeISR())
    {
      if (motor_cfg[i].goal_speed == 0)
      {
        motorSetPwm(i, 0);
      }
      else
      {
        motorSetPwm(i, (int16_t)motor_cfg[i].pwm_output);
      }
    }      
  }
#if (DEBUG > 0)
  static int lastMillis;
  Serial.println("Delta ms = " + String(millis() - lastMillis));
  lastMillis = millis();
#endif
}

void motorEncoderLeftISR(void)
{
  motorEncoderUpdate(L_MOTOR);
}

void motorEncoderRightISR(void)
{
  motorEncoderUpdate(R_MOTOR);
}

void motorEncoderUpdate(uint8_t ch)
{
  uint8_t enc_bit = 0;
  
  if (digitalRead(motor_cfg[ch].enc_pin[0]) == HIGH)
  {
    enc_bit |= (1<<0);
  }
  if (digitalRead(motor_cfg[ch].enc_pin[1]) == HIGH)
  {
    enc_bit |= (1<<1);
  }

  switch(enc_bit)
  {
    case 0x01:
    case 0x02:
      motor_cfg[ch].counter -= motor_cfg[ch].mot_dir;
      break;

    default:
      motor_cfg[ch].counter += motor_cfg[ch].mot_dir;
      break;
  }  
}