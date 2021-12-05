from PIL import Image
from screeninfo import get_monitors

def resize1(file):
    image = Image.open(file)

    screen = get_monitors()[0]
    width = screen.width

    scaleFactor = image.size[0]/width

    newHeight = image.size[1]/scaleFactor

    new_image = image.resize((width,round(newHeight)))
    newName = "resizedImages/"+file.split(".jpg")[0].split("images/")[1]+'Resized.jpg'
    new_image.save(newName)


def headerSize():
    file = 'images/snes9x.jpg'
    image = Image.open(file)
    return image.size[1]

def resize2(file):
    image = Image.open(file)

    screen = get_monitors()[0]
    width = screen.width
    height = screen.height

    scaleFactorHeight = 1080/height
    scaleFactorwidth = 1920/width

    newHeight = image.size[1]/scaleFactorHeight
    newWidth = image.size[0]/scaleFactorwidth

    new_image = image.resize((round(newWidth),round(newHeight)))
    newName = "resizedImages/"+file.split(".png")[0].split("images/")[1]+'Resized.png'
    new_image.save(newName)

