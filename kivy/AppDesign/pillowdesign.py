# All Imports
from PIL import Image, ImageFilter, ImageEnhance

#Function
with Image.open("AppDesign/robin.jpeg") as picture:
    # picture.show()

    # black_white = picture.convert("L")
    # black_white.show()

    # mirror = picture.transpose(Image.FLIP_LEFT_RIGHT)
    # mirror.show()

    # blur = picture.filter(ImageFilter.BLUR)
    # blur.show()

    # ImageEnhance
    # contrast = ImageEnhance.Contrast(picture)
    # contrast = contrast.enhance(1.2)
    # contrast.show()
    
    color = ImageEnhance.Color(picture).enhance(2.5)
    color.show()