#include<Wire.h>
#include<String.h>
#include"SharpGP2Y10.h"//Thư viện cảm biến bụi
#include"DHT.h"//Thư viện cảm biến nhiệt độ
#include<BH1750.h>//Thư viện cảm biến cường độ ánh sáng

//
const int DHTPIN = 4;//khai báo chân cho cảm biến nhiệt độ vào chân digital 4
const int DHTTYPE = DHT11;//chọn cảm biến DHT11
int dustOutPin = A0;//Chân A0 của cảm biến bụi
int dustInPin = 2;//Chân D2 của cảm biến bụi
int rwSensor = 8;//Cảm biến mưa D8
float dustDensity = 0;//Mật độ bụi

int relay[3] = {5, 6, 7};
//Chân In của relay 1 điều khiển bóng đèn
//Chân In của relay 2 điều khiển quạt
//Chân In của relay 3 điều khiển còi cảnh báo

BH1750 lightMeter;//khai báo đối tượng cho cảm biến cường độ ánh sáng
DHT dht(DHTPIN, DHTTYPE);//khai báo đối tượng cho cảm biến nhiệt độ
SharpGP2Y10 dustSensor(dustOutPin, dustInPin);//Khai báo đối tượng cho cảm biến bụi


//Đọc cảm biến nhiệt độ: sử dụng chân D4
void tempHumRead() {
  float h = dht.readHumidity();//đọc giá trị nhiệt độ từ cảm biến
  float t = dht.readTemperature();//đọc giá trị độ ẩm từ cảm biến

  Serial.print(t);
  Serial.print(" ");
  Serial.print(h);
}

void tempControl() {
  float t = dht.readTemperature();
  Serial.println("nhiet do");
  //  if(t >= 30){
  //    digitalWrite(relay[1], LOW);
  //    Serial.println("quat da bat");
  //  }else{
  //    digitalWrite(relay[1], HIGH);
  //    Serial.println("quat da tat");
  //  }
}

//Đọc cảm biến bụi
void dustRead() {
  dustDensity = dustSensor.getDustDensity();
  Serial.print(dustDensity);
}


//Đọc cảm biến cường độ ánh sáng
void lightRead() {
  float lux = lightMeter.readLightLevel();
  Serial.print(lux);
}

void lightControl() {
  float lux = lightMeter.readLightLevel();
  Serial.println("anh sang");
  //  if(lux <= 50.0){
  //    digitalWrite(relay[0], LOW);
  //    Serial.println("den da bat");
  //  }else{
  //    digitalWrite(relay[0], HIGH);
  //    Serial.println("den da tat");
  //  }
}

//Đọc cảm biến khí ga sử dụng chân A1
void gasRead() {
  int value = analogRead(A1);

  Serial.print(value);
}

void gasNotice() {
  /*sent notice if gas level overcome threshold*/
  int value = analogRead(A1);
  Serial.println("khi ga");
  //  if(value >= 400){
  //    digitalWrite(relay[2], LOW);
  //    Serial.println("canh bao");
  //  }else{
  //    digitalWrite(relay[2], HIGH);
  //    Serial.println("khong canh bao");
  //  }
}


//Đọc cảm biến mưa sử dụng chân D8
void rwRead() {
  int value = digitalRead(rwSensor);//lưu giá trị cảm biến vào biến value
  Serial.print(value);
}

void blink() {
  digitalWrite(13, HIGH);
  delay(1000);
  digitalWrite(13, LOW);
  delay(1000);
  digitalWrite(13, HIGH);
  delay(1000);
  digitalWrite(13, LOW);
  delay(1000);
  digitalWrite(13, HIGH);
  delay(1000);
  digitalWrite(13, LOW);
}

//Điều khiển tự động
void autoControl() {
  tempControl();
  lightControl();
  gasNotice();
}

//Điều khiển bán thủ công
void manualControl(String command) {
  if (command.substring(0, 2) == "x:") {
    int pin = 0;
    int state = LOW;
    if (command.substring(3, 6) == "led") {
      pin = relay[0];
    }
    else if (command.substring(3, 6) == "fan") {
      pin = relay[1];
    }
    else if (command.substring(3, 6) == "alarm") {
      pin = relay[2];
    }
    if (command.substring(7) == "on") {
      state = HIGH;
    }
    else   if (command.substring(7) == "off") {
      state = LOW;
    }
    digitalWrite(pin, state);

  }
}


void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  pinMode(rwSensor, INPUT); // pinMode ở chế độ nhận tín hiệu vào cho cảm biến
  digitalWrite(rwSensor, HIGH);
  Wire.begin();
  lightMeter.begin();
  //Serial.println(F("BH1750 test begin"));
  dht.begin();

  for (int i = 0; i <= 2; i++) {
    pinMode(relay[i], OUTPUT);
  }
  for (int i = 0; i <= 2; i++) {
    digitalWrite(relay[i], HIGH);
  }

}


void loop() {
  // clear serial terminal
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    //    Serial.print("Mode: ");
    if (data == "x: get" || data == "x: get\n") {
      //      Serial.println("manual");
      digitalWrite(LED_BUILTIN, HIGH);
      Serial.flush();
      Serial.print("y: ");
      tempHumRead();
      Serial.print(" ");
      rwRead();
      Serial.print(" ");
      dustRead();
      Serial.print(" ");
      gasRead();
      Serial.print(" ");
      lightRead();
      Serial.print('\n');
      //      while (1) {
      //        String data_next = Serial.readStringUntil('\n');
      //        manualControl(data_next);
      //        if (data_next == "x: end" || data_next == "x: end\n") {
      //          Serial.println("da ket thuc");
      //          break;
      //        }
      //        delay(500);
      //      }
    }
    //    else {
    //      //      Serial.println("auto");
    //      //      autoControl();
    //      delay(100);

    //    }
  }
  digitalWrite(LED_BUILTIN, LOW);
}
