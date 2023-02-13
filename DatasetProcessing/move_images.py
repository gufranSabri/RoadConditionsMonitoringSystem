import random
import shutil
import glob

source_dir = "/media/gufran/GsHDD/Work/Projects/RoadCapture/Dataset/original"
dest_dir = "/media/gufran/GsHDD/Work/Projects/RoadCapture/Dataset/finalized_reduced"

classes = ["good", "medium", "bad", "unpaved"]

for c in classes:
    print(c)
    print(source_dir+ '/{c}/{c}*'.format(c=c))
    for i in random.sample(glob.glob(source_dir+ '/{c}/{c}*'.format(c=c)),100):
        shutil.copy(i, dest_dir+"/"+c)


# import shutil
# import os

# source_dir = "/media/gufran/GsHDD/Work/Projects/AI/PotholeSeverityClassification/Challenge Track 2_ Pothole severity classification via computer vision-20221006T083657Z-001/Challenge Track 2_ Pothole severity classification via computer vision/png"
# dest_dir = "/media/gufran/GsHDD/Work/Projects/AI/PotholeSeverityClassification/Challenge Track 2_ Pothole severity classification via computer vision-20221006T083657Z-001/Challenge Track 2_ Pothole severity classification via computer vision/png/SceneEx"

# classes = ["Scene G1", "Scene G2", "Scene G3", "Scene G4", "Scene G5"]

# cc = 0
# for c in classes:
#     curr = source_dir + "/" + c
#     images = os.listdir(curr)

#     print(c)
#     for i in images:
#         cc+=1
#         curri = curr + "/" + i

#         shutil.copy(curri, dest_dir+"/"+str(cc)+".png")