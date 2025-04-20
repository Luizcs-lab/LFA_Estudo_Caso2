import re
import gradio as gr
from sympy import symbols, sympify, SympifyError, sin, cos, tan, log, sqrt, exp
from transformers import pipeline
import torch

# Inicializa modelo BART para correção básica
try:
    grammar_corrector = pipeline("text-classification", model="facebook/bart-large-mnli")
except Exception as e:
    grammar_corrector = None
    print(f"Erro ao carregar modelo BART: {e}")

x = symbols('x')

palavras_para_operadores = {
    "mais": "+", "menos": "-", "vezes": "*", "multiplicado por": "*",
    "dividido por": "/", "sobre": "/", "elevado a": "**", "ao quadrado": "**2"
}

palavras_para_numeros = {
    "zero": "0", "um": "1", "dois": "2", "três": "3", "quatro": "4",
    "cinco": "5", "seis": "6", "sete": "7", "oito": "8", "nove": "9",
    "dez": "10", "onze": "11", "doze": "12", "treze": "13", "quatorze": "14",
    "quinze": "15", "dezesseis": "16", "dezessete": "17", "dezoito": "18", "dezenove": "19",
    "vinte": "20", "trinta": "30", "quarenta": "40", "cinquenta": "50"
}

funcoes_matematicas = {
    "seno de": "sin", "cosseno de": "cos", "tangente de": "tan",
    "log de": "log", "raiz de": "sqrt", "exponencial de": "exp"
}

def tratar_numeros_compostos(texto):
    for dezena in ["vinte", "trinta", "quarenta", "cinquenta"]:
        for unidade in palavras_para_numeros:
            composto = f"{dezena} e {unidade}"
            if composto in texto:
                valor = int(palavras_para_numeros[dezena]) + int(palavras_para_numeros[unidade])
                texto = texto.replace(composto, str(valor))
    return texto

def corrigir_entrada(texto):
    if grammar_corrector:
        # Aqui o modelo apenas retorna classificação sem modificar a frase
        # Implementações mais robustas exigiriam um modelo text2text como T5.
        return texto  # Placeholder, pois bart-large-mnli não corrige texto diretamente
    return texto

def converter_para_expressao(texto):
    texto = texto.lower()
    texto = corrigir_entrada(texto)
    texto = tratar_numeros_compostos(texto)

    for palavra, numero in palavras_para_numeros.items():
        texto = re.sub(rf"\b{palavra}\b", numero, texto)

    for palavra, simbolo in palavras_para_operadores.items():
        texto = re.sub(rf"\b{palavra}\b", simbolo, texto)

    for palavra, funcao in funcoes_matematicas.items():
        texto = re.sub(rf"{palavra}\s*([\w\.]+)", rf"{funcao}(\1)", texto)

    return texto.strip()

def interpretar_expressao(texto):
    expressao = converter_para_expressao(texto)
    try:
        resultado = sympify(expressao)
        resultado_numerico = resultado.evalf()
        return f"### ✅ Expressão reconhecida:\n`{expressao}`\n\n**Resultado Numérico:** `{resultado_numerico}`"
    except (SympifyError, SyntaxError):
        return "⚠️ Não foi possível interpretar. Exemplos:\n- sete mais dois vezes três\n- raiz de vinte e cinco"

with gr.Blocks(css=".gr-button-primary {background: #10b981 !important;}") as interface:
    gr.Markdown(
        """
        # 🧠 Interpretador de Expressões com IA

        Digite uma expressão como:
        - sete mais dois vezes três
        - raiz de vinte e cinco
        """
    )

    entrada = gr.Textbox(label="Digite a expressão:", placeholder="Ex: raiz de 25 ou sete mais dois vezes três")
    botao = gr.Button("Interpretar", variant="primary")
    saida_texto = gr.Markdown()

    botao.click(fn=interpretar_expressao, inputs=entrada, outputs=saida_texto)

    gr.Markdown("---\n📘 Suporte a expressões aritméticas e funções trigonométricas!")

interface.launch()