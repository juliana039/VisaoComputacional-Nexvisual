# Classificador de Gatos Web

App web com TypeScript (compilado) no frontend e Python no backend.

A classificação usa o modelo pré-treinado **CLIP** (`ViT-B/32`) rodando
localmente no servidor — não há chamada a nenhuma API externa de IA.

## Estrutura esperada do projeto

```
.
├── Dockerfile
├── requirements.txt
├── server.py
└── public/
    ├── index.html
    ├── styles.css
    ├── app.js
    ├── gatos/
    │   ├── 1.jpeg
    │   ├── 2.jpg
    │   ├── 3.png
    │   ├── 4.jpg
    │   ├── 5.png
    │   └── 6.png
    └── memes/
        ├── laranja.(png|jpg|jpeg)
        ├── preto.(png|jpg|jpeg)
        ├── frajola.(png|jpg|jpeg)
        ├── malhado.(png|jpg|jpeg)
        ├── cinza.(png|jpg|jpeg)
        ├── branco.(png|jpg|jpeg)
        ├── siames.(png|jpg|jpeg)
        └── tricolor.(png|jpg|jpeg)
```

O `server.py` serve tudo dentro de `public/` como arquivos estáticos e expõe
o endpoint `POST /api/classify`.

## Como rodar localmente

```bash
pip install -r requirements.txt
python server.py
```

Abra `http://127.0.0.1:8000` (ou a porta definida na variável `PORT`).

## Como rodar na Render

1. Suba este projeto para um repositório no GitHub.
2. Em [dashboard.render.com](https://dashboard.render.com), clique em **New → Web Service**.
3. Conecte sua conta do GitHub e selecione o repositório.
4. A Render detecta o `Dockerfile` na raiz automaticamente. Escolha o
   **Instance Type: Free** e clique em criar.
5. O build baixa os pesos do CLIP (~350MB) durante a etapa de build, então a
   primeira build demora alguns minutos.
6. Pronto — o app fica disponível em `https://SEU-SERVICO.onrender.com`.
   A cada `git push` para a branch principal, a Render builda e publica
   automaticamente de novo.

**Atenção:** o plano gratuito da Render tem só 512MB de RAM, o que é
apertado para PyTorch + CLIP. Se o serviço cair com erro de memória nos
logs, considere o plano pago Starter (512MB→mais folga real) ou trocar
para um modelo CLIP mais leve.

## Observação

O app não treina modelo nenhum. Ele usa CLIP pré-treinado para comparar a
imagem enviada com frases descritivas em inglês (ex: `a photo of an orange cat`)
e escolhe a categoria mais parecida.
