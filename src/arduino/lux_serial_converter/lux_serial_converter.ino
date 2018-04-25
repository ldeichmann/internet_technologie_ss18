int analogPin = 0;
int val = 0;

float u_in = 3.3;
float r_v = 4700;
float e_v_const_1 = -1.31022;
float e_v_const_2 = 210.91430;

void setup() {
  Serial.begin(9600);              //  setup serial
  // initialize digital pin LED_BUILTIN as an output.
//  pinMode(LED_BUILTIN, OUTPUT);
}

int calculate_lux(int analog_value) {

  float u_ldr = (analog_value * u_in) / 1023;
//  Serial.println("u_ldr");             // debug value
//  Serial.println(u_ldr);             // debug value
  float r_ldr = (r_v * u_ldr) / (u_in - u_ldr);
//  Serial.println("r_ldr");             // debug value
//  Serial.println(r_ldr);             // debug value
  float e_v = pow(r_ldr / 1000, e_v_const_1) * e_v_const_2; // divison by 1000 to convert to kiloohm
//  Serial.println("e_v");             // debug value
//  Serial.println(e_v);             // debug value

  return (int) e_v;
  
}


// the loop function runs over and over again forever
void loop() {
//  digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
//  delay(1000);                       // wait for a second
//  digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
  delay(1000);                       // wait for a second

//  Serial.println("Reading values");             // debug value
  val = analogRead(analogPin);     // read the input pin
  Serial.println(calculate_lux(val));             // debug value

}
