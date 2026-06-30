# Avisos para rodar os laboratorios no Mac

Eu ajustei os caminhos de imagens, videos e alguns arquivos locais para o caminho real deste computador:

`/Users/julianapereirademagalhaes/Downloads/visaocomp`

Pontos que talvez ainda precisem de atencao no Mac, mas que eu nao modifiquei automaticamente:

| Arquivo | Celula | Comando/trecho | Observacao |
| --- | ---: | --- | --- |
| `M6A3 - Sistemas de Monitoramento de Experimentos 1.ipynb` | 5 | `!pip install torch torchvision tensorboard` | Em notebook, se der conflito de ambiente, prefira `%pip install torch torchvision tensorboard`. |
| `OneDrive_1_1-21-2026/VC_M1A3 - Visualização de Imagens/VC_M1A3 - Visualização de Imagens.ipynb` | 4 | `!pip3 install matplotlib` | Pode usar `%pip install matplotlib` para instalar no kernel aberto. |
| `OneDrive_1_1-21-2026/VC_M1A4 - Introdução a OpenCV/M1A4 - Introdução a OpenCV.ipynb` | 4 | `!pip3 install opencv-python` | Pode usar `%pip install opencv-python`. |
| `OneDrive_1_1-21-2026/VC_M1A5 - Operações Básicas em Imagens/VC_M1A5 - Operações Básicas em Imagens.ipynb` | 5 | `!pip3 install opencv-python` | Pode usar `%pip install opencv-python`. |
| `OneDrive_1_1-21-2026/VC_M1A7 - Fundamentos de Filtros Espaciais e Convoluções/VC_M1A7 - Fundamentos de Filtros Espaciais e Convoluções.ipynb` | 5 | `!pip3 install opencv-python` | Pode usar `%pip install opencv-python`. |
| `OneDrive_2_1-21-2026/VC_M2A1 - Detecção e Extração de Características/VC_M2A1 - Detecção e Extração de Características.ipynb` | 5 | `!pip3 install opencv-python` | Pode usar `%pip install opencv-python`. |
| `OneDrive_2_1-21-2026/VC_M2A2 - Correspondências de Características/M2A2 - Correspondências de Características.ipynb` | 5 | `!pip3 install opencv-python` | Pode usar `%pip install opencv-python`. |
| `OneDrive_2_1-21-2026/VC_M2A10 - Modelos Pré-Treinados/M2A10 - Modelos Pré-Treinados.ipynb` | 5 | `!pip3 install torch torchvision` | Pode usar `%pip install torch torchvision`. |
| `OneDrive_3_1-21-2026/VC_M3A3 - Transfer learning e Refinamento com Redes Pré-treinadas/VC_M3A3 - Transfer learning e Refinamento com Redes Pré-treinadas .ipynb` | 5 | `!pip install torch torchvision` | Pode usar `%pip install torch torchvision`. |
| `OneDrive_3_1-21-2026/VC_M3A3 - Transfer learning e Refinamento com Redes Pré-treinadas/VC_M3A3 - Transfer learning e Refinamento com Redes Pré-treinadas .ipynb` | 13, 14, 15 | `num_workers=1` ou `num_workers=4` | Se o DataLoader travar no Mac/Jupyter, teste `num_workers=0`. |
| `OneDrive_3_1-21-2026/VC_M3A5 - Detecção de objetos/M3A5 - Detecção de objetos.ipynb` | 5, 11 | `!pip install ultralytics` e `YOLO("yolo11n.pt")` | O peso `yolo11n.pt` sera baixado automaticamente na primeira execucao, se houver internet. |
| `OneDrive_3_1-21-2026/VC_M3A6 - Segmentação semântica/VC_M3A6 - Segmentação semântica.ipynb` | 5, 11 | `!pip install ultralytics` e `SAM("sam_b.pt")` | O peso `sam_b.pt` sera baixado automaticamente na primeira execucao, se houver internet. |
| `OneDrive_4_1-21-2026/VC_M4A2 - GANs/VC_M4A2 - GANs .ipynb` | 5 | `!pip install torch torchvision` | Pode usar `%pip install torch torchvision`. |
| `OneDrive_4_1-21-2026/VC_M4A5 - Fundamentos de Modelos Multimodais/VC_M4A5 - Fundamentos de Modelos Multimodais.ipynb` | 5 | `!pip install git+https://github.com/openai/CLIP.git` | Precisa de internet e Git instalado. Em notebook, pode usar `%pip install git+https://github.com/openai/CLIP.git`. |
| `OneDrive_4_1-26-2026/VC_Desafio_4_Gabarito.ipynb` | 3 | `!pip install ultralytics matplotlib torch` | Pode usar `%pip install ultralytics matplotlib torch`. |
| `OneDrive_5_1-21-2026/VC_M5A1 - Inspeção Visual de Itens em Esteira de Manufatura/VC_M5A1 - Inspeção Visual de Itens em Esteira de Manufatura.ipynb` | 11 | `data="./yolo_train.yaml"` | Este laboratorio espera arquivos de treino como `data/fruits/classes.txt`; eles nao aparecem na pasta atual. |
| `OneDrive_5_1-21-2026/VC_M5A2 - Reconhecimento de Texto/VC_M5A2 - Reconhecimento de Texto.ipynb` | 5 | `!pip install easyocr` | Precisa de internet; o EasyOCR tambem baixa modelos na primeira execucao. |
| `OneDrive_5_1-21-2026/VC_M5A3 - Identificação de elementos visuais em UI de aplicativos/VC_M5A3 - Identificação de elementos visuais em UI de aplicativos.ipynb` | 5 | `!pip install torch torchvision datasets tqdm ipywidgets` | Pode usar `%pip install ...`; alguns datasets baixam dados na primeira execucao. |
| `OneDrive_5_1-21-2026/VC_M5A4 - Sistema de vigilância/VC_M5A4 - Sistema de vigilância.ipynb` | 6 | `!pip install torch torchvision datasets tqdm ipywidgets torchcodec torchvideo ffmpeg-python av` | Em Mac, se `torchcodec`, `torchvideo` ou `av` falharem, pode ser dependencia de compilacao/FFmpeg. |
| `OneDrive_5_1-21-2026/VC_M5A5 - Segmentação de falhas em tecidos/VC_M5A5 - Segmentação de falhas em tecidos.ipynb` | 5 | `!pip install torch torchvision tqdm ipywidgets` | Pode usar `%pip install ...`. |
| `OneDrive_5_1-21-2026/VC_M5A6 - Detecção de faixas para veículos autônomos/VC_M5A6 - Detecção de faixas para veículos autônomos.ipynb` | 5 | `!pip install torch torchvision datasets tqdm ipywidgets` | Pode usar `%pip install ...`. |

Observacao geral: linhas com `device = "cuda" if torch.cuda.is_available() else "cpu"` nao precisam ser trocadas no Mac. Elas simplesmente caem para CPU se nao houver GPU CUDA.

