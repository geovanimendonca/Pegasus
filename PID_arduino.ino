//Sensor de temperatura usando o LM35
// A1 Sensor temperatura
// D3 Led2
// D6 Fan
// D9 Led1

#include <PID_v1.h>
#include <Thermistor.h>

Thermistor temp(1);

//Define Variables we'll be connecting to
double Setpoint, Input, Output;
int y=0;
//Specify the links and initial tuning parameters
double Kp = 10, Ki = 1, Kd = 1;

PID myPID(&Input, &Output, &Setpoint, Kp, Ki, Kd, P_ON_M, DIRECT);

unsigned long millisTarefa1 = millis();
unsigned long millisTarefa2 = millis();

//const int LM35 = A1; // Define o pino que lera a saída do LM35
const int aquecedor = 5;
double temperatura, temperatura_armazenada, temperatura_real, temperatura_serial; // Variável que armazenará a temperatura medida
const int fan = 6;
const int led = 9;
int amostras = 50;

//Função que será executada uma vez quando ligar ou resetar o Arduino
void setup() {

  Serial.begin(9600); // inicializa a comunicação serial
  pinMode(aquecedor, OUTPUT);
  pinMode(fan, OUTPUT);
  pinMode(led, OUTPUT);

  // Inicialização com aquecedor e fan desligados. Led sempre ligado.
  analogWrite(aquecedor, 0);
  analogWrite(fan, 0);
  analogWrite(led, 255);


  // Inicialização com setpoint baixo
  Setpoint = 47.7;

  // Ativa o PID e limita a saida
  myPID.SetMode(AUTOMATIC);
  myPID.SetOutputLimits(0,80);
}

//Função que será executada continuamente
void loop() {

  if (Serial.available()) {
    //Setpoint = Serial.readString().toInt(); // Serial do raspberry
    Setpoint = Serial.parseInt(); // Ler pela serial do arduino

    if (Setpoint > 100) { // Limita o setpoint lido
      Setpoint = 100;
    }
  }
  
  // Média de valores de temperatura (diminuir ruido)
  for ( int x = 0; x < amostras ; x++ ) {
    temperatura_real = temp.getTemp();
    temperatura_armazenada = temperatura_real + temperatura_armazenada;
  }

  temperatura = temperatura_armazenada / amostras;
  temperatura_armazenada = 0; // Zera a temperatura armazenada para o próximo loop
  Input = temperatura; // Input PID


  
  if (temperatura > 85) { Setpoint = 65 ;}


  
  // Redundancia limite de saida do PID
  if (Output < 80) {
    analogWrite(aquecedor, Output);
  }

 // if (temperatura > Setpoint + 5) {
 //   analogWrite(fan, 255);
 //   analogWrite(aquecedor, 0);
 //  } else {
 //    analogWrite(fan, 0);
 // }

  /*
    if (temperatura > Setpoint+1){
    analogWrite(fan, 255);
    analogWrite(aquecedor,0);
    } else if(temperatura > Setpoint){
    analogWrite(fan,0);
    analogWrite(aquecedor,0);
    } else {
    analogWrite(fan,0);
    }
 */

  
  
  if (temperatura < Setpoint-1){
    analogWrite(aquecedor, 80); 
  }
  if (Setpoint <40 && temperatura > Setpoint){
    analogWrite(fan,255);
  } else { analogWrite(fan,0);}
  
  // Print Serial
  if ((millis() - millisTarefa1) >= 1000) {
    millisTarefa1 = millis();
    Serial.print(temperatura);
    Serial.print(",");
    Serial.println(Setpoint);
    //Serial.print(",");
    //Serial.print(Output);   
    //Serial.print(",");
    //Serial.print(Kp);
    //Serial.print(",");
    //Serial.print(Ki);
    //Serial.print(",");
    //Serial.println(Kd);
  }

  // Atualizar PID
  myPID.Compute();
}
