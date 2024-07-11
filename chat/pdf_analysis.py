import os
import base64
from pdf2image import convert_from_path, pdfinfo_from_path
from io import BytesIO


def pdf_to_base64_images(pdf_path):
    poppler_path = r'D:\temp\poppler-24.02.0\Library\bin'
    os.environ["PATH"] += os.pathsep + poppler_path
    images = convert_from_path(pdf_path, last_page=1, size=(512, 512))
    base64_images = []
    for image in images:
        width, height = image.size
        resolution = f"{width}x{height}"
        print(f"Image resolution: {resolution}")
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        base64_images.append(img_str)

    return base64_images


def test1():
    pdf_path = os.getcwd()
    pdf_path = os.path.join(pdf_path, 'test.pdf')
    base64_images = pdf_to_base64_images(pdf_path)

    if base64_images:
        print(base64_images[0])


test1()
