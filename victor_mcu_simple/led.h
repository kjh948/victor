#include <WS2812FX.h>

#define LED_COUNT 19
#define LED_PIN D8

#define TIMER_MS 5000

WS2812FX ws2812fx = WS2812FX(LED_COUNT, LED_PIN, NEO_RGB + NEO_KHZ800);

unsigned long last_change = 0;
unsigned long now = 0;


#define BLINK_PER_MINUTE 10
#define MS_PER_BLINK (60000 / BLINK_PER_MINUTE)
#define SECOND_BLINK (MS_PER_BLINK*0.1 )

#define LEFT_LED 10
#define RIGHT_LED 8



uint16_t eyeBlink(void) {
  static unsigned long lastTime = 0;
  static bool secondBlinkActive = false;
  static bool firstBlinkActive = false;

  WS2812FX::Segment* seg = ws2812fx.getSegment(); // get the current segment

  unsigned long blinkTimer = millis() - lastTime;
  if ((blinkTimer > SECOND_BLINK) && !secondBlinkActive) { // time for the second beat?
    ws2812fx.setPixelColor(LEFT_LED, 0);
    ws2812fx.setPixelColor(RIGHT_LED, 0);
    secondBlinkActive = true;
  }
  if (blinkTimer > MS_PER_BLINK) {
    ws2812fx.setPixelColor(LEFT_LED, 0x007BFF);
    ws2812fx.setPixelColor(RIGHT_LED, 0x007BFF);
    secondBlinkActive = false;
    lastTime = millis();
    //ws2812fx.setCycle();
  }

  return seg->speed; // return the delay until the next animation step (in msec)
}

uint16_t myCustomEffect(void) { // random chase
  WS2812FX::Segment* seg = ws2812fx.getSegment(); // get the current segment
  for(uint16_t i=seg->stop; i>seg->start; i--) {
    ws2812fx.setPixelColor(i, ws2812fx.getPixelColor(i-1));
  }
  ws2812fx.setPixelColor(seg->start, 0x007BFF);
  return seg->speed; // return the delay until the next animation step (in msec)
}

void ledOff()
{
  for(uint16_t i=0; i<LED_COUNT; i++) ws2812fx.setPixelColor(i,0);
}

void ledBlink()
{
  ledOff();
  ws2812fx.setCustomMode(eyeBlink);   
  ws2812fx.setSegment(0, 7, 12, FX_MODE_CUSTOM, 0x007BFF, 1000, false);
}

void ledZcar()
{
  ledOff();
  ws2812fx.setSegment(0, 7, 12, 43,0x007BFF, 1000, false);
}

void ledMoveforward()
{
  ledOff();
  ws2812fx.setSegment(0, 0, 8, 18, 0x001BFF, 500, REVERSE);
  ws2812fx.setSegment(1, 9, 19, 18,0x001BFF, 500, false);
}
void ledTurnleft()
{
  ledOff();
  ws2812fx.setSegment(0, 0, LED_COUNT-1, 18, 0x001B1B, 500, false);
}

void ledTurnright()
{
  ledOff();
  ws2812fx.setSegment(0, 0, LED_COUNT-1, 18, 0x001B1B, 500, REVERSE);
}



void initLED()
{
  ws2812fx.init();
  ws2812fx.setBrightness(150);
  ws2812fx.setSpeed(1000);
  ws2812fx.setColor(0);
  ws2812fx.start();
}

void setLED(int cmd)
{
  static int pat=0;
  
  now = millis();
  ws2812fx.service();

  if (now - last_change > TIMER_MS) {

    ledBlink();
//    ledTurnleft();
//    if(pat%2==0) 
//    {
//      ledBlink();
//      printf("Blink\n");
//    }
//    if(pat%2==1) 
//    {
//      ledZcar();
//      printf("Zcar\n");
//    }
//    
//#ifdef DEBUG
//      printf("pattern=\t%d\n",pat%2);
//#endif
//    pat++;
    last_change = now;
  }
}
