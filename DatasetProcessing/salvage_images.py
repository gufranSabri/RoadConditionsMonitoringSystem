import cv2
import os

from cv2 import moveWindow

fname = '/media/gufran/GsHDD/UNI/SeniorDesign/Dataset/sih_road_dataset'

l = os.listdir(fname+'/very_poor')
max = len(l)

a = 578

for i in l:
    img = cv2.imread(fname+'/very_poor/'+i)

    im2 = cv2.resize(img, (224,124))
    img = cv2.resize(img, (224,224))
    cropped_image = img[100:, :]

    cv2.imshow("1", cropped_image)
    cv2.imshow("2", im2)

    moveWindow("2",0,300)

    x = cv2.waitKey(0)

    if x == ord('1'):
        cv2.imwrite(fname+'/salvaged/'+"bad"+str(a) + ".jpg", cropped_image)
        a+=1
    if x == ord('2'):
        cv2.imwrite(fname+'/salvaged/'+"bad"+str(a) + ".jpg", im2)
        a+=1
    if x == ord('3'):
        cv2.imwrite(fname+'/salvaged/'+"bad"+str(a) + ".jpg", cropped_image)
        a+=1
        cv2.imwrite(fname+'/salvaged/'+"bad"+str(a) + ".jpg", im2)
        a+=1
    if x == ord('0'):
        break
    
    cv2.destroyAllWindows()

