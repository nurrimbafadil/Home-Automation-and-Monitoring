/*
Developed by @nurrimbafadil
Arduino PubSub Library is need to add.
Download from: https://github.com/knolleary/pubsubclient
*/

#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// Update these with values suitable for your network.

const char* ssid = "..............";
const char* password = "...........";
const char* mqtt_server = "mqtt.eclipse.org";

int light = 0; 
int fan = 2;

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;

void setup_wifi() {

  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  // Switch on the LED if an 1 was received as first character
  if ((char)payload[0] == '1') {
    digitalWrite(light, HIGH);   // Turn the LED on (Note that LOW is the voltage level
    Serial.print("Light on");
    // but actually the LED is on; this is because
    // it is active low on the ESP-01)
  }
  else if ((char)payload[0] == '2') {
    digitalWrite(light, LOW);   // Turn the LED on (Note that LOW is the voltage level
    Serial.print("Light off");
    // but actually the LED is on; this is because
    // it is active low on the ESP-01)
  }
  else if ((char)payload[0] == '3') {
    digitalWrite(fan, HIGH);   // Turn the LED on (Note that LOW is the voltage level
    Serial.print("Fan on");
    // but actually the LED is on; this is because
    // it is active low on the ESP-01)
  }
  else if ((char)payload[0] == '4') {
    digitalWrite(fan, LOW);   // Turn the LED on (Note that LOW is the voltage level
    Serial.print("Fan off");
    // but actually the LED is on; this is because
    // it is active low on the ESP-01)
  }

}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      client.publish("outTopic", "hello world");
      // ... and resubscribe
      client.subscribe("onsemi/light");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void setup() {
  pinMode(light, OUTPUT);     // Initialize the BUILTIN_LED pin as an output
  pinMode(fan, OUTPUT);     // Initialize the BUILTIN_LED pin as an output
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void loop() {

  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}
