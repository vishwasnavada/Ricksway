# -*- coding: utf-8 -*-

import six.moves.urllib as urllib
import os

try:
    import urllib.request
except ImportError:
    raise ImportError('You should use Python 3.x')

if not os.path.exists('./RoadDamageDataset.tar.gz'):
    url_base = 'https://s3-ap-northeast-1.amazonaws.com/mycityreport/RoadDamageDataset.tar.gz'
    urllib.request.urlretrieve(url_base, './RoadDamageDataset.tar.gz')

    print("Download RoadDamageDataset.tar.gz Done")

else:
    print("You have RoadDamageDataset.tar.gz")


if not os.path.exists('./trainedModels.tar.gz'):
    url_base = 'https://s3-ap-northeast-1.amazonaws.com/mycityreport/trainedModels.tar.gz'
    urllib.request.urlretrieve(url_base, './trainedModels.tar.gz')

    print("Download trainedModels.tar.gz Done")

else:
    print("You have trainedModels.tar.gz")

from xml.etree import ElementTree
from xml.dom import minidom
import collections

import os

import matplotlib.pyplot as plt
import matplotlib as matplot
import seaborn as sns

base_path = os.getcwd() + '/RoadDamageDataset/'

damageTypes = ["D00", "D01", "D10", "D11", "D20", "D40", "D43", "D44"]

# govs corresponds to municipality name.
govs = ["Adachi", "Chiba", "Ichihara",
        "Muroran", "Nagakute", "Numazu", "Sumida"]

# the number of total images and total labels.
cls_names = []
total_images = 0
for gov in govs:

    file_list = os.listdir(base_path + gov + '/Annotations/')

    for file in file_list:

        total_images = total_images + 1
        if file == '.DS_Store':
            pass
        else:
            try:
                infile_xml = open(base_path + gov + '/Annotations/' + file)
                tree = ElementTree.parse(infile_xml)
                root = tree.getroot()
                for obj in root.iter('object'):
                    cls_name = obj.find('name').text
                    cls_names.append(cls_name)
            except:
                pass

print("total")
print('# of images: ' + str(total_images))
print("# of labels：" + str(len(cls_names)))

# the number of each class labels.
import collections
count_dict = collections.Counter(cls_names)
cls_count = []
for damageType in damageTypes:
    print(str(damageType) + ' : ' + str(count_dict[damageType]))
    cls_count.append(count_dict[damageType])

sns.set_palette("winter", 8)
sns.barplot(damageTypes, cls_count)

# the number of each class labels for each municipality
for gov in govs:
    cls_names = []
    total_images = 0
    file_list = os.listdir(base_path + gov + '/Annotations/')

    for file in file_list:

        total_images = total_images + 1
        if file == '.DS_Store':
            pass
        else:
            try:
                infile_xml = open(base_path + gov + '/Annotations/' + file)
                tree = ElementTree.parse(infile_xml)
                root = tree.getroot()
                for obj in root.iter('object'):
                    cls_name = obj.find('name').text
                    cls_names.append(cls_name)
            except:
                pass
    print(gov)
    print("# of images：" + str(total_images))
    print("# of labels：" + str(len(cls_names)))

    count_dict = collections.Counter(cls_names)
    cls_count = []
    for damageType in damageTypes:
        print(str(damageType) + ' : ' + str(count_dict[damageType]))
        cls_count.append(count_dict[damageType])

    print('**************************************************')

import cv2
import random


def draw_images(image_file):
    gov = image_file.split('_')[0]
    img = cv2.imread(base_path + gov + '/JPEGImages/' +
                     image_file.split('.')[0] + '.jpg')

    infile_xml = open(base_path + gov + '/Annotations/' + image_file)
    tree = ElementTree.parse(infile_xml)
    root = tree.getroot()

    for obj in root.iter('object'):
        cls_name = obj.find('name').text
        xmlbox = obj.find('bndbox')
        xmin = int(xmlbox.find('xmin').text)
        xmax = int(xmlbox.find('xmax').text)
        ymin = int(xmlbox.find('ymin').text)
        ymax = int(xmlbox.find('ymax').text)

        font = cv2.FONT_HERSHEY_SIMPLEX

        # put text
        cv2.putText(img, cls_name, (xmin, ymin - 10),
                    font, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # draw bounding box
        cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 255, 0), 3)
    return img

for damageType in damageTypes:
    tmp = []
    for gov in govs:
        file = open(base_path + gov +
                    '/ImageSets/Main/%s_trainval.txt' % damageType, 'r')

        for line in file:
            line = line.rstrip('\n').split('/')[-1]

            if line.split(' ')[2] == '1':
                tmp.append(line.split(' ')[0] + '.xml')

    random.shuffle(tmp)
    fig = plt.figure(figsize=(6, 6))
    # for number, image in enumerate(tmp[0:1]):
    #     img = draw_images(image)
    #     plt.subplot(1, 1, number)
    #     plt.axis('off')
    #     plt.title('The image including ' + damageType)
    #     plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
