
# Segmentação de Imagens Usando Watershed e Gradiente Morfológico

Este repositório contém a implementação de um pipeline de segmentação de imagens baseado no artigo **"[The Algorithm of Watershed Color Image Segmentation Based on Morphological Gradient](https://www.mdpi.com/1424-8220/22/21/8202#)"**. O código utiliza o algoritmo Watershed em conjunto com gradiente morfológico para segmentar objetos em imagens.

## Estrutura do Projeto

- `main.py`: Código principal que executa o pipeline de segmentação.
- `imgs/`: Pasta com as imagens de entrada.
- `ground_truth/`: Pasta com as imagens de referência (segmentação esperada) para avaliação de métricas.
- `result/`: Pasta onde serão salvas as imagens processadas e os resultados.

## Funcionalidades

1. Carregamento de imagens originais.
2. Conversão para o espaço de cor HSV (ou LAB, se configurado).
3. Cálculo do gradiente morfológico.
4. Aplicação do algoritmo Watershed para segmentação.
5. Avaliação de métricas (Precision, Recall, F1-Score) em relação ao ground truth.
6. Geração de imagens intermediárias e resultados segmentados.

---

## Pré-requisitos

Antes de executar o código, você precisa instalar os pacotes necessários. Certifique-se de ter o Python 3.7 ou superior instalado.

### Instalando Dependências

1. Clone este repositório:
   ```bash
   git clone https://github.com/felipemaia02/image-segmentation-toolkit.git
   cd image-segmentation-toolkit
   ```

2. Crie um ambiente virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Para Linux/Mac
   venv\Scripts\activate     # Para Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

---

## Como Rodar o Código

1. Certifique-se de que as pastas `imgs/` e `ground_truth/` contêm as imagens necessárias:
   - Coloque suas imagens de entrada na pasta `imgs/`.
   - Coloque as segmentações esperadas na pasta `ground_truth/` com os mesmos nomes das imagens em `imgs/`.

   *Tenho algumas imagens como exemplo*

2. Execute o script principal:
   ```bash
   python main.py
   ```

3. Os resultados serão salvos na pasta `result/` com o prefixo `_result` no nome do arquivo e no formato `.png`.

---

## Verificação de Conformidade com o Artigo

Este código implementa as seguintes etapas descritas no artigo **"The Algorithm of Watershed Color Image Segmentation Based on Morphological Gradient"**:

1. **Gradiente Morfológico**:
   - Realça bordas dos objetos na imagem, como descrito no artigo.

2. **Redução de Reflexos**:
   - Suaviza reflexos na imagem ao processar o canal V (valor) do espaço HSV.

3. **Segmentação com Watershed**:
   - Detecta contornos precisos com base nos gradientes e marcadores.

4. **Espaço de Cor Alternativo**:
   - Pode ser ajustado para trabalhar com HSV ou LAB, dependendo da configuração.

5. **Avaliação de Métricas**:
   - Compara o resultado da segmentação com o ground truth usando métricas de precisão (Precision), Recall e F1-Score.



## Possíveis Ajustes

- **Alterar Espaço de Cor**:
  No arquivo `main.py`, você pode mudar o espaço de cor para LAB ou HSV alterando a linha:
  ```python
  image, converted_image = load_and_convert_image(image_path, color_space='HSV')
  ```

- **Kernel do Gradiente**:
  Ajuste o tamanho do kernel para melhorar o gradiente morfológico:
  ```python
  kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
  ```

- **Métricas**:
  Certifique-se de que as imagens de `ground_truth/` correspondem corretamente às de `imgs/` para resultados mais precisos.

---

## Contribuições

Sinta-se à vontade para abrir issues ou enviar pull requests caso tenha sugestões de melhorias.
