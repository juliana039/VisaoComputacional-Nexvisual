# Classificador de Gatos Web

App web com TypeScript no frontend e Python no backend. A classificação
usa o modelo pré-treinado **CLIP** (`ViT-B/32`) rodando localmente no
servidor — não há chamada a nenhuma API externa de IA.

## Estrutura do projeto

```
projeto_gatos_web/
├── Dockerfile
├── requirements.txt      # dependências Python (torch, clip, Pillow)
├── package.json          # dependências e scripts do TypeScript
├── server.py             # servidor HTTP (arquivos estáticos + /api/classify)
├── src/                  # código-fonte TypeScript
├── scripts/
└── public/               # gerado/servido pelo server.py
    ├── index.html
    ├── styles.css
    ├── app.js             # gerado a partir de src/ pelo build do TypeScript
    ├── gatos/             # imagens de exemplo (1.jpeg a 6.png)
    └── memes/             # memes exibidos no resultado, por categoria
```

## Pré-requisitos

- Python 3.10+ instalado (no Mac, use sempre `pip3` e `python3`, não `pip`/`python`)
- Node.js e npm instalados

## Como rodar localmente

1. **Entre na pasta do projeto:**

   ```bash
   cd projeto_gatos_web
   ```

2. **Instale as dependências Python:**

   ```bash
   pip3 install -r requirements.txt
   ```

   Isso instala PyTorch, o pacote `clip` (OpenAI) e Pillow. A primeira
   execução do servidor vai baixar os pesos do modelo CLIP
   (~350MB) automaticamente — pode demorar alguns minutos.

3. **Instale as dependências do TypeScript e compile:**

   ```bash
   npm install
   npm run build
   ```

   Isso gera/atualiza `public/app.js` a partir do código em `src/`.

4. **Inicie o servidor:**

   ```bash
   python3 server.py
   ```

   Você deve ver no terminal:

   ```text
   Servidor rodando em http://127.0.0.1:8000
   Pressione Ctrl+C para parar.
   ```

5. **Abra no navegador:**

   ```text
   http://localhost:8000
   ```

## Como testar

- Clique nos botões `Gato 1` a `Gato 6` para testar com imagens prontas.
- Ou escolha uma imagem do seu computador pelo botão de upload.
- Clique em `Analisar gato`.
- Se o CLIP não considerar a imagem como gato, aparece `Oops! Isso não é gato!`.

## Problemas comuns

- **`pip: command not found`** → use `pip3` no lugar de `pip` (Mac).
- **Erro ao colar caminho de arquivo copiado do Finder** → remova as barras
  invertidas (`\`) que aparecem antes dos espaços no caminho antes de usar
  a string em Python.
- **Porta 8000 já em uso** → defina outra porta antes de rodar:

  ```bash
  PORT=8001 python3 server.py
  ```

- **Servidor lento na primeira classificação** → normal, é o momento em
  que o CLIP é carregado na memória pela primeira vez.

## Observação

O app não treina nenhum modelo. Ele usa o CLIP pré-treinado para comparar
a imagem enviada com frases descritivas em inglês (ex: `a photo of an
orange cat`) e escolhe a categoria mais parecida — classificação
zero-shot, sem fine-tuning.
