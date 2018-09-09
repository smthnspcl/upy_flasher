import machine

i2c = machine.I2C(scl=machine.Pin(4, sda=machine.Pin(5)))
oled = SSD1306_I2C(128, 32, i2c)

oled.fill(0)
oled.test("eyyy")
oled.show()
