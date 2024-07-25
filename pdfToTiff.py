# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 18:56:25 2024

@author: gaosh
"""

import fitz  # PyMuPDF
from PIL import Image
import os

# Function to convert PDF to images
def pdf_to_images(pdf_path, output_folder):
    doc = fitz.open(pdf_path)  # Open the PDF file
    for page_num in range(len(doc)):  # Iterate over each page
        page = doc.load_page(page_num)  # Load the current page
        pix = page.get_pixmap()  # Render page to an image
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)  # Create a Pillow image
        img_path = os.path.join(output_folder, f"page_{page_num + 1}.png")  # Define the image path
        img.save(img_path)  # Save the image as a PNG file
    doc.close()  # Close the PDF document

# Function to convert images to a single TIFF
def images_to_tiff(image_folder, tiff_path):
    images = []
    for file_name in sorted(os.listdir(image_folder)):  # List all files in the folder
        if file_name.endswith('.png'):  # Check if the file is a PNG image
            img_path = os.path.join(image_folder, file_name)  # Get the full path of the image
            images.append(Image.open(img_path))  # Open the image and add to the list
    # Save the first image as TIFF and append the rest of the images
    images[0].save(tiff_path, save_all=True, append_images=images[1:], compression="tiff_deflate")

# Paths
pdf_path = 'example.pdf'  # Path to your PDF file
output_folder = 'output_images'  # Folder to save the images
tiff_path = 'output.tiff'  # Path to save the final TIFF file

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Convert PDF to images
pdf_to_images(pdf_path, output_folder)

# Convert images to TIFF
images_to_tiff(output_folder, tiff_path)

print(f"PDF has been converted to TIFF and saved at {tiff_path}")

