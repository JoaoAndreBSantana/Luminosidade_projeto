from machine import Pin, I2C, SoftI2C
import time
from ssd1306 import SSD1306_I2C
import neopixel


# Configurações BH1750
BH1750_ADDR = 0x23
BH1750_CMD = 0x10

# i2C sensor luminosiidade
# inicializo o barramento canal 1, 3 para o pino do clck e 2 para o pino dos dados
i2c_sensor = I2C(1, scl=Pin(3), sda=Pin(2), freq=100000)

# i2C display OLED
# utilizo i2c via software nos pinos 15 e 14 

i2c_oled = SoftI2C(scl=Pin(15), sda=Pin(14))
oled = SSD1306_I2C(128, 64, i2c_oled) # inicializa display OLED 128x64 pixels 

#  matriz 5x5 conectado no pino 7
NUM_LEDS = 25
np = neopixel.NeoPixel(Pin(7), NUM_LEDS)# variavel que controla matriz neo pixel

#
LED = {
    0: 24, 1: 23, 2: 22, 3: 21, 4: 20,
    5: 15, 6: 16, 7: 17, 8: 18, 9: 19,
    10: 14, 11: 13, 12: 12, 13: 11, 14: 10,
    15: 5, 16: 6, 17: 7, 18: 8, 19: 9,
    20: 4, 21: 3, 22: 2, 23: 1, 24: 0
}

# indices para o circulo
BORDAS = [
    0, 1, 2, 3, 4,        
    20, 21, 22, 23, 24,   
    5, 10, 15,            
    9, 14, 19            
]
#Envio o comando  via I2C para o BH1750 começar a medir a luz.
def iniciar_bh1750():
    i2c_sensor.writeto(BH1750_ADDR, bytes([BH1750_CMD]))

#Ler2 bytes do sensor via I2C.
#Junta os bytes em um valor inteiro.
def ler_lux():
    data = i2c_sensor.readfrom(BH1750_ADDR, 2)
    raw = (data[0] << 8) | data[1]
    return raw / 1.2# converte para lux dividindo por 1.2 
#percorro a lista bordas e acendo o rgb cinza
def acender_borda(cor=(50, 50, 50)):
    for i in range(NUM_LEDS):
        if i in BORDAS:
            np[LED[i]] = cor
        else:
            np[LED[i]] = (0, 0, 0)
    np.write()#atualizo os leds

def apagar_matriz():
    for i in range(NUM_LEDS):
        np[LED[i]] = (0, 0, 0)
    np.write()
#iniciar sensor e espero 200 ms para estabilização
iniciar_bh1750()
time.sleep_ms(200)

while True:
    try:
        lux = ler_lux()
        print("Luminosidade: {:.2f} ".format(lux))

        oled.fill(0)
        oled.text("Luminosidade:", 0, 16)
        oled.text("{:.2f} ".format(lux), 0, 32)
        oled.show()

        if lux <= 3:
            apagar_matriz()
        else:
            acender_borda((50, 50, 50))  

        time.sleep(1)

    except Exception as e:
        print("Erro na leitura:", e)
        oled.fill(0)
        oled.text("Erro leitura!", 0, 24)
        oled.show()
        apagar_matriz()
        time.sleep(2)
