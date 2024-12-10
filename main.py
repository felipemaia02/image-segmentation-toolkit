import os
import cv2
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from PIL import Image
from sklearn.metrics import precision_score, recall_score, f1_score

# Configuração do matplotlib
try:
    matplotlib.use('TkAgg')
except ImportError:
    matplotlib.use('Agg')

# Função para exibir e salvar imagens
def show_images(images, titles, save_path=None):
    plt.figure(figsize=(15, 5))
    for i, (img, title) in enumerate(zip(images, titles)):
        plt.subplot(1, len(images), i + 1)
        if len(img.shape) == 3:
            plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        else:
            plt.imshow(img, cmap="gray")
        plt.title(title)
        plt.axis('off')
    
    if save_path:
        plt.savefig(save_path)
        print(f"Gráficos salvos como: {save_path}")
    else:
        plt.show()

# Função para carregar e converter a imagem
def load_and_convert_image(image_path, color_space='HSV'):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Certifique-se de que a imagem {image_path} está no diretório.")
    if color_space == 'HSV':
        converted_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    elif color_space == 'LAB':
        converted_image = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)
    else:
        converted_image = image
    return image, converted_image

# Função para reconstrução do gradiente
def reconstruct_gradient(image_channel):
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    opened = cv2.morphologyEx(image_channel, cv2.MORPH_OPEN, kernel)
    closed = cv2.morphologyEx(image_channel, cv2.MORPH_CLOSE, kernel)
    reconstructed_gradient = cv2.subtract(closed.astype(np.uint8), opened.astype(np.uint8))
    return reconstructed_gradient

# Função para reduzir reflexos
def reduce_reflections(image_hsv):
    _, _, value_channel = cv2.split(image_hsv)
    reduced = cv2.medianBlur(value_channel, 5)
    image_hsv[:, :, 2] = reduced
    return image_hsv

# Função para aplicar a limiarização
def apply_threshold(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary

# Função para o método Zone Growing (simulado com gradiente morfológico)
def zone_growing(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    gradient = cv2.morphologyEx(gray, cv2.MORPH_GRADIENT, kernel)
    return gradient

# Função para aplicar a limiarização e calcular marcadores
def threshold_and_markers(gradient):
    _, binary = cv2.threshold(gradient, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    dist_transform = cv2.distanceTransform(binary, cv2.DIST_L2, 5)
    _, markers = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
    markers = np.uint8(markers)
    unknown = cv2.subtract(binary, markers)
    _, markers = cv2.connectedComponents(markers)
    markers = markers + 1
    markers[unknown == 255] = 0
    return markers

# Função para aplicar o algoritmo Watershed
def apply_watershed(image, markers):
    markers = cv2.watershed(image, markers)
    segmented_image = np.copy(image)
    segmented_image[markers == -1] = [255, 0, 0]
    return segmented_image

# Função para calcular métricas de avaliação
def evaluate_segmentation(ground_truth, segmented_image):
    if len(ground_truth.shape) == 3:
        ground_truth = cv2.cvtColor(ground_truth, cv2.COLOR_BGR2GRAY)
    if len(segmented_image.shape) == 3:
        segmented_image = cv2.cvtColor(segmented_image, cv2.COLOR_BGR2GRAY)
    
    _, ground_truth = cv2.threshold(ground_truth, 127, 1, cv2.THRESH_BINARY)
    _, segmented_image = cv2.threshold(segmented_image, 127, 1, cv2.THRESH_BINARY)
    
    precision = precision_score(ground_truth.flatten(), segmented_image.flatten())
    recall = recall_score(ground_truth.flatten(), segmented_image.flatten())
    f1 = f1_score(ground_truth.flatten(), segmented_image.flatten())
    
    return precision, recall, f1

# Função que coordena o fluxo completo
def generate_comparison(image_path, save_path=None, ground_truth_path=None):
    image, image_hsv = load_and_convert_image(image_path, color_space='HSV')
    image_hsv = reduce_reflections(image_hsv)
    gradient = reconstruct_gradient(image_hsv[:, :, 2])
    markers = threshold_and_markers(gradient)
    segmented_image = apply_watershed(image, markers)
    threshold = apply_threshold(image)
    zone_grow = zone_growing(image)

    if ground_truth_path:
        ground_truth = cv2.imread(ground_truth_path)
        if ground_truth is None:
            print(f"Ground truth não encontrado ou inválido: {ground_truth_path}")
        else:
            precision, recall, f1 = evaluate_segmentation(ground_truth, segmented_image)
            print(f"Precision: {precision:.2f}, Recall: {recall:.2f}, F1-Score: {f1:.2f}")
    
    # Comparação com 4 imagens
    show_images(
        [image, threshold, zone_grow, segmented_image],
        ["(a) Original Image", "(b) Automatic Threshold", "(c) Zone Growing", "(d) Result of the Paper Algorithm"],
        save_path=save_path
    )

# Função principal
def main():
    path = "imgs/"
    output_dir = "result/"
    ground_truth_dir = "ground_truth/"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    list_dir = os.listdir(path)

    for file in list_dir:
        file_path = os.path.join(path, file)
        ground_truth_path = os.path.join(ground_truth_dir, file)
        try:
            with Image.open(file_path):
                output_path = os.path.join(output_dir, os.path.splitext(file)[0] + "_result.png")
                generate_comparison(file_path, save_path=output_path, ground_truth_path=ground_truth_path)
        except (IOError, FileNotFoundError):
            print(f"Arquivo ignorado (não é uma imagem válida): {file_path}")

# Executar o script
if __name__ == "__main__":
    main()
