# Lê PDF, envia conteúdo ao modelo e pede checklist
import os
from dotenv import load_dotenv
import pdfplumber
from openai import OpenAI

load_dotenv()
API_KEY = os.getenv("OPENAI_KEY")
client = OpenAI(api_key=API_KEY)

REGRAS = [
    "Mencionar prazo",
    "Conter valor total",
    "Ter campo de assinatura",
    "Mencionar partes envolvidas"
]

def extrair_texto(path):
    with pdfplumber.open(path) as pdf:
        pages = [p.extract_text() or "" for p in pdf.pages]
    return "\n".join(pages)

def validar(path):
    texto = extrair_texto(path)[:3000]  # evita prompt gigante
    regras_texto = "\n".join("- " + r for r in REGRAS)
    prompt = f"""
Você é um validador de contratos. Use as regras:
{regras_texto}

Texto do contrato:
{texto}

Responda:
- Itens encontrados
- Itens faltando
- Riscos principais (curto)
- Sugestões de melhoria (curto)
"""
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        max_tokens=500
    )
    return resp.choices[0].message["content"]

if __name__ == "__main__":
    path = input("Caminho do PDF: ")
    print(validar(path))
