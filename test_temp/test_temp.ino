#include <DHT.h>  // Including library for dht 
#include <ESP8266WiFi.h>

const char *ssid =  "DIGI-T53k";    
const char *pass =  "TF359U9k";

const uint16_t port = 50100;
const char *host = "192.168.100.44";
 
#define DHTPIN 2     
 
DHT dht(DHTPIN, DHT11);
 
WiFiClient client;
 
void setup() 
{
       Serial.begin(115200);
       delay(10);
       dht.begin();
       
       Serial.println("Connecting to ");
       Serial.println(ssid);
       
       WiFi.begin(ssid, pass);
 
      while (WiFi.status() != WL_CONNECTED) 
     {
            delay(500);
            Serial.print(".");
     }
     
      Serial.println("");
      Serial.println("WiFi connected");

      
      if(!client.connect(host, port)){
        Serial.println("Connection failed!");
        delay(1000);
        return;
      }
 
}
 
void loop() 
{
        if( client.read() == 97)
        {
          float h = dht.readHumidity();
          float t = dht.readTemperature();
          
          if (isnan(h) || isnan(t)) 
             {
                 Serial.println("Failed to read from DHT sensor!");
                 delay(1000);
                 //return;
             }
          if( t > 0 )
          {
            Serial.print("Temperature: ");
            Serial.print(t);
            Serial.println();
            Serial.print("Humidity: ");
            Serial.print(h);
            Serial.println();
            String temp = "";
            temp.concat(t);
            client.print(temp);
          }
        }
      delay(1000);
}
