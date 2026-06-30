FROM python:3.11-slim

# Dependências de sistema: git é necessário para instalar o pacote "clip" direto do GitHub
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Cria o mesmo usuário (UID 1000) que o Hugging Face Spaces usa para rodar o container
RUN useradd -m -u 1000 user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR /app

# Instala as dependências Python primeiro (melhor uso de cache do Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do projeto
COPY --chown=user:user . .

# Baixa os pesos do CLIP durante o build, para não esperar o download na primeira
# requisição (deixa o cache do modelo dentro da própria imagem)
USER user
RUN python -c "import clip, torch; clip.load('ViT-B/32', device='cpu')"

# O Hugging Face Spaces espera o app respondendo nesta porta
ENV HOST=0.0.0.0 \
    PORT=7860

EXPOSE 7860

CMD ["python", "server.py"]
