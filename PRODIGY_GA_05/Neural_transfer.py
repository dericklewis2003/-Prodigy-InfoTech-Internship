# 0. Import Dependencies and Pretrained Model
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import PIL.Image
import matplotlib.pyplot as plt

# Load pre-trained model
model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')

# 1. Preprocess Image and Load
def load_image(img_path):
    img = tf.io.read_file(img_path)
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)
    img = img[tf.newaxis, :]
    return img

# 2. Visualize Output
def show_image(image):
    if len(image.shape) > 3:
        image = tf.squeeze(image, axis=0)
    plt.imshow(image)
    plt.axis('off')
    plt.show()

# 3. Stylize Image
def stylize_image(content_image, style_image):
    stylized_image = model(tf.constant(content_image), tf.constant(style_image))[0]
    return stylized_image

# Main execution
if __name__ == "__main__":
    content_path = r"C:\Users\19030\Desktop\College\Python\Prodigy Info\task 5\1280px-Gateway_Of_India.jpg"
    style_path = "style image.jpg"

    content_image = load_image(content_path)
    style_image = load_image(style_path)

    print("Content image shape:", content_image.shape)
    print("Style image shape:", style_image.shape)

    stylized_image = stylize_image(content_image, style_image)
    print("Stylized image shape:", stylized_image.shape)

    plt.figure(figsize=(12, 4))
    plt.subplot(1, 3, 1)
    show_image(content_image)
    plt.title('Content Image')
    
    plt.subplot(1, 3, 2)
    show_image(style_image)
    plt.title('Style Image')
    
    plt.subplot(1, 3, 3)
    show_image(stylized_image)
    plt.title('Stylized Image')
    
    plt.tight_layout()
    plt.show()

    print("Script execution completed. If you don't see the images, there might be an issue with your display environment.")
