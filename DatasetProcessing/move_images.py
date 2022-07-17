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
