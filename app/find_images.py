import os
import cv2
from sklearn.metrics.pairwise import cosine_similarity
import logging

def load_image(file_path):
    image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    return cv2.resize(image, (100, 100)).flatten()

def calculate_cosine_distance(vector1, vector2):
    return cosine_similarity([vector1], [vector2])[0][0]

def find_similar_images(target_image_path, folder_path):
    targetVector = load_image(target_image_path)
    similarImages = []

    for file_name in os.listdir(folder_path):
        if file_name.endswith(('.jpg', '.jpeg', '.png')):
            imagePath = os.path.join(folder_path, file_name)
            imageVector = load_image(imagePath)
            similarity = calculate_cosine_distance(targetVector, imageVector)
            similarImages.append((imagePath, similarity))

    similarImages.sort(key=lambda x: x[1], reverse=True)
    return similarImages[:5]

def save_similar_images(similar_images, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i, (image_path, _) in enumerate(similar_images):
        image_name = os.path.basename(image_path)
        new_image_path = os.path.join(output_folder, f"similar_{i+1}_{image_name}")
        image = cv2.imread(image_path)
        cv2.imwrite(new_image_path, image)

sourceImage = "imagesWithoutBackground/7b6bd33145c7df017b04c41c37177d5f.png"
sourceDirectory = "imagesWithoutBackground"
outputDirectory = "./similarImages"
similarImages = find_similar_images(sourceImage, sourceDirectory)

if similarImages:
    save_similar_images(similarImages, outputDirectory)
else:
    logging.info("There are not similar images")