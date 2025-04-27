from ast import Div
import re
import gradio as gr
from sympy import Add, FunctionClass, Mul, Pow, symbols, sympify, SympifyError, sin, cos, tan, log, sqrt, exp, sinh, cosh, tanh
from transformers import pipeline

# Inicializa modelo de correção gramatical
try:
    grammar_corrector = pipeline("text2text-generation", model="t5-small", tokenizer="t5-small")
except Exception as e:
    grammar_corrector = None
    print(f"Erro ao carregar modelo: {e}")

x = symbols('x')

palavras_para_operadores = {
    "mais": "+", "menos": "-", "vezes": "*", "multiplicado por": "*",
    "dividido por": "/", "sobre": "/", "elevado a": "**", "ao quadrado": "**2"
}

unidades = {
    "zero": 0, "um": 1, "dois": 2, "três": 3, "quatro": 4, "cinco": 5,
    "seis": 6, "sete": 7, "oito": 8, "nove": 9
}

dezenas = {
    "dez": 10, "onze": 11, "doze": 12, "treze": 13, "quatorze": 14, "quinze": 15,
    "dezesseis": 16, "dezessete": 17, "dezoito": 18, "dezenove": 19,
    "vinte": 20, "trinta": 30, "quarenta": 40, "cinquenta": 50,
    "sessenta": 60, "setenta": 70, "oitenta": 80, "noventa": 90
}

centenas = {
    "cem": 100, "cento": 100, "duzentos": 200, "trezentos": 300, "quatrocentos": 400,
    "quinhentos": 500, "seiscentos": 600, "setecentos": 700, "oitocentos": 800, "novecentos": 900
}

multiplicadores = {
    "mil": 1000, "milhão": 1000000, "milhões": 1000000
}

funcoes_matematicas = {
    "seno de": "sin", "cosseno de": "cos", "tangente de": "tan",
    "log de": "log", "raiz de": "sqrt", "exponencial de": "exp", 
    "seno hiperbólico de": "sinh", "cosseno hiperbólico de": "cosh", "tangente hiperbólica de": "tanh"
}
#
def texto_para_numero(texto):
    palavras = texto.split()
    total = 0
    atual = 0

    for palavra in palavras:
        if palavra in unidades:
            atual += unidades[palavra]
        elif palavra in dezenas:
            atual += dezenas[palavra]
        elif palavra in centenas:
            atual += centenas[palavra]
        elif palavra in multiplicadores:
            if atual == 0:
                atual = 1
            total += atual * multiplicadores[palavra]
            atual = 0
        elif palavra == "e":
            continue
        else:
            if atual != 0:
                total += atual
                atual = 0
    total += atual
    return str(total)

def tratar_numeros(texto):
    for palavra, numero in unidades.items():
        texto = re.sub(rf'\b{palavra}\b', str(numero), texto)
    texto = texto.replace('vezes', '*').replace('sobre', '/').replace('mais', '+').replace('menos', '-')
    texto = re.sub(r'\s+', ' ', texto)
    return texto

def corrigir_entrada(texto, usar_correcao):
    texto = texto.lower()
    if usar_correcao:
        texto = texto.replace('mis', 'mais')
        texto = texto.replace('meos', 'menos')
        texto = texto.replace('vezs', 'vezes')
        texto = texto.replace('sobe', 'sobre')
        texto = re.sub(r'\bde\b', '', texto)  # Remove 'de' com mais cuidado
    return texto

def converter_para_expressao(texto, usar_correcao=True):
    texto = texto.lower()
    texto = corrigir_entrada(texto, usar_correcao)
    texto = tratar_numeros(texto)

    for palavra, simbolo in palavras_para_operadores.items():
        texto = re.sub(rf"\b{palavra}\b", simbolo, texto)

    for palavra, funcao in funcoes_matematicas.items():
        texto = re.sub(rf"{palavra}\s*([\w\.]+)", rf"{funcao}(\1)", texto)

    return texto.strip()

def explicar_passos(expr):
    passos = []

    def detalhar(subexpr):
        if subexpr.is_Atom:
            return subexpr

        if isinstance(subexpr, Add):
            args = subexpr.args
            descrito = " + ".join([str(detalhar(arg)) for arg in args])
            passos.append(f"Somando: {descrito}")
            return subexpr

        if isinstance(subexpr, Mul):
            args = subexpr.args
            descrito = " × ".join([str(detalhar(arg)) for arg in args])
            passos.append(f"Multiplicando: {descrito}")
            return subexpr

        if isinstance(subexpr, Pow):
            base, exp = subexpr.args
            base = detalhar(base)
            exp = detalhar(exp)
            passos.append(f"Elevando: {base} ^ {exp}")
            return subexpr

        if isinstance(subexpr, Div) or '/' in str(subexpr):
            passos.append(f"Dividindo: {str(subexpr)}")
            return subexpr

        if isinstance(subexpr, FunctionClass):
            passos.append(f"Aplicando função: {str(subexpr)}")
            return subexpr

        return subexpr

    detalhar(expr)
    return passos

def interpretar_expressao(texto, usar_correcao, modo_debug):
    texto_original = texto
    texto_corrigido = corrigir_entrada(texto, usar_correcao)
    texto_convertido = tratar_numeros(texto_corrigido)

    expressao = texto_convertido

    try:
        resultado = sympify(expressao)
        resultado_simplificado = resultado.simplify()

        resposta = "## 🔍 Interpretação Detalhada\n\n"
        resposta += f"**📥 Entrada original:** `{texto_original}`\n\n"
        resposta += f"**✅ Após correção:** `{texto_corrigido}`\n\n"
        resposta += f"**🔢 Após conversão:** `{expressao}`\n\n"

        resposta += "### 🧠 Etapas de Cálculo:\n\n"
        passos = explicar_passos(resultado)
        for i, passo in enumerate(passos, 1):
            resposta += f"{i}. {passo}\n"

        if not resultado.free_symbols:
            resultado_numerico = resultado.evalf()
            resposta += f"\n\n### 🧮 Resultado Final Numérico: `{resultado_numerico}`\n"
        else:
            resposta += f"\n\n### 🧮 Resultado Final Simbólico: `{resultado_simplificado}`\n"

        if modo_debug:
            resposta = "## 🛠️ [Modo Depuração Ativado]\n\n" + resposta

        return resposta

    except (SympifyError, SyntaxError) as e:
        return f"⚠️ Não foi possível interpretar.\n\nErro: {e}\n\nExemplos:\n- sete mais dois vezes três\n- raiz de vinte e cinco\n- x elevado a dois menos três"

# Interface Gradio
with gr.Blocks(css=".gr-button-primary {background: #10b981 !important;}") as interface:
    gr.Markdown("# 🧠 Interpretador de Expressões com IA")

    gr.Markdown("Digite uma expressão como:\n- sete mais dois vezes três\n- raiz de vinte e cinco\n- x elevado a dois menos três")

    entrada = gr.Textbox(label="Digite a expressão:", placeholder="Ex: raiz de 25 ou x mais três vezes dois")

    with gr.Row():
        usar_correcao = gr.Checkbox(label="Ativar correção gramatical", value=False)
        modo_debug = gr.Checkbox(label="Modo Depuração", value=False)

    botao = gr.Button("Interpretar", variant="primary")
    saida_texto = gr.Markdown()

    botao.click(fn=interpretar_expressao, inputs=[entrada, usar_correcao, modo_debug], outputs=saida_texto)

    gr.Markdown("---\n📘 Suporte a expressões aritméticas, raízes, potências, funções trigonométricas e expressões simbólicas!")

interface.launch()