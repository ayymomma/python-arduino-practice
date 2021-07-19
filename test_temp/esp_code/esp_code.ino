#include <DHT.h>  // Including library for dht 
#include <ESP8266WiFi.h>

//const char *ssid =  "DIGI-T53k";    
//const char *pass =  "TF359U9k";
const char *ssid = "ureche";
const char *pass = "qwerty123";

//const uint16_t port = 50100;
//const char *host = "192.168.100.44";
const uint16_t port = 50100;
const char *host = "192.168.43.198";

char test_case = '0';
 
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

        if(client.available()){
          test_case = client.read();
        }
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


   if(test_case == '1'){
      float h = dht.readHumidity();
      float t = dht.readTemperature();

      if (isnan(h) || isnan(t)) 
         {
             client.print("Failed to read from DHT sensor!");
             delay(1000);
         }
      else{
        char tt[10];
        char hh[10];

        dtostrf(t, 2, 2, tt);
        dtostrf(h, 2, 2, hh);
        String s1 = "T=";
        String s2 = " ";
        String s3 = "H=";
        client.print(s1 + t + s2 + s3 + h);
      }
      
   }
   delay(1000);
 
}
