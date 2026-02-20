// ---------------- LEFT MOTOR ----------------
#define L_PWM 5
#define L_DIR 4
#define L_ENCA 2
#define L_ENCB 3

// ---------------- RIGHT MOTOR ----------------
#define R_PWM 6
#define R_DIR 7
#define R_ENCA 18
#define R_ENCB 19

// ---------------- ENCODER VARIABLES ----------------
volatile long leftTicks = 0;
volatile long rightTicks = 0;

const int ticks_per_rev = 683;
const float wheel_diameter = 0.115;
const float wheel_circumference = 3.1416 * wheel_diameter;

// ---------------- SETUP ----------------
void setup() {

  Serial.begin(115200);

  pinMode(L_PWM, OUTPUT);
  pinMode(L_DIR, OUTPUT);
  pinMode(R_PWM, OUTPUT);
  pinMode(R_DIR, OUTPUT);

  pinMode(L_ENCA, INPUT);
  pinMode(L_ENCB, INPUT);
  pinMode(R_ENCA, INPUT);
  pinMode(R_ENCB, INPUT);

  attachInterrupt(digitalPinToInterrupt(L_ENCA), leftEncoderISR, RISING);
  attachInterrupt(digitalPinToInterrupt(R_ENCA), rightEncoderISR, RISING);

  digitalWrite(L_DIR, HIGH);
  digitalWrite(R_DIR, HIGH);
}

// ---------------- LOOP ----------------
void loop() {

  // Run motors slowly for testing
  analogWrite(L_PWM, 80);
  analogWrite(R_PWM, 80);

  // Send ONLY ticks in simple format
  Serial.print("ENC:");
  Serial.print(leftTicks);
  Serial.print(",");
  Serial.println(rightTicks);

  delay(50);   // 20Hz update rate
}


// ---------------- ENCODER ISRs ----------------
void leftEncoderISR() {
  if (digitalRead(L_ENCB))
    leftTicks++;
  else
    leftTicks--;
}

void rightEncoderISR() {
  if (digitalRead(R_ENCB))
    rightTicks++;
  else
    rightTicks--;
}