import shutil
import os

fname = '/media/gufran/GsHDD/UNI/SeniorDesign/Dataset/self'
save_path = fname+'/actual'

g,m,b,u = 0,0,0,0

vids = ['vid1','vid2','vid3','vid4','vid5']
for v in vids:
    classes= os.listdir(fname+'/'+v)
    print(v)
    for c in classes:
        images= os.listdir(fname+'/'+v+'/'+c)
        print(c, len(images))
        # for i in images:
        #     curr=0
        #     if c == 'good':
        #         g+=1
        #         curr=g
        #     if c == 'medium':
        #         m+=1
        #         curr=m
        #     if c == 'bad':
        #         b+=1
        #         curr=b
        #     if c == 'unpaved':
        #         u+=1
        #         curr=u

            # shutil.copy(fname+'/'+v+'/'+c+'/'+i,save_path+'/'+c+'/'+c+str(curr)+'.jpg')
    print()

    



