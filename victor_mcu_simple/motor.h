

// Init constants and global variables
#define WheelSeparation  0.135                              // wheel separation in meters

void initMotor()
{
  pinMode(D1, OUTPUT); // 1,2EN aka D1 pwm left
  pinMode(D2, OUTPUT); // 3,4EN aka D2 pwm right
  pinMode(D3, OUTPUT); // 1A,2A aka D3
  pinMode(D4, OUTPUT); // 3A,4A aka D4

  analogWriteFreq(15000);
}

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
