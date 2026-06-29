"""
TALLER PLN - Aplicación Básica de Procesamiento de Lenguaje Natural
Desarrolla las principales etapas del PLN: Tokenización, Normalización,
Lematización y Stemming sobre un texto ingresado por el usuario.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
import unicodedata
import re
import os

# --- Descargar recursos NLTK necesarios ---
def descargar_recursos_nltk():
    """Descarga los recursos de NLTK necesarios si no están disponibles."""
    recursos = ['punkt', 'punkt_tab', 'stopwords', 'wordnet', 'omw-1.4']
    for recurso in recursos:
        try:
            nltk.data.find(f'tokenizers/{recurso}' if 'punkt' in recurso else recurso)
        except LookupError:
            nltk.download(recurso, quiet=True)

descargar_recursos_nltk()

# Importar después de descargar
from nltk.stem import WordNetLemmatizer


# ========================== Funciones PLN ==========================

def tokenizar(texto):
    """
    Tokenización: Divide el texto en tokens (palabras y signos de puntuación).
    """
    if not texto.strip():
        return "⚠ Por favor, ingrese un texto."
    tokens = word_tokenize(texto, language='spanish')
    resultado = "═══ TOKENIZACIÓN ═══\n\n"
    resultado += f"Texto original:\n\"{texto}\"\n\n"
    resultado += f"Número de tokens: {len(tokens)}\n\n"
    resultado += "Tokens encontrados:\n"
    for i, token in enumerate(tokens, 1):
        resultado += f"  [{i}] {token}\n"
    return resultado


def normalizar(texto):
    """
    Normalización: Convierte a minúsculas, elimina acentos/tildes,
    remueve signos de puntuación y elimina stopwords.
    """
    if not texto.strip():
        return "⚠ Por favor, ingrese un texto."

    resultado = "═══ NORMALIZACIÓN ═══\n\n"
    resultado += f"Texto original:\n\"{texto}\"\n\n"

    # Paso 1: Convertir a minúsculas
    texto_lower = texto.lower()
    resultado += f"1. Minúsculas:\n   \"{texto_lower}\"\n\n"

    # Paso 2: Eliminar acentos/tildes
    texto_sin_acentos = ''.join(
        c for c in unicodedata.normalize('NFD', texto_lower)
        if unicodedata.category(c) != 'Mn'
    )
    resultado += f"2. Sin acentos:\n   \"{texto_sin_acentos}\"\n\n"

    # Paso 3: Eliminar signos de puntuación
    texto_sin_puntuacion = re.sub(r'[^\w\s]', '', texto_sin_acentos)
    resultado += f"3. Sin puntuación:\n   \"{texto_sin_puntuacion}\"\n\n"

    # Paso 4: Tokenizar
    tokens = word_tokenize(texto_sin_puntuacion, language='spanish')

    # Paso 5: Eliminar stopwords
    stop_words = set(stopwords.words('spanish'))
    # Normalizar stopwords (sin acentos) para mejor coincidencia
    stop_words_norm = set()
    for sw in stop_words:
        sw_norm = ''.join(
            c for c in unicodedata.normalize('NFD', sw)
            if unicodedata.category(c) != 'Mn'
        )
        stop_words_norm.add(sw_norm)

    tokens_filtrados = [t for t in tokens if t not in stop_words_norm]
    resultado += f"4. Stopwords eliminadas:\n   {list(stop_words.intersection(set(word_tokenize(texto_lower, language='spanish'))))}\n\n"
    resultado += f"5. Texto normalizado:\n   {tokens_filtrados}\n"

    return resultado


def lematizar(texto):
    """
    Lematización: Reduce las palabras a su forma base (lema)
    utilizando WordNetLemmatizer.
    """
    if not texto.strip():
        return "⚠ Por favor, ingrese un texto."

    lemmatizer = WordNetLemmatizer()
    tokens = word_tokenize(texto.lower(), language='spanish')
    # Filtrar solo palabras (sin puntuación)
    tokens = [t for t in tokens if re.match(r'\w+', t)]

    resultado = "═══ LEMATIZACIÓN ═══\n\n"
    resultado += f"Texto original:\n\"{texto}\"\n\n"
    resultado += f"{'Palabra':<20} {'Lema':<20}\n"
    resultado += "─" * 40 + "\n"

    for token in tokens:
        lema = lemmatizer.lemmatize(token)
        indicador = " ✓" if lema != token else ""
        resultado += f"  {token:<20} → {lema:<20}{indicador}\n"

    return resultado


def aplicar_stemming(texto):
    """
    Stemming: Reduce las palabras a su raíz utilizando
    SnowballStemmer para español.
    """
    if not texto.strip():
        return "⚠ Por favor, ingrese un texto."

    stemmer = SnowballStemmer('spanish')
    tokens = word_tokenize(texto.lower(), language='spanish')
    # Filtrar solo palabras (sin puntuación)
    tokens = [t for t in tokens if re.match(r'\w+', t)]

    resultado = "═══ STEMMING ═══\n\n"
    resultado += f"Texto original:\n\"{texto}\"\n\n"
    resultado += f"{'Palabra':<20} {'Raíz (Stem)':<20}\n"
    resultado += "─" * 40 + "\n"

    for token in tokens:
        raiz = stemmer.stem(token)
        indicador = " ✓" if raiz != token else ""
        resultado += f"  {token:<20} → {raiz:<20}{indicador}\n"

    return resultado


# ========================== Interfaz Gráfica ==========================

class AplicacionPLN:
    def __init__(self, root):
        self.root = root
        self.root.title("PLN")
        self.root.geometry("700x580")
        self.root.resizable(True, True)
        self.root.configure(bg="#f0f4f8")

        # Estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')

        self._crear_widgets()

    def _crear_widgets(self):
        # --- Título ---
        titulo = tk.Label(
            self.root,
            text="Aplicación PLN",
            font=("Arial", 16, "bold"),
            bg="#f0f4f8",
            fg="#2c3e50"
        )
        titulo.pack(pady=(15, 10))

        # --- Frame de entrada ---
        frame_entrada = tk.LabelFrame(
            self.root,
            text="Ingresar Texto",
            font=("Arial", 10),
            bg="#f0f4f8",
            fg="#2c3e50",
            padx=10,
            pady=5
        )
        frame_entrada.pack(padx=20, pady=(0, 10), fill="x")

        self.texto_entrada = tk.Text(
            frame_entrada,
            height=3,
            width=60,
            font=("Arial", 11),
            wrap="word",
            relief="solid",
            borderwidth=1
        )
        self.texto_entrada.pack(padx=5, pady=5, fill="x")

        # --- Frame de botones y salida ---
        frame_contenido = tk.Frame(self.root, bg="#f0f4f8")
        frame_contenido.pack(padx=20, pady=5, fill="both", expand=True)

        # --- Frame de botones (izquierda) ---
        frame_botones = tk.Frame(frame_contenido, bg="#f0f4f8")
        frame_botones.pack(side="left", fill="y", padx=(0, 15))

        botones_config = [
            ("Tokenizar", "#3498db", self._tokenizar),
            ("Normalización", "#27ae60", self._normalizar),
            ("Lematización", "#8e44ad", self._lematizar),
            ("Stemming", "#e67e22", self._stemming),
        ]

        for texto, color, comando in botones_config:
            btn = tk.Button(
                frame_botones,
                text=texto,
                command=comando,
                font=("Arial", 10, "bold"),
                bg=color,
                fg="white",
                activebackground=color,
                activeforeground="white",
                width=15,
                height=1,
                cursor="hand2",
                relief="raised",
                borderwidth=2
            )
            btn.pack(pady=5)

        # Botón limpiar
        btn_limpiar = tk.Button(
            frame_botones,
            text="Limpiar",
            command=self._limpiar,
            font=("Arial", 9),
            bg="#95a5a6",
            fg="white",
            activebackground="#7f8c8d",
            activeforeground="white",
            width=15,
            cursor="hand2",
            relief="raised",
            borderwidth=2
        )
        btn_limpiar.pack(pady=(15, 5))

        # --- Frame de salida (derecha) ---
        frame_salida = tk.LabelFrame(
            frame_contenido,
            text="Salida",
            font=("Arial", 10),
            bg="#f0f4f8",
            fg="#2c3e50",
            padx=5,
            pady=5
        )
        frame_salida.pack(side="left", fill="both", expand=True)

        self.texto_salida = tk.Text(
            frame_salida,
            height=15,
            width=45,
            font=("Consolas", 10),
            wrap="word",
            relief="solid",
            borderwidth=1,
            state="disabled",
            bg="#ffffff"
        )
        self.texto_salida.pack(padx=5, pady=5, fill="both", expand=True)

        # Scrollbar para la salida
        scrollbar = ttk.Scrollbar(
            self.texto_salida,
            orient="vertical",
            command=self.texto_salida.yview
        )
        scrollbar.pack(side="right", fill="y")
        self.texto_salida.configure(yscrollcommand=scrollbar.set)

    def _obtener_texto(self):
        """Obtiene el texto del campo de entrada."""
        return self.texto_entrada.get("1.0", "end-1c")

    def _mostrar_resultado(self, resultado):
        """Muestra el resultado en el área de salida."""
        self.texto_salida.configure(state="normal")
        self.texto_salida.delete("1.0", "end")
        self.texto_salida.insert("1.0", resultado)
        self.texto_salida.configure(state="disabled")

    def _tokenizar(self):
        texto = self._obtener_texto()
        resultado = tokenizar(texto)
        self._mostrar_resultado(resultado)

    def _normalizar(self):
        texto = self._obtener_texto()
        resultado = normalizar(texto)
        self._mostrar_resultado(resultado)

    def _lematizar(self):
        texto = self._obtener_texto()
        resultado = lematizar(texto)
        self._mostrar_resultado(resultado)

    def _stemming(self):
        texto = self._obtener_texto()
        resultado = aplicar_stemming(texto)
        self._mostrar_resultado(resultado)

    def _limpiar(self):
        """Limpia los campos de entrada y salida."""
        self.texto_entrada.delete("1.0", "end")
        self.texto_salida.configure(state="normal")
        self.texto_salida.delete("1.0", "end")
        self.texto_salida.configure(state="disabled")


# ========================== Main ==========================

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionPLN(root)
    root.mainloop()
