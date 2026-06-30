import json
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parent
NOTEBOOK = ROOT / "classificador_gatos_clip.ipynb"


def md(source: str) -> dict:
    normalized = textwrap.dedent(source).strip()
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": normalized.splitlines(keepends=True),
    }


def code(source: str) -> dict:
    normalized = textwrap.dedent(source).strip()
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": normalized.splitlines(keepends=True),
    }


cells = [
    md(
        """
        # Classificador de Gatos por Cor com Meme de Resposta

        Este projeto usa **visão computacional multimodal** com o modelo pré-treinado **CLIP**.

        A ideia é simples: em vez de treinar uma rede neural do zero, comparamos a foto enviada com frases como `a photo of an orange cat` e `a photo of a black and white tuxedo cat`.

        O texto mais parecido vira a categoria final. Depois disso, o notebook mostra um meme local relacionado ao resultado.
        """
    ),
    md(
        """
        ## Instalação

        Rode a célula abaixo apenas se o pacote `clip` ainda não estiver instalado.

        Como o modelo é pré-treinado, a primeira execução pode baixar pesos do CLIP.
        """
    ),
    code(
        """
        # Se aparecer erro "No module named 'clip'", descomente e rode esta linha:
        # %pip install git+https://github.com/openai/CLIP.git
        """
    ),
    md(
        """
        ## Imports e configuração

        O notebook tenta encontrar as pastas `gatos aleatorios/` e `memes/` tanto quando é aberto de dentro da pasta do projeto quanto quando é aberto a partir da pasta principal dos laboratórios.
        """
    ),
    code(
        """
        from pathlib import Path

        import matplotlib.pyplot as plt
        import torch
        from PIL import Image

        try:
            import clip
        except ModuleNotFoundError as error:
            raise ModuleNotFoundError(
                "O pacote CLIP ainda não está instalado. Rode a célula de instalação acima: "
                "%pip install git+https://github.com/openai/CLIP.git"
            ) from error


        PROJECT_DIR = Path.cwd()
        if not (PROJECT_DIR / "memes").exists() and (PROJECT_DIR / "projeto_gatos_clip" / "memes").exists():
            PROJECT_DIR = PROJECT_DIR / "projeto_gatos_clip"

        RANDOM_CATS_DIR = PROJECT_DIR / "gatos aleatorios"
        MEMES_DIR = PROJECT_DIR / "memes"

        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Dispositivo usado: {device}")
        print(f"Pasta do projeto: {PROJECT_DIR}")
        """
    ),
    md(
        """
        ## Categorias do projeto

        Cada categoria tem:

        - um prompt em inglês, porque o CLIP costuma responder melhor aos textos em inglês;
        - um rótulo em português para apresentar;
        - um meme local associado.

        A função `find_meme` aceita `.png`, `.jpg` ou `.jpeg`, então você pode trocar os memes sem precisar alterar o código.
        """
    ),
    code(
        """
        def find_meme(name):
            for extension in (".png", ".jpg", ".jpeg"):
                candidate = MEMES_DIR / f"{name}{extension}"
                if candidate.exists():
                    return candidate
            raise FileNotFoundError(f"Nenhum meme encontrado para {name} em {MEMES_DIR}")


        CATEGORIES = [
            {
                "key": "laranja",
                "label": "gato laranja",
                "prompt": "a photo of an orange cat",
                "meme": find_meme("laranja"),
            },
            {
                "key": "preto",
                "label": "gato preto",
                "prompt": "a photo of a black cat",
                "meme": find_meme("preto"),
            },
            {
                "key": "frajola",
                "label": "gato frajola",
                "prompt": "a photo of a black and white tuxedo cat",
                "meme": find_meme("frajola"),
            },
            {
                "key": "malhado",
                "label": "gato malhado",
                "prompt": "a photo of a striped tabby cat",
                "meme": find_meme("malhado"),
            },
            {
                "key": "cinza",
                "label": "gato cinza",
                "prompt": "a photo of a gray cat",
                "meme": find_meme("cinza"),
            },
            {
                "key": "branco",
                "label": "gato branco",
                "prompt": "a photo of a white cat",
                "meme": find_meme("branco"),
            },
            {
                "key": "siames",
                "label": "gato siamês",
                "prompt": "a photo of a siamese cat",
                "meme": find_meme("siames"),
            },
            {
                "key": "tricolor",
                "label": "gato tricolor",
                "prompt": "a photo of a calico cat",
                "meme": find_meme("tricolor"),
            },
        ]

        for category in CATEGORIES:
            print(f"{category['label']}: {category['prompt']}")
        """
    ),
    md(
        """
        ## Carregar o modelo CLIP

        Aqui está a parte principal de reutilização de modelo pré-treinado.

        `ViT-B/32` é um modelo CLIP já treinado para aproximar imagens e textos no mesmo espaço de representação.
        """
    ),
    code(
        """
        model, preprocess = clip.load("ViT-B/32", device=device)
        model.eval()

        text_tokens = clip.tokenize([category["prompt"] for category in CATEGORIES]).to(device)

        print("Modelo CLIP carregado com sucesso.")
        """
    ),
    md(
        """
        ## Funções de classificação

        A função principal recebe uma imagem, calcula a similaridade com cada prompt e devolve um ranking.

        Também existe uma checagem simples para avisar quando a imagem talvez nem seja de gato. Ela compara a imagem com prompts gerais como `a photo of a cat`, `a photo of a dog` e `a photo of a landscape`.
        """
    ),
    code(
        """
        GENERAL_PROMPTS = [
            ("cat", "a photo of a cat"),
            ("dog", "a photo of a dog"),
            ("person", "a photo of a person"),
            ("landscape", "a photo of a landscape"),
            ("food", "a photo of food"),
            ("car", "a photo of a car"),
        ]

        general_tokens = clip.tokenize([prompt for _, prompt in GENERAL_PROMPTS]).to(device)


        def load_image_tensor(image_path):
            image = Image.open(image_path).convert("RGB")
            tensor = preprocess(image).unsqueeze(0).to(device)
            return image, tensor


        def softmax_probs(image_tensor, tokens):
            with torch.no_grad():
                logits_per_image, _ = model(image_tensor, tokens)
                probs = logits_per_image.softmax(dim=-1).cpu().numpy()[0]
            return probs


        def classify_cat_color(image_path, top_k=3):
            image_path = Path(image_path)
            image, image_tensor = load_image_tensor(image_path)
            probs = softmax_probs(image_tensor, text_tokens)

            ranking = []
            for category, probability in zip(CATEGORIES, probs):
                ranking.append(
                    {
                        "label": category["label"],
                        "prompt": category["prompt"],
                        "probability": float(probability),
                        "meme": category["meme"],
                    }
                )

            ranking = sorted(ranking, key=lambda item: item["probability"], reverse=True)
            return image, ranking[:top_k], ranking


        def check_if_cat(image_path):
            _, image_tensor = load_image_tensor(image_path)
            probs = softmax_probs(image_tensor, general_tokens)
            ranking = [
                {"key": key, "prompt": prompt, "probability": float(probability)}
                for (key, prompt), probability in zip(GENERAL_PROMPTS, probs)
            ]
            return sorted(ranking, key=lambda item: item["probability"], reverse=True)
        """
    ),
    md(
        """
        ## Visualizar um resultado

        Primeiro definimos a função que mostra a imagem de entrada, o ranking e o meme de resposta.
        """
    ),
    code(
        """
        def show_result(image_path):
            image_path = Path(image_path)
            image, top3, ranking = classify_cat_color(image_path, top_k=3)
            broad_ranking = check_if_cat(image_path)
            winner = top3[0]

            print(f"Imagem analisada: {image_path}")
            print(f"Categoria escolhida: {winner['label']} ({winner['probability']:.2%})")
            print()
            print("Top 3 categorias de cor/aparência:")
            for position, item in enumerate(top3, start=1):
                print(f"{position}. {item['label']} - {item['probability']:.2%}")

            print()
            print("Checagem geral da imagem:")
            for position, item in enumerate(broad_ranking[:3], start=1):
                print(f"{position}. {item['prompt']} - {item['probability']:.2%}")

            if broad_ranking[0]["key"] != "cat":
                print()
                print("Aviso: o CLIP não achou que 'cat' fosse a descrição geral mais parecida.")
                print("Isso é útil para discutir limitação: com prompts só de gato, ele sempre escolhe algum tipo de gato.")

            meme = Image.open(winner["meme"]).convert("RGB")

            fig, axes = plt.subplots(1, 2, figsize=(12, 5))
            axes[0].imshow(image)
            axes[0].set_title("Imagem de entrada")
            axes[0].axis("off")

            axes[1].imshow(meme)
            axes[1].set_title(f"Meme: {winner['label']}")
            axes[1].axis("off")

            plt.tight_layout()
            plt.show()

            return ranking
        """
    ),
    md(
        """
        ## Escolher imagem de teste

        Mude apenas o valor de `NUMERO_DO_GATO` entre `1` e `6` para testar as fotos da pasta `gatos aleatorios/`.
        """
    ),
    code(
        """
        NUMERO_DO_GATO = 1  # mude aqui: 1, 2, 3, 4, 5 ou 6

        def find_random_cat_image(number):
            matches = sorted(RANDOM_CATS_DIR.glob(f"{number}.*"))
            matches = [path for path in matches if path.suffix.lower() in {".jpg", ".jpeg", ".png"}]
            if not matches:
                raise FileNotFoundError(
                    f"Não encontrei a imagem {number} em {RANDOM_CATS_DIR}. "
                    "Confira se existe um arquivo como 1.jpeg, 2.jpg ou 3.png."
                )
            return matches[0]


        IMAGE_PATH = find_random_cat_image(NUMERO_DO_GATO)
        print(f"Imagem escolhida: {IMAGE_PATH}")
        """
    ),
    md(
        """
        ## Rodar classificação

        Depois de escolher o número acima, rode esta célula para ver o resultado.
        """
    ),
    code(
        """
        ranking = show_result(IMAGE_PATH)
        """
    ),
    md(
        """
        ## Testes rápidos

        Esta célula roda as fotos colocadas em `gatos aleatorios/`.
        """
    ),
    code(
        """
        TEST_IMAGES = []

        if RANDOM_CATS_DIR.exists():
            random_cat_images = sorted(
                [
                    path
                    for path in RANDOM_CATS_DIR.iterdir()
                    if path.suffix.lower() in {".jpg", ".jpeg", ".png"}
                ]
            )
            TEST_IMAGES.extend(random_cat_images)

        for test_image in TEST_IMAGES:
            _, top3, _ = classify_cat_color(test_image, top_k=3)
            broad = check_if_cat(test_image)
            print("-" * 72)
            print(test_image.name)
            print(f"resultado: {top3[0]['label']} ({top3[0]['probability']:.2%})")
            print(f"checagem geral: {broad[0]['prompt']} ({broad[0]['probability']:.2%})")
            print("top 3:", ", ".join(f"{item['label']} {item['probability']:.1%}" for item in top3))
        """
    ),
    md(
        """
        ## Conclusão para apresentação

        - O projeto usa visão computacional porque analisa pixels de uma imagem.
        - O projeto usa multimodalidade porque compara imagem com textos.
        - O modelo usado já vem pré-treinado; não foi necessário criar dataset nem treinar rede neural.
        - O resultado é probabilístico e relativo aos prompts escolhidos.
        - Uma limitação importante é que o fundo, iluminação ou estilo da imagem pode confundir a classificação.
        """
    ),
]


notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.14.5",
        },
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}


NOTEBOOK.write_text(json.dumps(notebook, ensure_ascii=False, indent=2), encoding="utf-8")
print(NOTEBOOK)
