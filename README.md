# Índice 

* [Título e Imagem de capa](#Título-e-Imagem-de-capa)
* [Índice](#índice)
* [Descrição do Projeto](#descrição-do-projeto)
* [Funcionalidades](#funcionalidades-e-demonstração-da-aplicação)
* [Tecnologias usadas](#tecnologias-utilizadas)
* [Instrução de instalação](#instalação)
* [Autores](#pessoas-desenvolvedoras)

<h1 aling="center">Interpretador de expressões matemáticas com IA</h1>
![capa do projeto](https://github.com/Luizcs-lab/LFA_Estudo_Caso2/blob/master/resources/Logo%20Interpretador%20de%20express%C3%B5es.png)

# Descrição do projeto
<p aling="center">Projeto da disciplina de Linguagens Formais e automâtos elaborado com intuito de desenvolver uma aplicação que interprete expressões algébricas escritas por extenso, usando de suporte da inteligência artificial para que faça correções gramáticais. </p>

# :hammer: Funcionalidades

As funcionalidades presentes na aplicação:
1. Correção Gramatical
    Esta corrige erros comuns que podem acontecer durante a digitação de alguma expressão.
2. Conversão de Números pro Extenso 
    Realiza a conversão das palavras fornecidas pelo usuário, reconhecendo todo tipo de número.
3. Substituição de Operadores
    Toda palavra que se refere á algum símbolo de operação será convertido respectivamente, exemplo: "mais" se transforma em +.
4. Funções Matemáticas
    Seno, Cosseno, Tangente, Logaritmos, raízes e demais outras funções conhecidas na matemática podem ser usadas pelo interpretador.
5. Modo Depuração 
    Exibe uma explicação em detalhes sobre os cálculos.
6. Interpretação e Explicação Detalhada
    Realiza um passo a passo de como ocorre os cálculos explicando as operações.
7. Integração com transformers para Correção Gramatical
    Usa modelo de correção gramatical de processamneto de linguagem natural
8. Interpretação de Expressões com Variáveis
    Qualquer que seja a expressão informada pelo usuário e eta apresente incógnitas como:"x, y, e z" serão processadas e cáculadas.                          

# Tecnologias Usadas
- SymPy
- Transformers
- Gradio

# Instrução de instalação
1. Criar e ativar um ambiente virtual:

python -m venv venv
source venv/bin/activate  # Para Linux/Mac
venv\Scripts\activate     # Para Windows

2. Instalar as dependências: Uma vez que o ambiente virtual esteja ativado, você pode instalar todas as dependências necessárias executando:

pip install gradio sympy transformers torch pandas

3. Configuração do Modelo de Correção Gramatical
Este projeto utiliza o modelo t5-small para correção gramatical. O modelo é carregado através da biblioteca transformers. A função de correção gramatical será executada utilizando a API do modelo:

python
Copiar
Editar
from transformers import pipeline
grammar_corrector = pipeline("text2text-generation", model="t5-small", tokenizer="t5-small")
Caso o modelo não esteja disponível, o projeto ainda pode operar com a correção manual definida no código.

Considerações Finais
Todas as dependências listadas são essenciais para a execução correta do projeto. Certifique-se de que todas estão instaladas e configuradas corretamente para garantir que o interpretador funcione como esperado.

Este documento fornece um resumo das bibliotecas e ferramentas necessárias para o correto funcionamento do interpretador de expressões matemáticas.

# Autores
- Cesar Luiz da Silva
- Caio de Moura Camargo
- Gabrielle de Souza Antônio
