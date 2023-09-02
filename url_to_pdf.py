import requests
import os
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


#Falta la compresión por lo que van a salir archivos pesados
# Aun pueden hacerse mejoras, es un algoritmo rapido
#Segun la cantidad de paginas que tenga
cantidad_de_paginas = 337
image_paths=[]

for pagina in range(cantidad_de_paginas + 1):
    numero_formateado = f"{pagina:03}"
    # Cambiar url segun el libro
    url = f"https://libros.conaliteg.gob.mx/2023/c/S2SAA/{numero_formateado}.jpg"
    response = requests.get(url)

    image_paths.append(f'paginas/{numero_formateado}.jpg')

    if response.status_code == 200:

        nombre_archivo = f'paginas/{numero_formateado}.jpg'
        
        with open(nombre_archivo, 'wb') as archivo:
            archivo.write(response.content) 
        print(f"La imagen ha sido descargada como {numero_formateado}.jpg")
    else:
        print("No se pudo descargar la imagen. Código de estado:", response.status_code)

def convert_images_to_pdf(images, output_pdf):
    c = canvas.Canvas(output_pdf, pagesize=letter)
    
    for image_path in images:
        img = Image.open(image_path)
        img_width, img_height = img.size
        
        # Calcular la escala para ajustar la imagen a la página
        scale_width = img_width / letter[0]
        scale_height = img_height / letter[1]
        scale = max(scale_width, scale_height)
        
        # Calcular las dimensiones ajustadas de la imagen
        adjusted_width = img_width / scale
        adjusted_height = img_height / scale
        
        # Añadir la imagen al PDF con las dimensiones ajustadas
        c.drawImage(image_path, 0, 0, width=adjusted_width, height=adjusted_height)
        
        # Agregar una nueva página para la siguiente imagen
        c.showPage()
    
    c.save()

if __name__ == "__main__":

    output_pdf = "libro.pdf"
    
    convert_images_to_pdf(image_paths, output_pdf)

