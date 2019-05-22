import socket 
import os 
import time
import threading
import datetime
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import shutil

def send_wallpaper():
    while True:

        create_wallpaper()
        lis = os.listdir('C:\\WallpaperManager\\WallpaperManagerServer\\s_photo')
        fileReadyToDelete = 0 
        if not lis:
            print ('файл не найден, ждем')
        else:
            exec(open("C:\\WallpaperManager\\WallpaperManagerServer\\wallpapermanagerconfig.conf").read())
            for addres in addres_client:
                try:
                    sock = socket.socket()         
                    port = 9090                
                    sock.connect((addres, port))
                    file = open('C:\\WallpaperManager\\WallpaperManagerServer\\s_photo\\send.jpg','rb')
                    print ('Start Sending...')
                    l = file.read(1024)

                    while (l):
                        #print ('Sending...')
                        sock.send(l)
                        l = file.read(1024)

                    file.close()
                    print ("Done Sending")
                    sock.shutdown(socket.SHUT_WR)                   
                    sock.close
                    fileReadyToDelete += 1                
                except Exception:
                    print('Соединения с клиентом ' + addres + ' не установлено')
                    fileReadyToDelete += 1 
                
                if fileReadyToDelete == len(addres_client):
                    os.remove('C:\\WallpaperManager\\WallpaperManagerServer\\s_photo\\send.jpg')

        time.sleep(4)
        

def create_wallpaper():
    lis = os.listdir('C:\\WallpaperManager\\WallpaperManagerServer\\photo')
    if not lis:
        print ('Папка пуста')
        time.sleep(4)
    else:    
        for file in lis:
            if file == "send.jpg":
                print ("Есть неотправленные файлы, жду")
                break
        path = ("C:\\WallpaperManager\\WallpaperManagerServer\\photo") 
        dir_list = [os.path.join(path, x) for x in os.listdir(path)]
        im = Image.open(dir_list[0])

        time_now = datetime.datetime.now()
        month_now = (time_now.strftime("%B"))
        calendar_image = Image.open('C:\\WallpaperManager\\WallpaperManagerServer\\calendar\\'+month_now+'.jpg')

        new_im = Image.new('RGB', (1920,1080))
        new_im.paste(im, (0,0))
        new_im.paste(calendar_image, (calendar_x, calendar_y))
        new_im.save('C:\\WallpaperManager\\WallpaperManagerServer\\s_photo\\send.jpg')

        img = Image.open('C:\\WallpaperManager\\WallpaperManagerServer\\s_photo\\send.jpg') #добавление текста
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("16658.otf", 52)
        int_month = int(time_now.strftime("%m"))
        draw.text((text_x, text_y), celebration[int_month], (255,0,255),font=font)
        img.save('C:\\WallpaperManager\\WallpaperManagerServer\\s_photo\\send.jpg')

        time.sleep(1)
        os.remove("C:\\WallpaperManager\\WallpaperManagerServer\\photo\\" + lis[0])       

def copy_image(): # Копирование файлов из пользовательской папки в системную
    while True:
        exec(open("C:\\WallpaperManager\\WallpaperManagerServer\\wallpapermanagerconfig.conf").read())
        newpath = path_photo_user 
        if not os.path.exists(newpath): #создаем каталог, если его нет
            os.makedirs(newpath)
        src_files = os.listdir(path_photo_user) # Копируем файлы из пользовательского каталога
        for file_name in src_files:
            full_file_name = os.path.join(path_photo_user, file_name)
            if (os.path.isfile(full_file_name)):
                shutil.copy(full_file_name, 'C:\\WallpaperManager\\WallpaperManagerServer\\photo\\')
                os.remove(full_file_name)
        time.sleep(4)


exec(open("C:\\WallpaperManager\\WallpaperManagerServer\\wallpapermanagerconfig.conf").read())

threading.Thread(target=send_wallpaper).start()
threading.Thread(target=copy_image).start()
