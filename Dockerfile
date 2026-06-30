FROM python:3.11-slim

# Dependências de sistema: git é necessário para instalar o pacote "clip" direto do GitHub
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Cria um usuário sem privilégios para rodar a aplicação (boa prática; a
# Render não exige um UID fixo como o Hugging Face exigia)
RUN useradd -m appuser
ENV HOME=/home/appuser \
    PATH=/home/appuser/.local/bin:$PATH

WORKDIR /app

# Instala as dependências Python primeiro (melhor uso de cache do Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do projeto
COPY --chown=appuser:appuser . .

# Baixa os pesos do CLIP durante o build, para não esperar o download na primeira
# requisição (deixa o cache do modelo dentro da própria imagem)
USER appuser
RUN python -c "import clip, torch; clip.load('ViT-B/32', device='cpu')"

# A Render injeta a variável PORT automaticamente em tempo de execução — o
# server.py já lê HOST/PORT do ambiente, só garantimos o HOST aqui
ENV HOST=0.0.0.0

# Apenas documentativo: a porta real em runtime vem de $PORT, definida pela Render
EXPOSE 10000

CMD ["python", "server.py"]
