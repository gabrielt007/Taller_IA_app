# Taller PLN - Aplicación Básica de Procesamiento de Lenguaje Natural

Aplicación gráfica desarrollada en Python que permite aplicar las principales etapas del **Procesamiento de Lenguaje Natural (PLN)** sobre un texto ingresado por el usuario.

## Funcionalidades

| Etapa | Descripción |
|---|---|
| **Tokenización** | Divide el texto en tokens (palabras y signos de puntuación) |
| **Normalización** | Convierte a minúsculas, elimina acentos, puntuación y stopwords |
| **Lematización** | Reduce las palabras a su forma base (lema) |
| **Stemming** | Reduce las palabras a su raíz usando SnowballStemmer (español) |

## Requisitos

- Python 3.8+
- NLTK

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/taller_IA.git
cd taller_IA

# Instalar dependencias
pip install -r requirements.txt
```

## Ejecución

```bash
python taller_pln.py
```

> **Nota:** Los recursos de NLTK necesarios se descargan automáticamente la primera vez que se ejecuta la aplicación.

## Tecnologías

- **Python** - Lenguaje de programación
- **Tkinter** - Interfaz gráfica
- **NLTK** - Procesamiento de Lenguaje Natural

