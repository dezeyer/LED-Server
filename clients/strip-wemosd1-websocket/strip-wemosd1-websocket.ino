
//#define FASTLED_ALLOW_INTERRUPTS 0
//#define FASTLED_INTERRUPT_RETRY_COUNT 0
//#define WEBSOCKETS_NETWORK_TYPE NETWORK_ESP8266_ASYNC
#define UDP_TX_PACKET_MAX_SIZE = 50*12+1;

#include <FastLED.h>
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

#include "settings.h"

CRGB leds[NUM_LEDS];

WiFiClient client;

// buffers for receiving and sending data
char packetBuffer[UDP_TX_PACKET_MAX_SIZE];
WiFiUDP Udp;

int c = -1;

void setup() {
  Serial.begin(115200);
  FastLED.addLeds<LED_TYPE, DATA_PIN, COLOR_ORDER>(leds, NUM_LEDS);         // for WS2812 (Neopixel)
  //FastLED.addLeds<LED_TYPE,DATA_PIN,CLK_PIN,COLOR_ORDER>(leds, NUM_LEDS); // for APA102 (Dotstar)
  FastLED.setDither(false);
  FastLED.setCorrection(TypicalLEDStrip);
  FastLED.setBrightness(255);
  FastLED.setMaxPowerInVoltsAndMilliamps(5, MILLI_AMPS);
  fill_solid(leds, NUM_LEDS, CRGB::Black);
  wdt_enable(WDTO_4S);   // Watchdog auf 4 s stellen
  FastLED.show();
  Udp.begin(random(5000,5500));
  
}
 
void loop() {
  EVERY_N_MILLISECONDS( 250 ) {
    sendUDP(String("s:ping"));
  }
  EVERY_N_MILLISECONDS( 15 ) { 
    wdt_reset();
    if (WiFi.status() != WL_CONNECTED) { // FIX FOR USING 2.3.0 CORE (only .begin if not connected)
      WiFi.begin(ssid, password); // connect to the network
      while (WiFi.status() != WL_CONNECTED) {
        delay(500);
      }
      if (WiFi.status() == WL_CONNECTED) {
        // Start UDP
        Serial.println("start udp");
        if(!overriderecipient){
          RecipientIP = WiFi.localIP();
          RecipientIP[3] = 255;
        }
      }
    }
    
  }
  int packetSize = Udp.parsePacket();
  if(packetSize)
  {
    // read the packet into packetBufffer
    Udp.read(packetBuffer,UDP_TX_PACKET_MAX_SIZE);
    if(packetBuffer[0] == 's' && packetBuffer[1] == 'r'){
      sendUDP("r:1:"+StripName+":"+String(NUM_LEDS)+":0");
    }
    if(packetBuffer[0] == 's' && packetBuffer[1] == 'u'){
        FastLED.show(); 
    }
    if(packetBuffer[0] == 'd'){
      c=1;
      while(c<strlen(packetBuffer)){
        leds[getledvalue(c)] = CRGB( getledvalue(c+3), getledvalue(c+6), getledvalue(c+9));
        c=c+12;
      }
    }
  }
}

int getledvalue(int startpoint){
  return 100 * int(packetBuffer[startpoint] - '0') + 10 * int(packetBuffer[startpoint+1] - '0') + int(packetBuffer[startpoint+2] - '0');
}
 
// Function to send UDP packets
void sendUDP(String text)
{
  //Serial.println(text);
  Udp.beginPacket(RecipientIP, RecipientPort);
  Udp.print(text);
  Udp.endPacket();
}
