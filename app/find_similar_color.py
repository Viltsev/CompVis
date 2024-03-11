import os
import cv2
from colormath.color_diff import delta_e_cie2000
from colormath.color_objects import LabColor
from PIL import Image, UnidentifiedImageError
from colormath.color_conversions import convert_color
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np


def asscalar_method(a):
    return a.item()

setattr(np, "asscalar", asscalar_method)

def calculate_average_color(image):
    # Calculate average color in rectangle
    averageColor = np.mean(image, axis=(0, 1))
    return LabColor(averageColor[0], averageColor[1], averageColor[2])

# Load images and calculate their averages colors
imageDirectory = 'imagesWithoutBackground'
imageFiles = os.listdir(imageDirectory)
imagePaths = [os.path.join(imageDirectory, f) for f in imageFiles]
images = []
averageColors = []
for image_path in imagePaths:
    if image_path.endswith('.DS_Store'):  # skip .DS_Store
        continue
    image = cv2.imread(image_path)
    images.append(image)
    averageColor = calculate_average_color(image)
    averageColors.append(averageColor)

# Search similar images by color
def search_similar_colors(query_color, average_colors):
    similarities = []
    for color in average_colors:
        similarity = delta_e_cie2000(query_color, color)
        similarities.append(similarity)
    return similarities

# Find similar images by color (main method)
def search_image(r, g, b):
    # RGB to Lab
    rgbColor = np.array([r, g, b], dtype=np.uint8)
    sourceColor = LabColor(rgbColor[2], rgbColor[1], rgbColor[0])
    labColor = convert_color(sourceColor, LabColor)

    queryColor = LabColor(labColor.lab_l, labColor.lab_a, labColor.lab_b)
    similarities = search_similar_colors(queryColor, averageColors)

    # amount of similar images
    amountImages = 15
    similarImagesInx = np.argsort(similarities)[:amountImages]
    outputDirectory = 'similarColors'

    if not os.path.exists(outputDirectory):
        os.makedirs(outputDirectory)

    for idx in similarImagesInx:
        image_filename = os.path.join(outputDirectory, f'similar_image_{idx}.jpg')
        cv2.imwrite(image_filename, images[idx])
        print(f'Saved similar image {idx} to {image_filename}')

search_image(0, 255, 0)













