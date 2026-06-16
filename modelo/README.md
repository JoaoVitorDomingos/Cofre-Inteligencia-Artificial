# 🧠 Modelo Treinado

Esta pasta é destinada ao armazenamento do modelo de Inteligência Artificial utilizado pelo projeto.

O modelo é responsável por classificar imagens capturadas pela webcam e determinar se o rosto do usuário está livre ou parcialmente obstruído.

---

# 🎯 Objetivo

Realizar a classificação em tempo real de duas classes:

| Classe | Descrição |
|----------------|----------------------------|
| 0 | Rosto livre |
| 1 | Rosto parcialmente obstruído |

A predição é utilizada para controlar a abertura do cofre através da comunicação Serial com o Arduino.

---

# 📂 Estrutura

```text
modelo/

├── README.md
└── modelo.keras
```

Após o treinamento, o arquivo deverá ficar nesta pasta.

---

# 🚀 Como gerar o modelo

Ative o ambiente do projeto:

```bash
conda activate ia-cofre
```

Execute o treinamento:

```bash
python treinamento/train.py
```

Ao final do processo será criado:

```text
modelo/

└── modelo.keras
```

---

# 💾 Formato

O modelo será salvo no formato padrão do TensorFlow/Keras:

```text
modelo.keras
```

Caso seja necessário, também poderá ser exportado em:

```text
modelo.h5
```

---

# 🔄 Fluxo de utilização

```text
Dataset
    │
    ▼
Treinamento
(train.py)
    │
    ▼
modelo.keras
    │
    ▼
Inferência
(inferencia.py)
    │
    ▼
Predição
    │
    ▼
Comunicação Serial
    │
    ▼
Arduino
```

---

# 📋 Arquitetura

O modelo consiste em uma Rede Neural Convolucional (CNN) treinada integralmente do zero.

Características:

- Inicialização aleatória dos pesos
- Sem Transfer Learning
- Sem Fine-tuning
- Sem pesos pré-treinados

Todo o treinamento é realizado localmente utilizando TensorFlow.

---

# 📊 Treinamento

Durante o treinamento são gerados indicadores como:

- Accuracy
- Loss
- Gráficos de treinamento
- Matriz de confusão

Esses arquivos são armazenados na pasta:

```text
resultados/
```

---

# ⚠️ Observações

O arquivo `modelo.keras` pode não estar presente neste repositório por um dos seguintes motivos:

- ainda não foi realizado o treinamento;
- o modelo está sendo regenerado;
- o arquivo ultrapassa o tamanho recomendado para armazenamento no GitHub.

Caso o arquivo não exista, basta executar novamente:

```bash
python treinamento/train.py
```

---

# 📌 Arquivo esperado

```text
modelo/

├── README.md
└── modelo.keras
```

---

# 🔒 Uso no projeto

O script `inferencia/inferencia.py` carrega automaticamente o modelo salvo nesta pasta.

Fluxo resumido:

```text
Webcam
    │
    ▼
modelo.keras
    │
    ▼
Classificação

    ├── Rosto livre
    │         │
    │         ▼
    │   Cofre liberado
    │
    └── Rosto obstruído
              │
              ▼
      Cofre bloqueado
```