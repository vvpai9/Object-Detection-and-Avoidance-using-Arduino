const int trig = 8;
const int echo = 9;
long duration;
int distance;
char lastCommand = 's'; // Initialize last command as 's' (stop)

void setup() {
  Serial1.begin(9600);
  pinMode(trig, OUTPUT);
  pinMode(echo, INPUT);
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
}

void loop() {
  digitalWrite(trig, LOW);
  delayMicroseconds(2);
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);
  duration = pulseIn(echo, HIGH);
  distance = duration * 0.034 / 2;
  Serial1.print("Distance: ");
  Serial1.print(distance);
  Serial1.println(" cm");
  delay(100);

  if (distance <= 10) {
    stopMotors(); // Stop motors if obstacle detected
  } else {
    // If no obstacle, continue with the last command
    executeCommand(lastCommand);
  }

  if (Serial1.available() > 0) {
    lastCommand = Serial1.read(); // Update last command
    executeCommand(lastCommand); // Execute the received command
  }
}

void executeCommand(char command) {
  switch (command) {
    case 'l':
      left();
      break;
    case 'r':
      right();
      break;
    case 'b':
      backward();
      break;
    case 'f':
      forward();
      break;
    case 's':
      stopMotors();
      break;
    default:
      break;
  }
}

void forward() {
  digitalWrite(2, HIGH);
  digitalWrite(3, LOW);
  digitalWrite(4, HIGH);
  digitalWrite(5, LOW);
}

void backward() {
  digitalWrite(2, LOW);
  digitalWrite(3, HIGH);
  digitalWrite(4, LOW);
  digitalWrite(5, HIGH);
}

void left() {
  digitalWrite(2, LOW);
  digitalWrite(3, LOW);
  digitalWrite(4, HIGH);
  digitalWrite(5, LOW);
}

void right() {
  digitalWrite(2, HIGH);
  digitalWrite(3, LOW);
  digitalWrite(4, LOW);
  digitalWrite(5, LOW);
}

void stopMotors() {
  digitalWrite(2, LOW);
  digitalWrite(3, LOW);
  digitalWrite(4, LOW);
  digitalWrite(5, LOW);
}
