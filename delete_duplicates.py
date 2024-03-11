import os
from PIL import Image, UnidentifiedImageError
import imagehash
import matplotlib.pyplot as plt

def find_duplicates(directory):
    # make empty dictionary to save hash of images and paths to duplicates
    hash_dict = {}
    duplicate_images = {}

    # check all files in the next directory
    for filename in os.listdir(directory):
        if filename.endswith('.DS_Store'):  # skip .DS_Store
            continue
        # check if file is file (not directory)
        if os.path.isfile(os.path.join(directory, filename)):
            # make full path to the file
            image_path = os.path.join(directory, filename)
            try:
                # try to open image with PIL library
                with Image.open(image_path) as img:
                    # get hash of the image
                    hash_value = str(imagehash.phash(img))
                    # check if we have the same hash in dictionary
                    if hash_value in hash_dict:
                        # if we have the same hash, so we have duplicate
                        # get path to the original image
                        original_image = hash_dict[hash_value]
                        # check, if we have this original image in duplicates list
                        if original_image in duplicate_images:
                            # if we have -> append path for duplicate list of this original image
                            duplicate_images[original_image].append(image_path)
                        else:
                            # if we don't have -> make new in dictionary
                            duplicate_images[original_image] = [image_path]
                    else:
                        # if we don't have this hash in dictionary -> append it
                        hash_dict[hash_value] = image_path
            except UnidentifiedImageError:
                print(f"Can not to read image: {image_path}")
    # return dictionary of duplicates
    return duplicate_images


def show_duplicates(duplicate_dict):
    # check every pair in duplicates dictionary
    for original_image, duplicates in duplicate_dict.items():
        # make figure to show original and his duplicates
        plt.figure()
        # make left subplot to show original
        plt.subplot(1, len(duplicates) + 1, 1)
        # show original
        original_img = Image.open(original_image)
        plt.imshow(original_img)
        plt.axis('off')
        plt.title('Original')
        # check all duplicates of original image
        for i, duplicate_image in enumerate(duplicates):
            # make subplot to show duplicate
            plt.subplot(1, len(duplicates) + 1, i + 2)
            # show duplicate image
            img = Image.open(duplicate_image)
            plt.imshow(img)
            plt.axis('off')
            plt.title('Duplicate')
        plt.show()


def delete_duplicates(duplicate_dict, index_to_delete):
    # check every pair in duplicates dictionary
    for original_image, duplicates in duplicate_dict.items():
        # check if the index doesn't go beyond the list of duplicates
        if index_to_delete < len(duplicates):
            # get path to duplicate by index
            path_to_delete = duplicates[index_to_delete]
            # check if file exists
            if os.path.exists(path_to_delete):
                # delete file
                os.remove(path_to_delete)
                print(f"Удален дубликат: {path_to_delete}")
            else:
                print(f"Файл для удаления не найден: {path_to_delete}")
                break

directory = "images"
duplicates = find_duplicates(directory)
show_duplicates(duplicates)
delete_duplicates(duplicates, 0)
