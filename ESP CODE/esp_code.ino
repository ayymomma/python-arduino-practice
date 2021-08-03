#include <DHT.h>  // Including library for dht 
#include <ESP8266WiFi.h>

//const char *ssid =  "DIGI-T53k";    
//const char *pass =  "TF359U9k";
const char *ssid = "ureche";
const char *pass = "qwerty123";

//const uint16_t port = 50100;
//const char *host = "192.168.100.44";
uint16_t port = 50100;
const char *host = "192.168.43.198";

char test_case = '0';
float voltage_value = 0.0;
String output = "";
#define DHTPIN 2
#define DHTPIN_MOTOR 14
#define ANALOGPIN A0
#define REDLED 16
#define GREENLED 0
#define ECHOPIN 15
#define TRIGPIN 13
#define SOUND_VELOCITY 0.034

long duration;
float distanceCm;
float maxDistance = 20.0;

DHT dht(DHTPIN, DHT11);
DHT dht_motor(DHTPIN_MOTOR, DHT11);
 
WiFiClient client;
 
void setup() 
      {
      Serial.begin(115200);
      delay(10);
      dht.begin();
      dht_motor.begin();

      pinMode(TRIGPIN, OUTPUT);
      pinMode(ECHOPIN, INPUT);

      pinMode(REDLED, OUTPUT);
      pinMode(GREENLED, OUTPUT);
      digitalWrite(REDLED, LOW);
      digitalWrite(GREENLED, LOW);
      
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
   if( client.available()){
     char input = client.read();
 
     if( input == 'S' ){
        digitalWrite(REDLED, LOW);
        digitalWrite(GREENLED, HIGH);
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
        stop_test();
     }

   }
   output = "";


   if(test_case == '1'){
    temperature_test();
    client.print(output);
   }
   if(test_case == '2'){
     voltage_test();
     client.print(output);
   }
   if(test_case == '3'){
     speed_test();
     client.print(output);
   }
   if(test_case == '4'){
     temperature_test();
     voltage_test();
     client.print(output);
   }
   if(test_case == '5'){
    voltage_test();
    speed_test();
    client.print(output);
   }
   if(test_case == '6'){
    temperature_test();
    voltage_test();
    speed_test();
    client.print(output);
   }

   if(test_case != '0')
   {
        digitalWrite(TRIGPIN, LOW);
        delayMicroseconds(2); 
        
        digitalWrite(TRIGPIN, HIGH);
        delayMicroseconds(10);
        digitalWrite(TRIGPIN, LOW);
        
        duration = pulseIn(ECHOPIN, HIGH);
        
        distanceCm = duration * SOUND_VELOCITY/2;
    
        Serial.print("Distance (cm): ");
        Serial.println(distanceCm);

        if(distanceCm < maxDistance){
          stop_test();
        }
   }
   delay(1000);
 
}
void stop_test(){
    digitalWrite(GREENLED, LOW);
    digitalWrite(REDLED, HIGH);
    Serial.println("b'STOP'");
    test_case = '0';
}

void temperature_test(){
    float h = dht.readHumidity();
    float t = dht.readTemperature();
    
    float mh = dht_motor.readHumidity();
    float mt = dht_motor.readTemperature();
    
    String s1 = "T=";
    String s2 = " ";
    String s3 = "H=";
    output = output + "T=" + String(t,2) + " H=" + String(h,2) + " T=" + String(mt,2) + " H=" + String(mh,2) + " ";
}

void voltage_test(){
    voltage_value = analogRead(ANALOGPIN);
    output = output + String(voltage_value, 2) + " ";
}

void speed_test(){
    output = output + "10000";
}
