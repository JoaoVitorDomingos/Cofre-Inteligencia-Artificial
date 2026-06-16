# 📂 Dataset

Esta pasta é destinada ao armazenamento do conjunto de dados utilizado no treinamento da Rede Neural Convolucional (CNN).

O dataset **não está incluído neste repositório** devido ao seu tamanho e às limitações de armazenamento do GitHub.

---

# 📌 Dataset utilizado

**Nome:**

Burglary Detection / Face Mask Detection

**Origem:**

Roboflow Universe

**Objetivo:**

Classificar imagens em duas categorias:

- ✅ Rosto livre
- 🚫 Rosto parcialmente obstruído

---

# 📥 Download

Faça o download do dataset através do link:

https://universe.roboflow.com/face-mask-detection-v7lf1/burglary-detection

---

# 📁 Estrutura esperada

Após a extração, esta pasta deve possuir a seguinte estrutura:

```text
dataset/

├── train/
│   ├── livre/
│   └── tampado/
│
├── valid/
│   ├── livre/
│   └── tampado/
│
└── test/
    ├── livre/
    └── tampado/
```

Caso a estrutura exportada pelo Roboflow seja diferente, ajuste os caminhos utilizados no código de treinamento.

---

# 🧠 Utilização

O dataset é utilizado exclusivamente durante a etapa de treinamento do modelo.

Fluxo:

```text
Dataset
    │
    ▼
Treinamento (train.py)
    │
    ▼
Modelo treinado (.keras)
    │
    ▼
Inferência em tempo real
```

---

# 📄 Observações

- O treinamento é realizado integralmente no computador.
- Nenhum modelo pré-treinado é utilizado.
- Todos os pesos da rede neural são inicializados aleatoriamente.
- O modelo final é salvo na pasta `modelo/`.

---

# ⚠️ Aviso

Este repositório não redistribui o dataset original.

Todos os direitos sobre as imagens pertencem aos seus respectivos autores e/ou à plataforma onde foram disponibilizadas.

Caso o link deixe de funcionar, consulte a documentação oficial do Roboflow ou substitua por um dataset equivalente contendo imagens de:

- rostos livres;
- rostos parcialmente obstruídos.

---

# 📌 Organização recomendada

```text
dataset/

├── README.md

├── train/

├── valid/

└── test/
```

Não é recomendado adicionar as imagens ao repositório Git, pois elas podem aumentar significativamente o tamanho do projeto.

As pastas `train/`, `valid/` e `test/` devem estar listadas no `.gitignore`.