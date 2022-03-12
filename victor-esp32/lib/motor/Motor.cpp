#include "Motor.h"
#include "analogWrite.h"

Motor::Motor(driver motor_driver, int counts_per_rev, int pwm_pin, int motor_pinA, int motor_pinB)
{
    motor_driver_ = motor_driver;
    counts_per_rev_ = counts_per_rev;

    pwm_pin_ = pwm_pin;
    motor_pinA_ = motor_pinA;
    motor_pinB_ = motor_pinB;
    
    analogWriteResolution(motor_pinA_, 8);
    analogWriteFrequency(motor_pinA_,30000);
    analogWriteResolution(motor_pinB_, 8);
    analogWriteFrequency(motor_pinB_,30000);
    
    analogWrite(motor_pinA_, 0);
    analogWrite(motor_pinB_, 0);

}

void Motor::updateSpeed(long encoder_ticks)
{
    //this function calculates the motor's RPM based on encoder ticks and delta time
    unsigned long current_time = millis();
    unsigned long dt = current_time - prev_update_time_;

    //convert the time from milliseconds to minutes
    double dtm = (double)dt / 60000;
    double delta_ticks = encoder_ticks - prev_encoder_ticks_;

    //calculate wheel's speed (RPM)
    rpm_ = (delta_ticks / counts_per_rev_) / dtm;

    prev_update_time_ = current_time;
    prev_encoder_ticks_ = encoder_ticks;
}

int Motor::getRPM()
{
    return rpm_;
}

void Motor::spin(int pwm)
{
    if (pwm > 0)
    {
        analogWrite(motor_pinA_, 0);
        analogWrite(motor_pinB_, abs(pwm));
    }
    else if (pwm < 0)
    {
        analogWrite(motor_pinB_, 0);
        analogWrite(motor_pinA_, abs(pwm));
    }
    else
    {
        analogWrite(motor_pinB_, 0);
        analogWrite(motor_pinA_, 0);
    }
}
