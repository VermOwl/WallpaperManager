import socket   
import os
import datetime
import time
import threading
import ctypes
 
def file_manager():
    while True:
                        
        while True:
            sock = socket.socket()      
            port = 9090              
            sock.bind(('', port))        
            file = open('C:\\WallpaperManager\\WallpaperManagerClient\\image\\add.jpg','wb')
            sock.listen(1)
            connect, addr = sock.accept()     
            print ('Got connection from', addr)
            print ("Start Receiving...")
            load = connect.recv(1024)
            while (load):
        
                file.write(load)
                load = connect.recv(1024)
            
            print ("Done Sending")
            file.close()
            sock.close()
            break
        time_now = datetime.datetime.now()                        #Даем название файлу                          
        random_number = (time_now.strftime("%y%m%d%H%M%S"))
        file_rename = ('C:\\WallpaperManager\\WallpaperManagerClient\\image\\' + str(random_number) + '.jpg')
        os.rename('C:\\WallpaperManager\\WallpaperManagerClient\\image\\add.jpg', file_rename)
        print ("File rename")
        #os.remove('C:\\WallpaperManager\\WallpaperManagerClient\\image\\add.jpg')
        
        path = 'C:\\WallpaperManager\\WallpaperManagerClient\\image'   
        dir_list = [os.path.join(path, x) for x in os.listdir(path)] #выгружаем все файлы из папки
        if dir_list:                                                 #сортируем и удаляем если кол-во файлов больше 10
            date_list = [[x, os.path.getctime(x)] for x in dir_list] 
            sort_date_list = sorted(date_list, key=lambda x: x[1])
            print (sort_date_list[0][0]) 
            print (len(date_list))
            if len(date_list) > 10:
                print ("Кол-во файлов превышено. Был удален файл " + str(sort_date_list[0][0]))
                os.remove(sort_date_list[0][0])
                

def wallpaper_install():
    path = 'C:\\WallpaperManager\\WallpaperManagerClient\\image' 
    image_set = ['wer']
    image_set.clear()
    i = 0

    while True:
        dir_list = [os.path.join(path, x) for x in os.listdir(path)]
        if i > len(dir_list) - 1:
            i = 0
            image_set.clear()
        imagePath = dir_list[i]

        for item in image_set:
            if dir_list[i] == item:
                print ("Я нашел элемент, выхожу")
                break
        else:
            ctypes.windll.user32.SystemParametersInfoW(20, 0, imagePath, 3)
            print ("Установил обои")
            image_set.append(imagePath)
        i = i + 1
        time.sleep(10) # Задержка выставления изображения на рабочий стол

threading.Thread(target=file_manager).start()
threading.Thread(target=wallpaper_install).start()