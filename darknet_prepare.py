import sys
import os
import numpy
import glob
import random
import shutil
import ntpath

result_folder = "Results"
images_folder = "Images"
labels_folder = "Labels"
test_file = "test.txt"
train_file = "train.txt"
obj_data_file = "obj.data"
obj_names_file = "obj.names"

#def move_obj_files_to_darknet_directory():
#    cfg_folder = os.path.join(sys.argv[4], "cfg")
#    shutil.copyfile(obj_data_file, cfg_folder + "/" + obj_data_file)
#    shutil.copyfile(obj_names_file, cfg_folder + "/" + obj_names_file)

def generate_darknet_config_file():
   with open(os.path.join(result_folder, obj_data_file), "w") as obj_file:
       obj_file.write("classes = 1\n\
train = " + toAbsoluteResultPath(train_file) + "\n\
valid = " + toAbsoluteResultPath(test_file) + "\n\
names = " + toAbsoluteResultPath(obj_names_file) + "\n\
backup = backup")

def generate_darknet_name_file():
    with open(os.path.join(result_folder, obj_names_file), "w") as obj_file:
        obj_file.write(sys.argv[3])

def toAbsoluteResultPath(file_name):
    return os.path.abspath(os.path.join(result_folder, ntpath.basename(file_name)))

def saveList(file_name, list):
    with open(os.path.join(result_folder, file_name), "w") as txt_file:
        for element in list:
            txt_file.write(element + "\n")

def save(image_list, labels_list, folder_name):
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    for image in image_list:
        image_name = ntpath.basename(image)
        shutil.copyfile(image, folder_name + "/" + image_name)
    for label in labels_list:
        label_name = ntpath.basename(label)
        shutil.copyfile(label, folder_name + "/" + label_name)

if len(sys.argv) < 4:
    print("Usage: darknet_prepare.py folder_number test_set_size label_name darknet_directory")
    sys.exit()

folder_number = int(sys.argv[1])
test_set_size = float(sys.argv[2])

imageDir = os.path.join(r'./' + images_folder, '%03d' %(folder_number))
labelsDir = os.path.join(r'./' + labels_folder, '%03d' %(folder_number))

jpg_files = ('*.jpg', '*.jpeg')
imageList = []
for jpg_file in jpg_files:
    imageList.extend(glob.glob(imageDir + '/' + jpg_file))

labelsList = glob.glob(labelsDir + '/' + '*.txt')

if not os.path.exists(result_folder):
    os.mkdir(result_folder)

results_dir = os.path.join(r'./' + result_folder)
save(imageList, labelsList, result_folder)

imageList = []
for jpg_file in jpg_files:
    imageList.extend(glob.glob(result_folder + '/' + jpg_file))

random.shuffle(imageList)
training_size = int(len(imageList) * (1.0-test_set_size))
test_size = len(imageList) - training_size

training_list = imageList[:training_size]
test_list = imageList[-test_size:]

training_absolute_list = list(map(toAbsoluteResultPath, training_list))
test_absolute_list = list(map(toAbsoluteResultPath, test_list))

saveList(train_file, training_absolute_list)
saveList(test_file, test_absolute_list)

# generate darknet config file:
generate_darknet_config_file()
generate_darknet_name_file()

# move files to darknet cfg directory:
#if len(sys.argv) == 5:
#    move_obj_files_to_darknet_directory()

print("darknet.exe detector train " + toAbsoluteResultPath(obj_data_file) + " YOUR_LAYERS YOUR_WEIGHTS")
