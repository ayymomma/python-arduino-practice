/* Controlul unui motor BLDC utilizand arduino.
 * Viteza motorului BLDC este controlata extern de la potentiometru sau intern de la interfata de control.
 * Implementeaza cele doua moduri de control AUTOMAT si MANUAL
 * Cod adaptat dupa resursa [13] din documentatia proiectului de licenta
 */
#define PWM_MAX_DUTY      255
#define PWM_MIN_DUTY      50
#define PWM_START_DUTY    100
 
byte bldc_step = 0, motor_speed, pin_state;

void setup() {
  Serial.begin(115200);
  //Serial.println("Type Command (START, STOP)");
  DDRD  |= 0xE0;  // configurarea pinilor 5, 6 si 7 ca pini de output 
  PORTD  = 0x00;
  DDRB  |= 0x0E;  // configurarea pinilor 9, 10 si 11 ca pini de output
  PORTB  = 0x31;
  //setarea timer1 (fara prescaling) 
  TCCR1A = 0;
  TCCR1B = 0x01;
  //setarea timer2 (fara prescaling)
  TCCR2A = 0;
  TCCR2B = 0x01;
  //configurarea modulului ADC
  ADMUX  = 0x60;   // selectarea canalului 0 pentru ADC
  ADCSRA = 0x84;   // ADC clock = 1MHz
 
  PCICR  = EIMSK = 0;  // disable all external interrupts
  pinMode(2, INPUT_PULLUP);
  pinMode(3, INPUT_PULLUP);
  pinMode(4, INPUT_PULLUP);
}
// intrerupere schimbare pe pinul 2 (PCINT2) ISR
ISR (PCINT2_vect)
{
  if( (PIND & PCMSK2) != pin_state )
    return;
  // decuplam semnalul de BEMF
  for(byte i = 0; i < 20; i++)
  {
    if(bldc_step & 1){
      if(PIND & PCMSK2)     i -= 1;
    }
    else {
      if(!(PIND & PCMSK2))  i -= 1;
    }
  }
  bldc_move();
  bldc_step++;
  bldc_step %= 6;
}
 
// functia de comutatie pentru motorul BLDC
//Comutatie in 6 pasi, respectiv
/* H  L Dec
   A  B  C
   A  C  B
   B  C  A
   B  A  C
   C  A  B
   C  B  A
*/
void bldc_move()
{
  switch(bldc_step)
  {
    case 0:
      AH_BL();
      BEMF_C_FALLING();
      break;
    case 1:
      AH_CL();
      BEMF_B_RISING();
      break;
    case 2:
      BH_CL();
      BEMF_A_FALLING();
      break;
    case 3:
      BH_AL();
      BEMF_C_RISING();
      break;
    case 4:
      CH_AL();
      BEMF_B_FALLING();
      break;
    case 5:
      CH_BL();
      BEMF_A_RISING();
  }
}
void BEMF_A_RISING()
{
  //activeaza intreruperile pentru pinul 2(PCINT18), celelalte sunt dezactivate
  PCMSK2 = 0x04;    
  pin_state = 0x04;
}
void BEMF_A_FALLING()
{
  //activeaza intreruperile pentru pinul 2(PCINT18), celelalte sunt dezactivate
  PCMSK2 = 0x04;    
  pin_state = 0;
}
void BEMF_B_RISING()
{
  //activeaza intreruperile pentru pinul 3(PCINT19), celelalte sunt dezactivate
  PCMSK2 = 0x08;    
  pin_state = 0x08;
}
void BEMF_B_FALLING()
{
  //activeaza intreruperile pentru pinul 3(PCINT19), celelalte sunt dezactivate
  PCMSK2 = 0x08;    
  pin_state = 0;
}
void BEMF_C_RISING()
{
  //activeaza intreruperile pentru pinul 4(PCINT20), celelalte sunt dezactivate
  PCMSK2 = 0x10;    
  pin_state = 0x10;
}
void BEMF_C_FALLING()
{
  //activeaza intreruperile pentru pinul 4(PCINT20), celelalte sunt dezactivate
  PCMSK2 = 0x10;  
  pin_state = 0;
}
 
void AH_BL()
{
  //PWM ON pe pinul 11 (9 si 10 nu genereaza PWM)
  PORTD &= ~0xA0;
  PORTD |=  0x40;
  TCCR1A =  0;      
  TCCR2A =  0x81;   
}
void AH_CL()
{
  //PWM ON pe pinul 11 (9 si 10 nu genereaza PWM)
  PORTD &= ~0xC0;
  PORTD |=  0x20;
  TCCR1A =  0;      
  TCCR2A =  0x81;   
}
void BH_CL()
{
  //PWM ON pe pinul 10 (9 si 11 nu genereaza PWM)
  PORTD &= ~0xC0;
  PORTD |=  0x20;
  TCCR2A =  0;      
  TCCR1A =  0x21;    
}
void BH_AL()
{
  //PWM ON pe pinul 10 (9 si 11 nu genereaza PWM)
  PORTD &= ~0x60;
  PORTD |=  0x80;
  TCCR2A =  0;     
  TCCR1A =  0x21;   
}
void CH_AL()
{
  //PWM ON pe pinul 9 (10 si 11 nu genereaza PWM)
  PORTD &= ~0x60;
  PORTD |=  0x80;
  TCCR2A =  0;       
  TCCR1A =  0x81;   
}
void CH_BL()
{
  //PWM ON pe pinul 9 (10 si 11 nu genereaza PWM)
  PORTD &= ~0xA0;
  PORTD |=  0x40;
  TCCR2A =  0;       
  TCCR1A =  0x81;   
}
 
void SET_PWM_DUTY(byte duty)
{
  OCR1A  = duty;  // set PWM pentru pinul 9
  OCR1B  = duty;  // set PWM pentru pinul 10
  OCR2A  = duty;  // set PWM oentru pinul 11
}
void stop()
{
  while(1);
}
void loop() {
  if (Serial.available()) 
  {
      String command = Serial.readStringUntil('+');
      String command_viteza = Serial.readStringUntil('\n');
      command.replace("b"," ");
      command.replace("'"," ");
      command_viteza.replace("b"," ");
      command_viteza.replace("'"," ");
      command.trim();
      command_viteza.trim();
      Serial.println(command);
      Serial.println(command_viteza);

      if (command.equals("START"))
      {
        Serial.println("Am intrat pe ramura de comanda manuala!");
        SET_PWM_DUTY(PWM_START_DUTY);
        int i = 5000;
        // motor start
        while(i > 100)
        {
          delayMicroseconds(i);
          bldc_move();
          bldc_step++;
          bldc_step %= 6;
          i = i - 20;
        }
        motor_speed = PWM_START_DUTY;
        PCICR  = 4;
        int viteza = command_viteza.toInt();
        Serial.println(viteza);
        while(1)
        { 
          if(motor_speed < PWM_MIN_DUTY)
            motor_speed = PWM_MIN_DUTY;
          SET_PWM_DUTY(viteza);
          if (Serial.available()) 
          {
              String command = Serial.readStringUntil('\n');
              command.replace("b"," ");
              command.replace("'"," ");
              command.trim();
              Serial.println(command);
              if (command.equals("STOP"))
              {
                 Serial.println("Am intrat pe ramura cu stop_manual");
                 exit(0);
              }
          }
        }
      }
  }
}
