# Classificador de Gatos por Cor com Meme de Resposta

Projeto simples de visão computacional para classificar a aparência de um gato usando CLIP em modo zero-shot, sem treinamento.

## Como rodar

1. Abra o notebook `classificador_gatos_clip.ipynb`.
2. Rode a primeira célula de instalação se o pacote `clip` ainda não estiver instalado.
3. Rode as células em ordem.
4. Troque a variável `IMAGE_PATH` para testar outra foto.

## Ideia

O CLIP compara a imagem com frases como `a photo of an orange cat`, `a photo of a striped tabby cat` e `a photo of a black cat`.
O texto mais parecido vira a categoria final, por exemplo `gato laranja`, `gato malhado` ou `gato frajola`.

## Estrutura

- `classificador_gatos_clip.ipynb`: notebook principal.
- `gatos aleatorios/`: fotos extras de gatos para testar.
- `memes/`: memes locais usados como resposta visual.
- `generate_assets.py`: recria imagens de teste e memes que estiverem faltando.

## Observação importante

O projeto não treina uma rede neural. Ele reutiliza um modelo pré-treinado e aplica classificação zero-shot por similaridade entre imagem e texto.
