import re
import gradio as gr
from sympy import sympify, SympifyError

# Operadores e números por extenso
palavras_para_operadores = {
    "mais": "+", "menos": "-", "vezes": "*", "multiplicado por": "*",
    "dividido por": "/", "sobre": "/", "elevado a": "**"
}

palavras_para_numeros = {
    "zero": "0", "um": "1", "dois": "2", "três": "3", "quatro": "4",
    "cinco": "5", "seis": "6", "sete": "7", "oito": "8", "nove": "9",
    "dez": "10", "onze": "11", "doze": "12", "treze": "13", "quatorze": "14",
    "quinze": "15", "dezesseis": "16", "dezessete": "17", "dezoito": "18", "dezenove": "19",
    "vinte": "20"
}

def converter_para_expressao(texto):
    texto = texto.lower()
    for palavra, numero in palavras_para_numeros.items():
        texto = re.sub(rf"\b{palavra}\b", numero, texto)
    for palavra, simbolo in palavras_para_operadores.items():
        texto = re.sub(rf"\b{palavra}\b", simbolo, texto)
    texto = re.sub(r"[^\d\+\-\*/\.\(\)\s\^]", "", texto)
    texto = texto.replace("^", "**")
    return texto

def interpretar_expressao(texto):
    expressao = converter_para_expressao(texto)
    try:
        resultado = sympify(expressao).evalf()
        return f"📘 Expressão interpretada: `{expressao}`\n✅ Resultado: `{resultado}`"
    except (SympifyError, SyntaxError):
        return "⚠️ Erro ao interpretar a expressão. Tente reformular."

def sugerir_reformulacoes(expressao):
    sugestoes = []

    if "e dividir" in expressao:
        sugestoes.append("Evite usar 'e dividir', prefira 'dividido por'.")
    
    if "vezes" in expressao and "mais" in expressao and "e dividir" in expressao:
        sugestoes.append("Use uma ordem clara, como: 'sete vezes três mais trezentos e oitenta, dividido por dois'.")

    if not sugestoes:
        return "Erro ao interpretar a expressão. Tente reformular como: 'sete vezes três mais dez' ou 'dez dividido por cinco'."
    
    return "Erro ao interpretar. Sugestões:\n- " + "\n- ".join(sugestoes)
    
# Criação da interface com Gradio
interface = gr.Interface(
    fn=interpretar_expressao,
    inputs=gr.Textbox(lines=2, placeholder="Digite a expressão em linguagem natural..."),
    outputs="markdown",
    title="🧠 Interpretador de Expressões Aritméticas com IA",
    description="Digite uma expressão como: 'sete mais três vezes dois' ou 'dez dividido por cinco'."
)

interface.launch()