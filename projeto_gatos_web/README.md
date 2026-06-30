# Classificador de Gatos Web

App web simples com TypeScript no frontend e Python no backend.

## Como rodar

0. Instale as dependências Python:

   ```bash
   pip install -r requirements.txt
   ```

1. Compile o TypeScript:

   ```bash
   npm run build
   ```

2. Inicie o servidor:

   ```bash
   python3 server.py
   ```

3. Abra no navegador:

   ```text
   http://localhost:8000
   ```

## Como testar

- Clique nos botões `Gato 1` a `Gato 6`.
- Ou escolha uma imagem do computador/celular.
- Clique em `Analisar gato`.
- Se o CLIP não considerar a imagem como gato, aparece `Oops! Isso não é gato!`.

## Observação

O app não treina modelo. Ele usa CLIP pré-treinado para comparar a imagem com textos.

Para deploy publico, veja `DEPLOY.md`.
