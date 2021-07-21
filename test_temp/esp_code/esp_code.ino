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
        
        String s2 = "";
        
        if(client.available()){
          test_case = client.read();
        }
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

        String s1 = "b'START + ";

        
        if(r != ' ')
          s2 = s2 + r;
        if(p != ' ')
          s2 = s2 + p;
        if(m != ' ')
          s2 = s2 + m;

        String s3 = "'";
        Serial.println(s1 + s2 + s3);
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
