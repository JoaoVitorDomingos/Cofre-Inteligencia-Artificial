# 🔐 Cofre Inteligente com Inteligência Artificial

Projeto desenvolvido para a disciplina de **Inteligência Artificial** do curso de **Bacharelado em Ciência da Computação - UNESPAR**.

O objetivo do projeto é integrar uma Rede Neural Convolucional (CNN) treinada do zero com um sistema embarcado em Arduino, criando um cofre inteligente capaz de bloquear sua abertura quando detectar um rosto parcialmente obstruído.

---

## 📖 Sobre o projeto

O sistema utiliza uma câmera conectada ao computador para capturar imagens em tempo real.

A imagem é processada por uma Rede Neural Convolucional treinada para classificar duas situações:

- ✅ Rosto livre
- 🚫 Rosto parcialmente obstruído

Após a classificação, um script Python envia um comando pela porta Serial para o Arduino.

Mesmo que a senha esteja correta, o cofre permanecerá bloqueado caso a IA identifique uma obstrução no rosto do usuário.

---

## 🎯 Objetivo

Adicionar uma camada extra de segurança ao cofre eletrônico desenvolvido na disciplina de Sistemas Microcontrolados, utilizando técnicas de Visão Computacional e Machine Learning.

---

## ⚙️ Funcionamento

```text
                 Webcam
                    │
                    ▼
         Captura de imagem (Python)
                    │
                    ▼
        Rede Neural Convolucional
                    │
         ┌──────────┴──────────┐
         │                     │
         ▼                     ▼
    Rosto livre        Rosto obstruído
         │                     │
         └──────────┬──────────┘
                    ▼
          Comunicação Serial
                    │
                    ▼
                Arduino Uno
                    │
                    ▼
        Controle do sistema do cofre
```

---

## 🔒 Funcionamento do cofre

O hardware é composto por:

- Microservo
- Display de 7 segmentos
- LEDs
- Buzzer
- Potenciômetro
- Botões

### Senha correta + rosto livre

- LED verde acende
- Buzzer emite um bip curto
- Microservo abre o cofre

### Senha correta + rosto obstruído

- Cofre permanece bloqueado
- Display exibe mensagem de bloqueio
- Servo permanece fechado

### Senha incorreta

- LED vermelho acende
- Buzzer emite um bip médio

### Três tentativas incorretas

- LED vermelho piscando
- Buzzer emite alarme contínuo

---

# 🧠 Inteligência Artificial

## Tipo de modelo

Rede Neural Convolucional (CNN)

Treinada integralmente do zero, sem utilização de pesos pré-treinados ou técnicas de Transfer Learning.

---

## Classes

| Classe | Descrição |
|----------------|----------------------------|
| 0 | Rosto livre |
| 1 | Rosto parcialmente obstruído |

---

## Dataset

Dataset público utilizado durante o treinamento.

Base principal:

Face Mask / Burglary Detection Dataset (Roboflow)

> O dataset não está presente neste repositório devido ao seu tamanho.

Consulte:

[`dataset/README.md`](./dataset/README.md)

para instruções de download.

---

# 📁 Estrutura do projeto

```text
cofre-inteligente-ia/

│
├── arduino/
│
├── dataset/
│
├── docs/
│
├── inferencia/
│
├── modelo/
│
├── resultados/
│
├── treinamento/
│
├── requirements.txt
├── environment.yml
├── .gitignore
└── README.md
```

---

# 💻 Tecnologias utilizadas

## Linguagens

- Python 3.11
- C++ (Arduino)

## Bibliotecas

- TensorFlow 2.20
- OpenCV
- NumPy
- Scikit-Learn
- Matplotlib
- PySerial

## Hardware

- Arduino Uno
- Webcam
- Microservo
- LEDs
- Buzzer
- Display de 7 segmentos
- Potenciômetro

---

# 🚀 Configuração do ambiente

## Criando ambiente Conda

```bash
conda create -n ia-cofre python=3.11
```

Ativando:

```bash
conda activate ia-cofre
```

---

## Instalando dependências

```bash
pip install tensorflow==2.20.0

conda install -c conda-forge opencv

conda install -c anaconda pyserial

conda install -c anaconda scikit-learn

pip install matplotlib
```

Ou simplesmente:

```bash
pip install -r requirements.txt
```

---

# ▶️ Executando o treinamento

```bash
python treinamento/train.py
```

O modelo treinado será salvo em:

```text
modelo/modelo.keras
```

---

# ▶️ Executando a inferência

```bash
python inferencia/inferencia.py
```

O script irá:

- abrir a webcam;
- capturar imagens em tempo real;
- realizar a classificação;
- enviar comandos para o Arduino via Serial.

---

# 🔌 Comunicação com Arduino

O computador envia um byte pela Serial:

| Valor | Ação |
|------------|----------------------------|
| 0 | Cofre liberado |
| 1 | Cofre bloqueado |

O Arduino interpreta esse comando e decide se permitirá ou não a abertura do cofre.

---

# 📊 Resultados

Após o treinamento serão disponibilizados:

- Accuracy
- Loss
- Gráficos de treinamento
- Matriz de confusão

Arquivos:

```text
resultados/

    graficos/

    matriz_confusao/
```

---

# 📚 Contexto acadêmico

Projeto desenvolvido para integrar os conhecimentos das disciplinas de:

- Inteligência Artificial
- Sistemas Microcontrolados

A proposta consiste em utilizar um modelo de Machine Learning treinado no computador para classificar imagens em tempo real e controlar um sistema físico embarcado através de comunicação Serial.

---

# 👥 Integrantes

| Nome |
|----------------|
| João Capazório |
| Guilherme Henrique |

---

# 📄 Licença

Este projeto foi desenvolvido exclusivamente para fins acadêmicos.

Uso livre para estudos e consulta.