#define NUM_LEDS      150
#define DATA_PIN      D8
#define LED_TYPE      WS2811
#define COLOR_ORDER   GRB

#define MILLI_AMPS         2000 // IMPORTANT: set the max milli-Amps of your power supply (4A = 4000mA)
#define FRAMES_PER_SECOND  120  // here you can control the speed. With the Access Point / Web Server the animations run a bit slower.

String StripName = "Regal";

const char* ssid     = "zy-intern";
const char* password = "Rg>379rqQX$*h-Tx";

//RecipientIP is overridden after wl connect, getting localip and set last octet to 255 (Broadcast)
//this will only work for /24 networks. If you want to set an other BC or a sinle IP adress set overriderecipient to true
bool overriderecipient = false;
IPAddress RecipientIP = IPAddress(0, 0, 0, 0);

unsigned int RecipientPort = 8002;
