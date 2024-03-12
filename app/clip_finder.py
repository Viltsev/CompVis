import os
from PIL import Image
import clip
import torch

source_folder = "imagesWithoutBackground"
output_folder = "clipResults"


def load_images_from_folder(folder):
    imgs = []
    for filename in os.listdir(folder):
        if filename.endswith('.DS_Store'):  # skip .DS_Store
            continue
        path = os.path.join(folder, filename)
        if os.path.isfile(path):
            img = Image.open(path)
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            imgs.append(img)
    return imgs


# Define device for calculation
device = "cuda" if torch.cuda.is_available() else "cpu"

# Download CLIP model and methods for preprocess images
model, preprocess = clip.load("ViT-B/32", device=device)

# Load images from the folder
images = load_images_from_folder(source_folder)

# Preprocess each image by preprocess method
images_processed = [
    preprocess(image) for image in images
]

# Gradients calculating off
with torch.no_grad():
    # Calculate embeddings for each image
    images_embeddings = model.encode_image(
        torch.stack(images_processed)
    )


# Search similarities between text and images
def text_image_search(query_text: str, imgs_embeddings: torch.Tensor):
    # Get embedding for requested text
    query_embeddings = model.encode_text(clip.tokenize([query_text]).to(device))
    # Calculate similarity between text and image
    similarities = query_embeddings @ imgs_embeddings.T
    return similarities


if __name__ == "__main__":
    query = "A photo of pants"
    sim = text_image_search(query, images_embeddings)
    sim_dict = dict(
        zip(range(len(sim[0])), sim[0])
    )
    # Sort images by similarity and get top 10 images
    sorted_sim = sorted(sim_dict.items(), key=lambda x: x[1], reverse=True)
    top_sim = sorted_sim[:10]

    # Folder creation
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for num, i in enumerate(top_sim):
        # Save images
        image_path = os.path.join(output_folder, f"result_{num}.jpg")
        images[i[0]].save(image_path)

    print(f"Saved top {len(top_sim)} images to {output_folder}")
