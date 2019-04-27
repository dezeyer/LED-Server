#include settings.h
#define FASTLED_ALLOW_INTERRUPTS 0
//#define FASTLED_INTERRUPT_RETRY_COUNT 0
#define WEBSOCKETS_NETWORK_TYPE NETWORK_ESP8266_ASYNC

#include <FastLED.h>
#include <ESP8266WiFi.h>
#include <ArduinoJson.h>
#include <WiFiUdp.h>

#define MILLI_AMPS         2000 // IMPORTANT: set the max milli-Amps of your power supply (4A = 4000mA)
#define FRAMES_PER_SECOND  120  // here you can control the speed. With the Access Point / Web Server the animations run a bit slower.


CRGB leds[NUM_LEDS];
 

WiFiUDP Udp;
unsigned int localUdpPort = 4210;  // local port to listen on
char incomingPacket[255];  // buffer for incoming packets

WiFiClient client;

void setup() {
  //Serial.begin(115200);
  FastLED.addLeds<LED_TYPE, DATA_PIN, COLOR_ORDER>(leds, NUM_LEDS);         // for WS2812 (Neopixel)
  //FastLED.addLeds<LED_TYPE,DATA_PIN,CLK_PIN,COLOR_ORDER>(leds, NUM_LEDS); // for APA102 (Dotstar)
  FastLED.setDither(false);
  FastLED.setCorrection(TypicalLEDStrip);
  FastLED.setBrightness(255);
  FastLED.setMaxPowerInVoltsAndMilliamps(5, MILLI_AMPS);
  fill_solid(leds, NUM_LEDS, CRGB::Black);
  FastLED.show();
  
  Udp.begin(localUdpPort);
}
 
void loop() {
  EVERY_N_MILLISECONDS( 15 ) { 
    if (WiFi.status() != WL_CONNECTED) { // FIX FOR USING 2.3.0 CORE (only .begin if not connected)
      WiFi.begin(ssid, password); // connect to the network
      while (WiFi.status() != WL_CONNECTED) {
        delay(500);
      }
    }

    //Kompletter Strip in einer farbe
    //for future use, when ws1812b strips are usable.
    //int root_length = root.size(); 
    //for(int i=0; i<root_length;i++){
    //  leds[i].r = root["data"][String(i)]["red"]; // 0
    //  leds[i].g = root["data"][String(i)]["green"]; // 0
    //  leds[i].b = root["data"][String(i)]["blue"]; // 0
    //}
    
  }

  int packetSize = Udp.parsePacket();
  if (packetSize){
    int len = Udp.read(incomingPacket, 255);
    if (len > 0)
    {
      incomingPacket[len] = 0;
    }
    Serial.printf("UDP packet contents: %s\n", incomingPacket);

    // send back a reply, to the IP address and port we got the packet from
    Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
    Udp.write(replyPacket);
    Udp.endPacket();
  }

  fill_solid( leds, NUM_LEDS, CRGB( red, green, blue) );
  FastLED.show();
  
  
}
void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {

  switch(type) {
    case WStype_DISCONNECTED:
      //USE_SERIAL.printf("[WSc] Disconnected!\n");
      break;
    case WStype_CONNECTED: {
      //USE_SERIAL.printf("[WSc] Connected to url: %s\n", payload);

      // send message to server when Connected
      webSocket.sendTXT("{\"register_client_type\":1,\"client_name\":\"wemosd1\"}");
    }
      break;
    case WStype_TEXT:
      //USE_SERIAL.printf("[WSc] get text: %s\n", payload);
      JsonObject& root = jsonBuffer.parseObject(payload);
      if (!root.success()) {
        jsonBuffer.clear();
      }else{
        red = root["data"]["0"]["red"];
        green = root["data"]["0"]["green"];
        blue = root["data"]["0"]["blue"];
      }
      // send message to server
      // webSocket.sendTXT("message here");
      break;
  }

}
 
