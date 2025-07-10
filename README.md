# Medindo a Luminosidade com Sensor BH1750

Este projeto lê o nível de luminosidade de um ambiente usando o sensor **BH1750**, exibe o valor em um **display OLED SSD1306 128x64**, e controla uma **matriz de LEDs NeoPixel 5x5**, acendendo suas bordas em cinza **somente se o ambiente estiver iluminado**.

---

## 📦 Componentes Utilizados

| Componente        | Descrição                                  |
|-------------------|---------------------------------------------|
| Raspberry Pi Pico | Microcontrolador                           |
| BH1750            | Sensor digital de luminosidade (I2C)       |
| Display OLED      | SSD1306 128x64, comunicação via SoftI2C    |
| NeoPixel          | Matriz 5x5 de LEDs endereçáveis WS2812     |

---

## 🛠️ Conexões dos Pinos

| Função              | Pino (RP2040) |
|---------------------|---------------|
| BH1750 SDA          | GP2           |
| BH1750 SCL          | GP3           |
| OLED SDA (SoftI2C)  | GP14          |
| OLED SCL (SoftI2C)  | GP15          |
| NeoPixel            | GP7           |

---

## ⚙️ Funcionamento do Código

### 🔹 Inicialização
- O sensor BH1750 é configurado para começar a medição contínua.
- O display OLED é iniciado para exibir os valores lidos.
- A matriz NeoPixel é mapeada corretamente conforme a montagem física.

### 🔹 Leitura de Luminosidade
- A cada segundo, o BH1750 envia 2 bytes representando a intensidade da luz.
- O valor bruto é convertido em **lux**, com base nas especificações do sensor.

### 🔹 Exibição no Display
- O valor da luminosidade (lux) é mostrado no OLED.
- Em caso de falha na leitura, o display exibe **"Erro leitura!"**.

### 🔹 Controle da Matriz NeoPixel
- Se **lux > 3**, as **bordas da matriz** são acesas em cinza claro (RGB 50, 50, 50).
- Se **lux <= 3**, **todos os LEDs são apagados**, inclusive as bordas.

---

## 🧠 Lógica de Iluminação

- A variável `BORDAS` define os LEDs que formam a borda da matriz 5x5.
- A estrutura `LED` faz o mapeamento lógico dos índices para a ordem física real da matriz NeoPixel.
- A função `acender_borda()` percorre os índices da borda e acende apenas eles.
- A função `apagar_matriz()` desliga todos os LEDs da matriz.

---

## 📊 Comportamento Real

| Situação          | Display OLED     | Matriz NeoPixel        |
|-------------------|------------------|-------------------------|
| Lux > 3           | Mostra o valor   | Bordas acesas em cinza |
| Lux <= 3          | Mostra o valor   | Todos os LEDs apagados |
| Erro de leitura   | "Erro leitura!"  | Todos os LEDs apagados |

---

## ✅ Conclusão

Este sistema oferece uma forma clara e visual de indicar a presença de luz ambiente:

- Fornece **feedback numérico** no display OLED  
- Reage visualmente com LEDs **quando há claridade**  
- Apaga a matriz completamente **no escuro**, destacando a mudança de estado

---
