
import numpy as np
import sys
import tarfile
import tensorflow as tf
import zipfile
import cv2
import urllib
import subprocess

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image

#if tf.__version__ != '1.4.1':
 #   raise ImportError('Please upgrade your tensorflow installation to v1.4.1!')

def url_to_image(url):
	# download the image, convert it to a NumPy array, and then read
	# it into OpenCV format
	resp = urllib.urlopen(url)
	image = np.asarray(bytearray(resp.read()), dtype="uint8")
	image = cv2.imdecode(image, cv2.IMREAD_COLOR)
 
	# return the image
	return image

from utils import label_map_util

from utils import visualization_utils as vis_util

# Path to frozen detection graph. This is the actual model that is used
# for the object detection.
PATH_TO_CKPT = 'trainedModels/ssd_mobilenet_RoadDamageDetector.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = 'trainedModels/crack_label_map.pbtxt'

NUM_CLASSES = 8

detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')


label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(
    label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)


def load_image_into_numpy_array(image):
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape(
        (im_height, im_width, 3)).astype(np.uint8)


# get images from val.txt
PATH_TO_TEST_IMAGES_DIR = '/home/ubuntu/DATASET/CrackDataset-TF/CrackDataset/'
D_TYPE = ['D00', 'D01', 'D10', 'D11', 'D20', 'D40', 'D43']
govs = ['Adachi', 'Ichihara', 'Muroran',
        'Chiba', 'Sumida', 'Nagakute', 'Numazu']

# val_list = []
# for gov in govs:
#     file = open(PATH_TO_TEST_IMAGES_DIR + gov + '/ImageSets/Main/val.txt', 'r')
#     for line in file:
#         line = line.rstrip('\n').split('/')[-1]
#         val_list.append(line)
#     file.close()

# print("# of validation images：" + str(len(val_list)))


ramp_frames = 30
cam = cv2.VideoCapture(1)

def get_image():
 retval, im = cam.read()
 return im

for i in range(ramp_frames):
 temp = get_image()

camera_capture = get_image()
file1 = "test.jpg"
cv2.imwrite(file1, camera_capture)


TEST_IMAGE_PATHS = ['test.jpg']
# random.shuffle(val_list)

# for val_image in val_list[0:5]:
#     TEST_IMAGE_PATHS.append(PATH_TO_TEST_IMAGES_DIR +
#                             val_image.split('_')[0] + '/JPEGImages/%s.jpg' % val_image)
# Size, in inches, of the output images.
IMAGE_SIZE = (12, 8)

with detection_graph.as_default():
    with tf.Session(graph=detection_graph) as sess:
        # Definite input and output Tensors for detection_graph
        image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
        # Each box represents a part of the image where a particular object was
        # detected.
        detection_boxes = detection_graph.get_tensor_by_name(
            'detection_boxes:0')
        # Each score represent how level of confidence for each of the objects.
        # Score is shown on the result image, together with the class label.
        detection_scores = detection_graph.get_tensor_by_name(
            'detection_scores:0')
        detection_classes = detection_graph.get_tensor_by_name(
            'detection_classes:0')
        num_detections = detection_graph.get_tensor_by_name('num_detections:0')
        for image_path in TEST_IMAGE_PATHS:
            image = Image.open(image_path)
            # the array based representation of the image will be used later in order to prepare the
            # result image with boxes and labels on it.
            image_np = load_image_into_numpy_array(image)
            # Expand dimensions since the model expects images to have shape:
            # [1, None, None, 3]
            image_np_expanded = np.expand_dims(image_np, axis=0)
            # Actual detection.
            (boxes, scores, classes, num) = sess.run(
                [detection_boxes, detection_scores,
                    detection_classes, num_detections],
                feed_dict={image_tensor: image_np_expanded})
            print(boxes, scores, classes, num)
            # Visualization of the results of a detection.
            vis_util.visualize_boxes_and_labels_on_image_array(
                image_np,
                np.squeeze(boxes),
                np.squeeze(classes).astype(np.int32),
                np.squeeze(scores),
                category_index,
                min_score_thresh=0.3,
                use_normalized_coordinates=True,
                line_thickness=8)
            Image.fromarray(image_np).save('/opt/lampp/htdocs/result.jpg')
            plt.figure(figsize=IMAGE_SIZE)
            plt.imshow(image_np)
            


