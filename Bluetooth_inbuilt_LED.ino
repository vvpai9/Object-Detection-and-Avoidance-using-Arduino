void setup() {
  Serial1.begin(9600);
  pinMode(13, OUTPUT);
}

void loop() {
  char data;
  data = Serial1.read();
  if (data == '1')
  {
    do
    {
      digitalWrite(13, HIGH);
      data = Serial1.read();
    }while(data != '0');
  }
  else
    digitalWrite(13, LOW);
}
