import cv2
import os
import sys

vid_path = '/media/gufran/GsHDD/UNI/SeniorDesign/Videos'
fname = '/media/gufran/GsHDD/Work/Projects/RoadCapture/Dataset/self'
check = False

# def emptyFunction(a):
#     pass  # function called when trackbar value is changed

# cv2.namedWindow("Edge threshold changer")
# cv2.resizeWindow("Edge threshold changer", 300, 200)
# cv2.createTrackbar("lower", "Edge threshold changer", 0, 150, emptyFunction)
# cv2.createTrackbar("upper", "Edge threshold changer", 100, 255, emptyFunction)


def get_max(l,i_name):
    m = 0
    for i in l:
        # i = i.replace(i_name,"").replace(".jpg","")
        i = i[1:i.index(".")]
        m = max(m, int(i))
    print(m+1,end=' ')

    return m+1

#vid 2,3,4,5 done
cap = cv2.VideoCapture('/media/gufran/GsHDD/Work/Projects/RoadCapture/Videos/vid2.mp4')

a,b,c,d,e = 0,0,0,0,0
if check:
    l = os.listdir(fname+'/good')
    a = get_max(l,'good')

    l = os.listdir(fname+'/medium')
    b = get_max(l,'medium')

    l = os.listdir(fname+'/bad')
    c = get_max(l,'bad')

    l = os.listdir(fname+'/unpaved')
    d = get_max(l,'unpaved')

    print()

cc = 0
if len(sys.argv)>1: last_stopped = int(sys.argv[1])
else: last_stopped=500
offset=500

while True:
    _, img = cap.read()
    cc+=1

    cv2.imshow("mainImg", img)

    cv2.imshow("mainImg", cv2.resize(img, (len(img[1])//4,len(img[0])//4)))
    img = cv2.resize(img, (224,224))
    cropped_image = img[100:, :]
    cv2.imshow("img", cropped_image)

    if cc < last_stopped-offset: 
        if cc%10000==0: print(cc, end=' ')
        x = cv2.waitKey(1)
        continue
        
    else: x = cv2.waitKey(0)
    

    if x == ord('1'):
        cv2.imwrite(fname+'/testingCode/good/'+"g"+str(a) + ".jpg", cropped_image)
        a += 1
    if x == ord('2'):
        cv2.imwrite(fname+'/testingCode/medium/'+"m"+str(b) + ".jpg", cropped_image)
        b += 1
    if x == ord('3'):
        cv2.imwrite(fname+'/testingCode/bad/'+"b"+str(c) + ".jpg", cropped_image)
        c += 1
    if x == ord('4'):
        cv2.imwrite(fname+'/testingCode/unpaved/'+"u"+str(d) + ".jpg", cropped_image)
        d += 1
    if x == ord('0'):
        break

print(cc)
    
    
cap.release()
cv2.destroyAllWindows()