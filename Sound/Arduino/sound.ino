void setup() {
  Serial.begin(9600);
  pinMode(3, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
}

void loop() {
    digitalWrite(3, LOW);
    digitalWrite(5, LOW);
    digitalWrite(6, LOW);
    digitalWrite(9, LOW);
    digitalWrite(10, LOW);

    int sound = Serial.read();
    if(sound>=50){
        // Serial.println((float)sound);
        digitalWrite(3, HIGH);
        
        if(sound>=80){
            // Serial.println((float)sound);
            digitalWrite(5, HIGH);
            
            if(sound>=120){
                // Serial.println((float)sound);
                digitalWrite(6, HIGH);
                
                if(sound>=160){
                    // Serial.println((float)sound);
                    digitalWrite(9, HIGH);
                    
                    if(sound>=210){
                        // Serial.println((float)sound);
                        digitalWrite(10, HIGH);
                        
                    }
                }
            }
        }
        delay(16.67);
    }
}