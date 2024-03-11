import hashlib
import os
import cv2
import rembg
import urllib3

def delete_background(directory):
    newDirectory = "imagesWithoutBackground"
    if not os.path.exists(newDirectory):
        os.makedirs(newDirectory)

    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            imagePath = os.path.join(directory, filename)

            image = cv2.imread(imagePath)

            if image is not None:
                # delete background rembg
                outputImage = rembg.remove(image)

                checksum = hashlib.md5(outputImage).hexdigest()
                newImagePath = os.path.join(newDirectory, f"{checksum}.png")
                cv2.imwrite(newImagePath, outputImage)
            else:
                print(f"Can not to read image: {imagePath}")

delete_background("images")
