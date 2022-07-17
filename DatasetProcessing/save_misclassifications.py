from asyncore import write
import tensorflow 
from keras.applications.vgg16 import preprocess_input as vi
from keras.applications.mobilenet_v2 import preprocess_input as mi
import cv2
import os
import numpy as np

custom = tensorflow.keras.models.load_model('/media/gufran/GsHDD/Work/Projects/RoadCapture/Models/custom.h5')
vgg = tensorflow.keras.models.load_model('/media/gufran/GsHDD/Work/Projects/RoadCapture/Models/vgg.h5')
mnet = tensorflow.keras.models.load_model('/media/gufran/GsHDD/Work/Projects/RoadCapture/Models/mnet.h5')

test_dir = '/media/gufran/GsHDD/Work/Projects/RoadCapture/Dataset/workenv/augmented/test'
save_dir_c = '/media/gufran/GsHDD/Work/Projects/RoadCapture/Dataset/workenv/mis_classifications_c'
save_dir_v = '/media/gufran/GsHDD/Work/Projects/RoadCapture/Dataset/workenv/mis_classifications_v'
save_dir_m = '/media/gufran/GsHDD/Work/Projects/RoadCapture/Dataset/workenv/mis_classifications_m'
labels = ["good","medium","bad","unpaved"]

cm = 0
vm = 0
mm = 0

cm = 0
vm = 0
mm = 0

for i in range(len(labels)):
    c = labels[i]
    ci = labels.index(c)
    
    images =  os.listdir(test_dir+'/'+c)
    
    print(c)
    
    for im in images:
        path = test_dir+'/'+c+'/'+im

        img = cv2.imread(path)
        img2 = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)

        imgv = vi(img)
        imgm = mi(img2)

        img = np.expand_dims(img, axis=0)
        imgv = np.expand_dims(imgv, axis=0)
        imgm = np.expand_dims(imgm, axis=0)

        cres = list(custom.predict(img,verbose=0)[0])
        vres = list(vgg.predict(imgv,verbose=0)[0])
        mres = list(mnet.predict(imgm,verbose=0)[0])
        
        cri = cres.index(max(cres))
        vri = vres.index(max(vres))
        mri = mres.index(max(mres))
        
        if ci != cri:
            cm+=1
            
            write_path = save_dir_c + '/' + c + '/' + labels[cri] + '/' + str(cm) + '.jpg'
            cv2.imwrite(write_path, cv2.imread(path))
            print(path)
            print(write_path)
        
        if ci != vri:
            vm+=1
            
            write_path = save_dir_v + '/' + c + '/' + labels[vri] + '/' + str(vm) + '.jpg'
            cv2.imwrite(write_path, cv2.imread(path))
            print(path)
            print(write_path)
        
        if ci != mri:
            mm+=1
            
            write_path = save_dir_m + '/' + c + '/' + labels[mri] + '/' + str(mm) + '.jpg'
            cv2.imwrite(write_path, cv2.imread(path))
            print(path)
            print(write_path)
    print()

print()

print(cm,vm,mm)