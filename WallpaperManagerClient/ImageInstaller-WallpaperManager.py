import ctypes

directory = r"c:\wallpapermanager"
imagePath = directory + r"\wall.jpg"

def changeBG(imagePath):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, imagePath, 3)
    return 0 

changeBG(imagePath)