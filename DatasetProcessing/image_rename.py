import cv2
import os
import sys

def rename(path, name, start_index):
    l = os.listdir(path)

    for i in l:
        img = cv2.imread(path+"/"+i)
        os.remove(path+"/"+i)
        b = cv2.imwrite(path+"/"+name+str(start_index)+".jpg", img)
        if b:print(start_index, end=' ')
        start_index += 1

    print(start_index)
    print()

fname = '/media/gufran/GsHDD/Work/Projects/RoadCapture/Dataset/augmented' #change
classes = ['good','medium','bad','unpaved']
# classes = ['bad','unpaved']

# single_letter_file_name = True if sys.argv[1] == '1' else False
# file_start_num1 = int(sys.argv[2])
# file_start_num2 = int(sys.argv[3])

for i in classes:
    rename(fname+"/"+i, i, 1)
    # if single_letter_file_name:rename(fname+'/'+i, i[0], file_start_num1 if i == 'bad' else file_start_num2)
    # else : rename(fname+'/'+i, i, file_start_num1 if i == 'bad' else file_start_num2)
