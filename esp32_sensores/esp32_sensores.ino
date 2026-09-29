/*
  ============================================================
  ESP32 - Lectura de sensores de ángulo (potenciómetros)
  Proyecto: Brazo robótico con pinza - U_Militar
  ============================================================

  Este código lee 3 potenciómetros conectados a pines ADC del
  ESP32. Cada potenciómetro simula un "sensor de grados" que
  indica la posición angular deseada para:

    - J1   -> joint_1   (rotación de la base)
    - J2   -> joint_2   (codo)
    - GRIP -> joint_gripper + joint_dedo_izq/der (apertura pinza)

  Los valores se envían por UART (Serial) en formato CSV cada
  100 ms, con el formato:

      J1:<grados>,J2:<grados>,GRIP:<grados>\n

  Ejemplo de línea enviada:
      J1:120,J2:80,GRIP:45

  El script en Python (control_pybullet.py) lee estas líneas
  desde el puerto serial y mueve el robot en PyBullet.

  CONEXIONES SUGERIDAS (ESP32):
    - Potenciómetro J1   -> GPIO 34 (ADC1_CH6)
    - Potenciómetro J2   -> GPIO 35 (ADC1_CH7)
    - Potenciómetro GRIP -> GPIO 32 (ADC1_CH4)
    - VCC potes -> 3.3V, GND potes -> GND
*/

#define PIN_J1   34
#define PIN_J2   35
#define PIN_GRIP 32

const int ADC_MAX = 4095;      // Resolución ADC del ESP32 (12 bits)
const int ANGULO_MIN = 0;      // Grados mínimos del potenciómetro
const int ANGULO_MAX = 180;    // Grados máximos del potenciómetro

const unsigned long INTERVALO_MS = 100; // Frecuencia de envío
unsigned long ultimoEnvio = 0;

void setup() {
  Serial.begin(115200);
  analogReadResolution(12); // Asegura resolución de 12 bits (0-4095)
  delay(500);
  Serial.println("ESP32 listo - enviando datos de sensores por UART");
}

void loop() {
  unsigned long ahora = millis();

  if (ahora - ultimoEnvio >= INTERVALO_MS) {
    ultimoEnvio = ahora;

    int lecturaJ1   = analogRead(PIN_J1);
    int lecturaJ2   = analogRead(PIN_J2);
    int lecturaGrip = analogRead(PIN_GRIP);

    int gradosJ1   = map(lecturaJ1,   0, ADC_MAX, ANGULO_MIN, ANGULO_MAX);
    int gradosJ2   = map(lecturaJ2,   0, ADC_MAX, ANGULO_MIN, ANGULO_MAX);
    int gradosGrip = map(lecturaGrip, 0, ADC_MAX, ANGULO_MIN, ANGULO_MAX);

    Serial.print("J1:");
    Serial.print(gradosJ1);
    Serial.print(",J2:");
    Serial.print(gradosJ2);
    Serial.print(",GRIP:");
    Serial.println(gradosGrip);
  }
}
