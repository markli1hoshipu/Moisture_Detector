#include <EEPROM.h>

void setup() {
  Serial.begin(57600);
  
  // read from address 0
  int address = 0;
  Serial.println("EEPROM Data:");
  while (address < EEPROM.length()) {
    // read a byte from EEPROM
    byte value = EEPROM.read(address);
    // print the value to the serial output
    Serial.print(value);
    Serial.print(" ");
    // print 16 bytes each line
    if ((address + 1) % 16 == 0) {
      Serial.println();
    }
    // move to next address
    address++;
  }
}

void loop() {
  // 程序不做任何事情，只需要一次性检查EEPROM即可
}
