//  int LDRSensor = 2;
// 
//void setup()
// {
//  //Initialize Sensor (pin3) as an INPUT.
//  pinMode (LDRSensor, INPUT);
//  Serial.begin (9600);
// }
// 
//void loop()
// {
//   //Read Digital output value from sensor using digitalRead()function
//   int Sensordata = digitalRead (LDRSensor);
//   //Print the sensor value on your serial monitor window
//   Serial.print("Sensor value:");
//   Serial.println(Sensordata);
//   delay(500) ;
// }

void setup()  
 {  
   Serial.begin(9600); 
 }  
void loop()  
 {  
   int s1=analogRead(A0); 
   Serial.println(s1);  
     
   if(s1< 500 )  // number change based on setup later
   {  
    
   }  
   else  
   {  
      
   }  
   delay(500);
 }
