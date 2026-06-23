# 📂 Dataset

Esta pasta é destinada ao armazenamento do conjunto de dados utilizado no treinamento da Rede Neural Convolucional (CNN).

O dataset **não está incluído neste repositório** devido ao seu tamanho e às limitações de armazenamento do GitHub.

---

# 📌 Dataset utilizado

**Nome:**

Face occlusion classification

**Origem:**

[GITHUB LamKser](https://github.com/LamKser)

**Objetivo:**

Classificar imagens em duas categorias:

- ✅ Rosto livre (0)
- 🚫 Rosto obstruído (1)

---

# 📥 Download

Faça o download do dataset através do link:

https://www.kaggle.com/datasets/dinhhoanglam/face-occlusion

---

# 📁 Estrutura esperada

Após a extração, esta pasta deve possuir a seguinte estrutura:

```text
dataset/
├── face_occlusion/
    ├── Test/
    │   ├── livre/
    │   └── obstruido/
    │
    ├── Train/
    │   ├── livre/
    │   └── obstruido/
    │
    └── Val/
        ├── livre/
        └── obstruido/
├── README.md
```

> Deverá ser realizado ajustes no nome das pastas.

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

Caso o link deixe de funcionar, consulte o perfil do autor oficial ou substitua por um dataset equivalente contendo imagens de:

- rostos livres;
- rostos parcialmente obstruídos.

---

# 📌 Organização recomendada

```text
dataset/
├── README.md
├── face_occlusion/
    ├── train/
    ├── valid/
    └── test/
```

Não é recomendado adicionar as imagens ao repositório Git, pois elas podem aumentar significativamente o tamanho do projeto.

A pasta `face_occlusion/` deve estar listadas no `.gitignore`.
