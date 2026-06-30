# Deploy do Classificador de Gatos

Este projeto tem duas partes:

- **Frontend:** HTML, CSS e TypeScript compilado para `public/app.js`.
- **Backend:** `server.py`, em Python, responsável por carregar CLIP/PyTorch e classificar a imagem.

## Por que Vercel não é ideal para tudo?

Vercel é excelente para sites e frontends estáticos. O problema é que este projeto precisa rodar um backend Python com:

- PyTorch
- CLIP
- processamento de upload de imagem
- carregamento de modelo pré-treinado

Essas dependências são pesadas para um deploy serverless simples. Por isso, se subir apenas na Vercel, a tela pode abrir, mas a rota `/api/classify` não vai funcionar do jeito atual.

## Opção 1: apresentação local

É a opção mais segura para apresentar.

```bash
cd projeto_gatos_web
pip install -r requirements.txt
npm run build
python3 server.py
```

Depois abra:

```text
http://localhost:8000
```

## Opção 2: link público simples

Para um link público funcionando de verdade, hospede o app completo em um serviço que rode Python continuamente.

Boas opções:

- **Hugging Face Spaces:** boa opção para projetos com modelo de IA.
- **Render:** permite subir app Python web.
- **Railway:** também permite backend Python.

O fluxo seria:

1. Subir este repositório para o GitHub.
2. Criar um serviço Python em uma dessas plataformas.
3. Configurar o comando de start:

   ```bash
   HOST=0.0.0.0 python3 projeto_gatos_web/server.py
   ```

4. Garantir que as dependências de `projeto_gatos_web/requirements.txt` sejam instaladas.
5. Se a plataforma definir a variável `PORT`, o app já usa essa porta automaticamente.

## Opção 3: Vercel + backend separado

Se quiser usar Vercel, o caminho mais correto é separar:

- Vercel: frontend
- Render/Railway/Hugging Face Spaces: backend Python

Nesse caso, o frontend precisaria chamar a URL pública do backend em vez de usar:

```text
/api/classify
```

Por exemplo:

```text
https://seu-backend.onrender.com/api/classify
```

## Resumo prático

Para entregar e testar rápido:

```text
Use local: localhost:8000
```

Para link público com IA funcionando:

```text
Use Hugging Face Spaces, Render ou Railway
```

Para usar Vercel:

```text
Use Vercel só no frontend e deixe o backend Python em outro serviço.
```
