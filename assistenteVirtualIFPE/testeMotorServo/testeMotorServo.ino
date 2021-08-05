#include <Servo.h> 
 
Servo myservo; // Cria objeto servo para controle (max. de 8 objetos)
 
int pos = 0; // Variavel para armazenar a posicao do servo motor
 
void setup() 
{ 
  myservo.attach(6); // Conectar servo motor no pino digital 6
} 
  
void loop() 
{ 
  for(pos = 0; pos < 90; pos += 1) // Vai de 0 a 90 graus em incrementos de 1 grau
  {                                   
    myservo.write(pos); // Manda o servo motor ir para a posicao "pos"
    delay(6); // Espera 6ms para o servo voltar para "pos" 
  } 
  
  for(pos = 90; pos>=1; pos-=1) // Vai de 90 graus para 0 
  {                                
    myservo.write(pos); // Manda o servo motor ir para a posicao "pos" 
    delay(6); // Espera 6ms para o servo voltar para "pos"
  } 
  
} 
