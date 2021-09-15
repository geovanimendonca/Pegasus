//Sensor de temperatura NTC 10K
// A1 Sensor temperatura
// D3 Led2
// D6 Fan
// D9 Led1

#include <PID_v1.h>
#include <Thermistor.h>

Thermistor temp(1);
double Setpoint, Input, Output;
int y=0;
double Kp = 10, Ki = 1, Kd = 1;

PID myPID(&Input, &Output, &Setpoint, Kp, Ki, Kd, P_ON_M, DIRECT);

unsigned long millisTarefa1 = millis();
unsigned long millisTarefa2 = millis();

const int aquecedor = 5;
double temperatura, temperatura_armazenada, temperatura_real, temperatura_serial;
const int fan = 6;
const int led = 9;
int amostras = 50;

void setup() {

  Serial.begin(9600); // inicializa a comunicação serial
  pinMode(aquecedor, OUTPUT);
  pinMode(fan, OUTPUT);
  pinMode(led, OUTPUT);

  // Inicialização com aquecedor e fan desligados. Led sempre ligado.
  analogWrite(aquecedor, 0);
  analogWrite(fan, 0);
  analogWrite(led, 255);

  // Ativa o PID e limita a saida
  myPID.SetMode(AUTOMATIC);
  myPID.SetOutputLimits(0,80);
}

void loop() {

  if (Serial.available()) {
    Setpoint = Serial.parseInt(); 

    if (Setpoint > 100) { 
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

  
  if (temperatura < Setpoint-1){
    analogWrite(aquecedor, 80); 
  }
  if (Setpoint <40 && temperatura > Setpoint){
    analogWrite(fan,255);
  } else { analogWrite(fan,0);}
  
  // Print Serial
  if ((millis() - millisTarefa1) >= 1000) {
    millisTarefa1 = millis();
    Serial.println(temperatura);
  }
  // Atualizar PID
  myPID.Compute();
}
