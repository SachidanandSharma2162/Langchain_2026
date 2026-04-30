import cv2
import numpy as np
import matplotlib.pyplot as plt

def compute_hessian_directional_derivative(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError("Image not found. Please provide a valid path.")
    img = img.astype(np.float64) / 255.0

    Ix = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
    Iy = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)

    Ixx = cv2.Sobel(Ix, cv2.CV_64F, 1, 0, ksize=3)
    Iyy = cv2.Sobel(Iy, cv2.CV_64F, 0, 1, ksize=3)
    Ixy = cv2.Sobel(Ix, cv2.CV_64F, 0, 1, ksize=3)

    T = Ixx + Iyy
    D = Ixx * Iyy - Ixy**2
    
    discriminant = np.sqrt(np.maximum((T**2) - 4*D, 0))
    
    lambda_max = (T + discriminant) / 2.0

    Vx = Ixy
    Vy = lambda_max - Ixx
    
    magnitude = np.sqrt(Vx**2 + Vy**2)
    magnitude[magnitude == 0] = 1e-8 
    Vx_norm = Vx / magnitude
    Vy_norm = Vy / magnitude

    directional_derivative = Ix * Vx_norm + Iy * Vy_norm

    result_img = cv2.normalize(directional_derivative, None, 0, 255, cv2.NORM_MINMAX)
    result_img = np.uint8(result_img)

    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.title('Original Image')
    plt.imshow(img, cmap='gray')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.title('Max Directional Derivative')
    plt.imshow(result_img, cmap='gray')
    plt.axis('off')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    compute_hessian_directional_derivative("img.jpg")