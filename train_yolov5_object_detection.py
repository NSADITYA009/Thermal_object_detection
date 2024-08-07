# -*- coding: utf-8 -*-
"""Copy of train-yolov5-object-detection-on-custom-data.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1O4b6ypJXicWpbejQLtMrJ8NbRO__mxna
"""

# Commented out IPython magic to ensure Python compatibility.
# clone YOLOv5 repository
!git clone https://github.com/ultralytics/yolov5  # clone repo
# %cd yolov5
!git reset --hard 064365d8683fd002e9ad789c1e91fa3d021b44f0

# install dependencies as necessary
!pip install -qr requirements.txt  # install dependencies (ignore errors)
import torch

from IPython.display import Image, clear_output  # to display images

# clear_output()
print('Setup complete. Using torch %s %s' % (torch.__version__, torch.cuda.get_device_properties(0) if torch.cuda.is_available() else 'CPU'))

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/yolov5
!pip install roboflow

from roboflow import Roboflow
rf = Roboflow(api_key="61eU9pEpBsXJkfwnPZsz")
project = rf.workspace("joseph-nelson").project("thermal-dogs-and-people")
dataset = project.version(6).download("yolov5")

# Commented out IPython magic to ensure Python compatibility.
# this is the YAML file Roboflow wrote for us that we're loading into this notebook with our data
# %cat {dataset.location}/data.yaml

# define number of classes based on YAML
import yaml
with open(dataset.location + "/data.yaml", 'r') as stream:
    num_classes = str(yaml.safe_load(stream)['nc'])

# Commented out IPython magic to ensure Python compatibility.
#this is the model configuration we will use for our tutorial 
# %cat /content/yolov5/models/yolov5s.yaml

#customize iPython writefile so we can write variables
from IPython.core.magic import register_line_cell_magic

@register_line_cell_magic
def writetemplate(line, cell):
    with open(line, 'w') as f:
        f.write(cell.format(**globals()))

# Commented out IPython magic to ensure Python compatibility.
# %%writetemplate /content/yolov5/models/custom_yolov5s.yaml
# 
# # parameters
# nc: {num_classes}  # number of classes
# depth_multiple: 0.33  # model depth multiple
# width_multiple: 0.50  # layer channel multiple
# 
# # anchors
# anchors:
#   - [10,13, 16,30, 33,23]  # P3/8
#   - [30,61, 62,45, 59,119]  # P4/16
#   - [116,90, 156,198, 373,326]  # P5/32
# 
# # YOLOv5 backbone
# backbone:
#   # [from, number, module, args]
#   [[-1, 1, Focus, [64, 3]],  # 0-P1/2
#    [-1, 1, Conv, [128, 3, 2]],  # 1-P2/4
#    [-1, 3, BottleneckCSP, [128]],
#    [-1, 1, Conv, [256, 3, 2]],  # 3-P3/8
#    [-1, 9, BottleneckCSP, [256]],
#    [-1, 1, Conv, [512, 3, 2]],  # 5-P4/16
#    [-1, 9, BottleneckCSP, [512]],
#    [-1, 1, Conv, [1024, 3, 2]],  # 7-P5/32
#    [-1, 1, SPP, [1024, [5, 9, 13]]],
#    [-1, 3, BottleneckCSP, [1024, False]],  # 9
#   ]
# 
# # YOLOv5 head
# head:
#   [[-1, 1, Conv, [512, 1, 1]],
#    [-1, 1, nn.Upsample, [None, 2, 'nearest']],
#    [[-1, 6], 1, Concat, [1]],  # cat backbone P4
#    [-1, 3, BottleneckCSP, [512, False]],  # 13
# 
#    [-1, 1, Conv, [256, 1, 1]],
#    [-1, 1, nn.Upsample, [None, 2, 'nearest']],
#    [[-1, 4], 1, Concat, [1]],  # cat backbone P3
#    [-1, 3, BottleneckCSP, [256, False]],  # 17 (P3/8-small)
# 
#    [-1, 1, Conv, [256, 3, 2]],
#    [[-1, 14], 1, Concat, [1]],  # cat head P4
#    [-1, 3, BottleneckCSP, [512, False]],  # 20 (P4/16-medium)
# 
#    [-1, 1, Conv, [512, 3, 2]],
#    [[-1, 10], 1, Concat, [1]],  # cat head P5
#    [-1, 3, BottleneckCSP, [1024, False]],  # 23 (P5/32-large)
# 
#    [[17, 20, 23], 1, Detect, [nc, anchors]],  # Detect(P3, P4, P5)
#   ]

# Commented out IPython magic to ensure Python compatibility.
# # train yolov5s on custom data for 100 epochs
# # time its performance
# %%time
# %cd /content/yolov5/
# !python train.py --img 416 --batch 16 --epochs 200 --data {dataset.location}/data.yaml --cfg ./models/custom_yolov5s.yaml --weights '' --name yolov5s_results  --cache

# Commented out IPython magic to ensure Python compatibility.
# Start tensorboard
# Launch after you have started training
# logs save in the folder "runs"
# %load_ext tensorboard
# %tensorboard --logdir runs

from utils.plots import plot_results  # plot results.txt as results.png
Image(filename='/content/yolov5/runs/train/yolov5s_results2/results.png', width=1000)  # view results.png

# Commented out IPython magic to ensure Python compatibility.
# trained weights are saved by default in our weights folder
# %ls runs/

# Commented out IPython magic to ensure Python compatibility.

# %ls runs/train/yolov5s_results/weights

# Commented out IPython magic to ensure Python compatibility.

# use the best weights!
# %cd /content/yolov5/
!python detect.py --weights runs/train/yolov5s_results2/weights/best.pt --img 416 --conf 0.4 --source /content/yolov5/Thermal-Dogs-and-People-6/test/images

#display inference on ALL test images
#this looks much better with longer training above

import glob
from IPython.display import Image, display

for imageName in glob.glob('/content/yolov5/runs/detect/exp/*.jpg'): #assuming JPG
    display(Image(filename=imageName))
    print("\n")

from google.colab import drive
drive.mount('/content/gdrive')

# Commented out IPython magic to ensure Python compatibility.
# %cp /content/yolov5/runs/train/yolov5s_results2/weights/best.pt /content/gdrive/MyDrive



