//left motor pins
const int EnableL= 5;
const int HighL = 6;
const int LowL = 7;

//right motor pins
const int EnableR= 10;
const int HighR = 8;
const int LowR = 9;

//ultra sonic pins
const int trigPin = 1;
const int echoPin = 2;

long duration;
int distance;

char incoming;

void setup() {
  //setting up the differnt pins
  pinMode(EnableL, OUTPUT);
  pinMode(HighL, OUTPUT);
  pinMode(LowL, OUTPUT);

  pinMode(EnableR, OUTPUT);
  pinMode(HighR, OUTPUT);
  pinMode(EnableR, OUTPUT);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT); 
  Serial.begin(9600);
}

//set the left and right motors to the same speed to go forward, to zero to stop
void Forward()
{
    digitalWrite(HighL, LOW);
    digitalWrite(LowL, HIGH);
    digitalWrite(EnableL, 255);

    digitalWrite(HighR, LOW);
    digitalWrite(LowR, HIGH);
    digitalWrite(EnableR, 255);
}

void Stop()
{
    digitalWrite(HighL, LOW);
    digitalWrite(LowL, HIGH);
    digitalWrite(EnableL, 0);

    digitalWrite(HighR, LOW);
    digitalWrite(LowR, HIGH);
    digitalWrite(EnableR, 0);
}

//set the speed of the left motor greater than the right one to go right, vary the differnce to get three speed settings
void Right1()
{
    digitalWrite(HighL, LOW);
    digitalWrite(LowL, HIGH);
    digitalWrite(EnableL, 255);

    digitalWrite(HighR, LOW);
    digitalWrite(LowR, HIGH);
    digitalWrite(EnableR, 100);
}


void Right2()
{
    digitalWrite(HighL, LOW);
    digitalWrite(LowL, HIGH);
    digitalWrite(EnableL, 255);

    digitalWrite(HighR, LOW);
    digitalWrite(LowR, HIGH);
    digitalWrite(EnableR, 150);
}

void Right3()
{
    digitalWrite(HighL, LOW);
    digitalWrite(LowL, HIGH);
    digitalWrite(EnableL, 255);

    digitalWrite(HighR, LOW);
    digitalWrite(LowR, HIGH);
    digitalWrite(EnableR, 200);
}

//same as turning left but set the speed of the right motor greater than the left one to turn left
void Left1()
{
    digitalWrite(HighL, LOW);
    digitalWrite(LowL, HIGH);
    digitalWrite(EnableL, 100);

    digitalWrite(HighR, LOW);
    digitalWrite(LowR, HIGH);
    digitalWrite(EnableR, 255);
}


void Left2()
{
    digitalWrite(HighL, LOW);
    digitalWrite(LowL, HIGH);
    digitalWrite(EnableL, 150);

    digitalWrite(HighR, LOW);
    digitalWrite(LowR, HIGH);
    digitalWrite(EnableR, 255);
}



void Left3()
{
    digitalWrite(HighL, LOW);
    digitalWrite(LowL, HIGH);
    digitalWrite(EnableL, 200);

    digitalWrite(HighR, LOW);
    digitalWrite(LowR, HIGH);
    digitalWrite(EnableR, 255);
}


void loop() {
   
   digitalWrite(trigPin, LOW);
   delayMicroseconds(2);
   digitalWrite(trigPin, HIGH);
   delayMicroseconds(10); 
   digitalWrite(trigPin, LOW);
   
   //get the distance between the vehicule and any potential obstacle
   duration = pulseIn(echoPin, HIGH);
   distance = duration*0.034/2; 
   
   //read the serial connection with the Raspberry it can be: W, Q, E or O
   if(Serial.available() > 0){
      incoming = Serial.read();     

   }
  
  //if the incoming signal is W go forward (given the distance is less than 15cm)
    if (incoming == 'W') {
      if (distance > 15) {
        Forward();
      }
      else {
        Stop();
      }
   }
   //if the incoming signal is Q go left (given the distance is less than 15cm)
    else if (incoming == 'Q') {
      if (distance > 15) {
        Left1();
    }}
     else {
        Stop();
        }
    }
   }
   //if the incoming signal is E go right (given the distance is less than 15cm)
    else if (incoming == 'E') {
      if (distance > 15) {
        Right1();
    }}
    else {
        Stop();
        }
    }    
   }
   //if the incoming signal is O stop the vehicule
    else if (incoming == 'O') {
        Stop();
        }
    }
}
