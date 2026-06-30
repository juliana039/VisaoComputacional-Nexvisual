# Deploy do classificador de gatos

Este app tem duas partes:

- frontend estatico em TypeScript, dentro de `public/`;
- backend Python em `server.py`, que carrega CLIP/PyTorch e classifica a imagem.

## Sobre Vercel

Vercel e otimo para frontend, mas nao e a melhor opcao para este projeto completo porque o backend usa CLIP/PyTorch, baixa/carrega modelo pesado e precisa processar imagem. Em Vercel puro, o frontend ate pode abrir, mas a classificacao em `/api/classify` nao ficaria funcionando do jeito atual.

## Melhor caminho para teste publico

Para a apresentacao, as opcoes mais praticas sao:

1. Rodar localmente e mostrar pelo navegador em `http://localhost:8000`.
2. Subir o codigo no GitHub com instrucoes de execucao.
3. Se precisar de link publico funcional, hospedar o backend em um servico que aceite Python com modelo pesado, como Hugging Face Spaces, Render ou Railway. O frontend pode ficar junto nesse servico ou separado na Vercel apontando para a URL do backend.

## Como testar localmente

```bash
cd projeto_gatos_web
npm run build
python3 server.py
```

Abra:

```text
http://localhost:8000
```

