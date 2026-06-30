# VisaoComputacional-Nexvisual

Repositório com laboratórios de visão computacional, desafios práticos e um projeto final simples usando modelo multimodal pré-treinado.

O destaque do repositório é o **Classificador de Gatos por Cor**, um projeto que recebe uma imagem, usa o modelo **CLIP** em modo zero-shot e tenta identificar visualmente o tipo/cor do gato. O sistema também mostra um meme correspondente ao resultado.

## Projeto principal

### Classificador de Gatos por Cor

O projeto classifica imagens em categorias como:

- gato laranja
- gato preto
- gato frajola
- gato malhado
- gato cinza
- gato branco
- gato siamês
- gato tricolor

Ele também tenta detectar quando a imagem enviada **não parece ser um gato**, retornando a mensagem:

```text
Oops! Isso não é gato!
```

## Como funciona

O projeto **não treina um modelo do zero**.

Ele reutiliza o **CLIP**, um modelo pré-treinado que entende imagens e textos no mesmo espaço de comparação. A imagem enviada é comparada com frases fixas, por exemplo:

```text
a photo of an orange cat
a photo of a black cat
a photo of a striped tabby cat
a photo of a siamese cat
```

A frase mais parecida com a imagem vira o resultado final. Por isso esse projeto é um exemplo de:

- visão computacional
- modelo multimodal
- classificação zero-shot
- reutilização de modelo pré-treinado

## Estrutura do repositório

```text
.
├── projeto_gatos_clip/
│   ├── classificador_gatos_clip.ipynb
│   ├── gatos aleatorios/
│   ├── memes/
│   └── requirements.txt
│
├── projeto_gatos_web/
│   ├── public/
│   ├── src/
│   ├── server.py
│   ├── requirements.txt
│   ├── package.json
│   └── DEPLOY.md
│
└── projetos_aulas/
    └── laboratórios e desafios do curso
```

## Versão notebook

A versão em notebook está em:

```text
projeto_gatos_clip/classificador_gatos_clip.ipynb
```

Para instalar as dependências:

```bash
cd projeto_gatos_clip
pip install -r requirements.txt
```

Depois, abra o notebook e rode as células em ordem.

## Versão web

A versão web está em:

```text
projeto_gatos_web/
```

Ela tem:

- frontend simples em TypeScript
- backend em Python
- upload de imagem
- botões com imagens prontas
- preview da imagem
- resultado com ranking de confiança
- meme correspondente à categoria

### Rodar localmente

Entre na pasta do projeto web:

```bash
cd projeto_gatos_web
```

Instale as dependências Python:

```bash
pip install -r requirements.txt
```

Compile o TypeScript:

```bash
npm run build
```

Inicie o servidor:

```bash
python3 server.py
```

Abra no navegador:

```text
http://localhost:8000
```

## Como testar

Na versão web:

1. Clique em **Escolher imagem** para enviar uma foto do computador.
2. Ou use os botões **Gato 1** a **Gato 6**.
3. Clique em **Analisar gato**.
4. Veja a categoria escolhida, o ranking e o meme.

Testes interessantes:

- foto clara de gato laranja
- foto de gato preto
- foto de gato preto e branco/frajola
- foto de gato malhado
- imagem que não seja gato
- foto com fundo colorido, para observar possíveis confusões do modelo

## Deploy: dá para colocar na Vercel?

Parcialmente.

A **Vercel funciona muito bem para frontend**, mas este projeto completo também tem um backend Python que carrega **CLIP + PyTorch**, que são dependências pesadas. Por isso, subir tudo diretamente na Vercel não é o caminho mais simples.

### Melhor opção para apresentação

Para apresentar hoje, o caminho mais seguro é:

```bash
cd projeto_gatos_web
python3 server.py
```

E mostrar em:

```text
http://localhost:8000
```

### Melhor opção para link público

Para um link público funcional, o ideal é hospedar o backend em um serviço que aceite Python com modelo pesado, como:

- Hugging Face Spaces
- Render
- Railway

Depois disso, a Vercel pode hospedar apenas o frontend, apontando para a URL do backend.

Mais detalhes estão em:

```text
projeto_gatos_web/DEPLOY.md
```

## Tecnologias usadas

- Python
- PyTorch
- CLIP
- Pillow
- TypeScript
- HTML
- CSS
- Jupyter Notebook

## Observação

O classificador pode errar algumas imagens. Isso é esperado porque ele não foi treinado especificamente para este conjunto de gatos. A proposta do projeto é demonstrar como um modelo pré-treinado pode ser reutilizado rapidamente para resolver uma tarefa visual de forma simples e apresentável.
