import cv2 # type: ignore
import numpy as np # type: ignore
from PIL import Image # type: ignore
import matplotlib.pyplot as plt # type: ignore
from pathlib import Path

def load_image(img_path):
    try:
        pil_img = Image.open(img_path).convert('RGB')
        img = np.array(pil_img)
        return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

def detect_faces(img):
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_classifier.detectMultiScale(
        gray_image,
        scaleFactor=1.1,
        minNeighbors=5,  # Adjust as needed
        minSize=(30, 30),  # Adjust as needed
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    return faces

def detect_eyes(gray_face):
    eye_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
    eyes = eye_classifier.detectMultiScale(gray_face)
    return len(eyes) >= 1  # At least one eye detected

def filter_faces_with_eyes(img, faces):
    valid_faces = []
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    for (x, y, w, h) in faces:
        face_region = gray_image[y:y+h, x:x+w]
        if detect_eyes(face_region):
            valid_faces.append((x, y, w, h))
    return valid_faces

def draw_faces(img, faces, color=(0, 255, 0)):
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
    return img

# Path to the image
img_path = Path(r'C:\Users\luish\OneDrive\Área de Trabalho\FIAP\FIAP Projetos Ano 2\FASE 06\PBI\RECONHECIMENTO FACIAL\IMG_TESTE')
image_files = list(img_path.glob('*.jpg')) + list(img_path.glob('*.png'))

if not image_files:
    print("No image files found in the directory.")
    exit()

img_file = str(image_files[0])
print(f"Trying to load the image: {img_file}")

img = load_image(img_file)
if img is None:
    exit()

print("Image loaded successfully.")

faces = detect_faces(img)
print(f"Faces detected before eye filtering: {len(faces)}")

faces = filter_faces_with_eyes(img, faces)
print(f"Faces detected after eye filtering: {len(faces)}")

img_with_faces = draw_faces(img.copy(), faces)

# Display the image
plt.figure(figsize=(10, 10))
plt.imshow(cv2.cvtColor(img_with_faces, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()

# Save the image with detected faces
output_path = img_path / 'resultado_deteccao_facial_melhorado.jpg'
cv2.imwrite(str(output_path), img_with_faces)
print(f"Image with face detection saved at: {output_path}")
