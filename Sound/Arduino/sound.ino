#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

#define PIN 6

Adafruit_NeoPixel strip = Adafruit_NeoPixel(64, PIN, NEO_GRB + NEO_KHZ800);

long previousMillis = 0;        // will store last time LED was updated
float interval = 16.67;
uint8_t intervalRainbow = 200;
int break1 = round(strip.numPixels()/ 3);
int break2 = (round(strip.numPixels()/ 3) - 1)  * 2;
int break1middle = round(strip.numPixels() / 2 / 3);
int break2middle = (round(strip.numPixels() / 2 / 3) - 1)  * 2;

void setup() {
    Serial.begin(9600);
    // This is for Trinket 5V 16MHz, you can remove these three lines if you are not using a Trinket
    #if defined (__AVR_ATtiny85__)
        if (F_CPU == 16000000) clock_prescale_set(clock_div_1);
    #endif
    // End of trinket special code
    strip.begin();
    strip.show(); // Initialize all pixels to 'off'
    // pinMode(11, OUTPUT);
    // pinMode(3, OUTPUT);
    // pinMode(5, OUTPUT);
    // pinMode(6, OUTPUT);
    // pinMode(9, OUTPUT);
    // pinMode(10, OUTPUT);
    
}

void loop() {
    float currentMillis = millis();
    if (Serial.available() > 0){
        if(currentMillis - previousMillis > interval) {
            previousMillis = currentMillis;     
            uint16_t sound = Serial.read(); 
            colorWipe(sound); 
        }
    }
    // else{
    //     rainbowCycle(intervalRainbow);
    // }
}

void colorWipe(uint16_t sound) {
    strip.clear();
    for(uint16_t i=0; i<sound; i++) {
        // strip.setPixelColor(i, strip.Color(0, 255, 0));
        if(i < break1){
            strip.setPixelColor(i, strip.Color(0, 255, 0));
        }
        if (i >= break1)
        {
            strip.setPixelColor(i, strip.Color(255, 255, 0));
        }
        if(i >= break2 ){
           strip.setPixelColor(i, strip.Color(255, 0, 0));
        }
        
        
    }
    strip.show();
}

// Slightly different, this makes the rainbow equally distributed throughout
void rainbowCycle(uint8_t wait) {
  uint16_t i, j;

  for (j = 0; j < 256 * 5; j++)
  { // 5 cycles of all colors on wheel
      for (i = 0; i < strip.numPixels(); i++)
      {
          strip.setPixelColor(i, Wheel(((i * 256 / strip.numPixels()) + j) & 255));
      }
      strip.show();
      delay(1);
  }
}

// Input a value 0 to 255 to get a color value.
// The colours are a transition r - g - b - back to r.
uint32_t Wheel(byte WheelPos) {
  WheelPos = 255 - WheelPos;
  if(WheelPos < 85) {
    return strip.Color(255 - WheelPos * 3, 0, WheelPos * 3);
  }
  if(WheelPos < 170) {
    WheelPos -= 85;
    return strip.Color(0, WheelPos * 3, 255 - WheelPos * 3);
  }
  WheelPos -= 170;
  return strip.Color(WheelPos * 3, 255 - WheelPos * 3, 0);
}