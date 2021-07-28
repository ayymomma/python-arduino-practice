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
int voltage_value = 0;
 
#define DHTPIN 2
#define DHTPIN_MOTOR 14
#define ANALOGPIN A0
     
DHT dht(DHTPIN, DHT11);
DHT dht_motor(DHTPIN_MOTOR, DHT11);
 
WiFiClient client;
 
void setup() 
      {
      Serial.begin(115200);
      delay(10);
      dht.begin();
      dht_motor.begin();
      
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

        String motor_sens = "";
        motor_sens = client.read();
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
        String s4 = " + ";
        Serial.println(s1 + motor_sens + s4 + s2 + s3);
     }
     if( input == 'X' )
     {
        Serial.println("b'STOP'");
        test_case = '0';
     }

   }


   if(test_case == '1'){
      float h = dht.readHumidity();
      float t = dht.readTemperature();

      float mh = dht_motor.readHumidity();
      float mt = dht_motor.readTemperature();

      /*if (isnan(h) || isnan(t) || isnan(mh) || isnan(mt)) 
         {
             client.print("Failed to read from DHT sensor!");
             delay(1000);
         }
      else{*/
        
        String s1 = "T=";
        String s2 = " ";
        String s3 = "H=";
        client.print(s1 + t + s2 + s3 + h + s2 + s1 + mt + s2 + s3 + mh);
    // }
      
   }


   if(test_case == '2'){
       voltage_value = analogRead(ANALOGPIN);
       client.print(voltage_value);
   }
   
   delay(1000);
 
}
