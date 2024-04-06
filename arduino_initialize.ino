#include <EEPROM.h>

void setup() {
  Serial.begin(57600);
  
  // 从地址0开始读取EEPROM中的数据
  int address = 0;
  Serial.println("EEPROM Data:");
  while (address < EEPROM.length()) {
    // 从EEPROM中读取一个字节的数据
    EEPROM.write(address,0);
    byte value = EEPROM.read(address);
    // 打印读取的数据到串口
    Serial.print(value);
    Serial.print(" ");
    // 每行打印16个字节
    if ((address + 1) % 16 == 0) {
      Serial.println();
    }
    // 移动到下一个地址
    address++;
  }
}

void loop() {
  // 程序不做任何事情，只需要一次性检查EEPROM即可
}
