#include <DHT.h>  // Including library for dht 
#include <ESP8266WiFi.h>

const char *ssid =  "DIGI-T53k";    
const char *pass =  "TF359U9k";

const uint16_t port = 50100;
const char *host = "192.168.100.44";
 
//#define DHTPIN 2     
 
//DHT dht(DHTPIN, DHT11);
 
WiFiClient client;
 
void setup() 
      {
      Serial.begin(115200);
      delay(10);
      //dht.begin();
      
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
  /*
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
        Serial.println();+
        Serial.print("Humidity: ");
        Serial.print(h);
        Serial.println();
        String temp = "";
        temp.concat(t);
        client.print(temp);
      }
   */
   if( client.available()){
     char input = client.read();
 
     if( input == 'S' ){
        char r;
        char p;
        char m;
        char command[14];
        client.read();
        if(client.available())
        {
          r = client.read();
        }
        if(client.available())
        {
          p = client.read();
        }
        else{
          p = ' ';
        }
        if(client.available())
        {
          m = client.read();
        }
        else{
          m = ' ';
        }
        
        command[0] = 'b';
        command[1] = '\'';
        command[2] = 'S';
        command[3] = 'T';
        command[4] = 'A';
        command[5] = 'R';
        command[6] = 'T';
        command[7] = ' ';
        command[8] = '+';
        command[9] = ' ';
        command[10] = r;
        command[11] = p;
        command[12] = m;
        command[13] = '\'';
        command[14] = '\0';
        Serial.println(command);
     }
     if( input == 'X' )
        Serial.println("b'STOP'");

   }
   delay(1000);
 
}
