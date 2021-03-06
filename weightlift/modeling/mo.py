import cv2
import numpy as np
import pandas as pd
import os
import math
import IPython, PIL
from IPython.display import Image

# where the frames from video will be saved
dirname = "outputs/frames"
    
# my notebook starts here
cap= cv2.VideoCapture(destination)
i = 0
while (cap.isOpened()) :
    ret, frame = cap.read()
    if ret == False :
        break
    path = os.path.join(dirname, '1tvimg'+str(i)+'.jpg')
    cv2.imwrite(path, frame)
    i = i + 1

cap.release()
cv2.destroyAllWindows()

#where the images with skeleton will be saved
processed = "outputs/frames+skel"
import cv2
import time
import numpy as np
import matplotlib.pyplot as plt

MODE = "MPI"

if MODE is "MPI" :
    protoFile = "outputs/models/pose/mpi/pose_deploy_linevec_faster_4_stages.prototxt"
    weightsFile = "outputs/models/pose_iter_160000.caffemodel"
    nPoints = 20
    POSE_PAIRS = [ [13, 3], [12, 3],] # for hands
    # POSE_PAIRS = [ [12, 5], [4, 5], ] # not good for top most point
net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)

def draw_skeleton_on_image(_frame) :

    frame = _frame
    frameCopy = np.copy(frame)
    frameWidth = frame.shape[1]
    frameHeight = frame.shape[0]
    threshold = 0.1

    inWidth = 368
    inHeight = 368

    inpBlob = cv2.dnn.blobFromImage(frame, 1.0 / 255, (inWidth, inHeight),
                            (0, 0, 0), swapRB=False, crop=False)

    net.setInput(inpBlob)

    output = net.forward()
    H = output.shape[2]
    W = output.shape[3]

    # Empty list to store the detected keypoints
    points = []

    temp = 0

    for i in range(nPoints):
        # confidence map of corresponding body's part.
        probMap = output[0, i, :, :]

        # Find global maxima of the probMap.
        minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)
        
        # Scale the point to fit on the original image
        x = (frameWidth * point[0]) / W
        y = (frameHeight * point[1]) / H
        
        if prob > threshold and (i==3 or i==12 or i==13): 
            cv2.circle(frameCopy, (int(x), int(y)), 8, (0, 255, 255), thickness=-1, lineType=cv2.FILLED)
            cv2.putText(frameCopy, "{}".format(i), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, lineType=cv2.LINE_AA)
            cv2.circle(frame, (int(x), int(y)), 8, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)

            # Add the point to the list if the probability is greater than the threshold
            points.append((int(x), int(y)))
        else :
            points.append(None)

    # Draw Skeleton
    for pair in POSE_PAIRS:
        partA = pair[0]
        partB = pair[1]

        if points[partA] and points[partB]:
            cv2.line(frame, points[partA], points[partB], (0, 255, 255), 3)

    plt.figure(figsize=[10,10])
    #plt.imshow(cv2.cvtColor(frameCopy, cv2.COLOR_BGR2RGB))
    plt.figure(figsize=[10,10])
    #   return frame
    #plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    dirr = os.path.join(processed, "1skeleton{}.jpg".format(kount))
    cv2.imwrite(dirr, frame)

import glob
# take all the frames
images = glob.glob("outputs/frames" + '/*.jpg')
images.sort()

kount = 88  # I took images from 88th frame
for img in images[88:199]:
    image_name = "1tvimg{}.jpg".format(kount)
    image_path = os.path.join("outputs/frames", image_name)
    frame = cv2.imread(image_path)
    draw_skeleton_on_image(frame)
    kount = kount + 1
    #print(image_name)
    if kount%50==0:
        print("upto",image_path,"images done")
p = len(os.listdir(processed))
img_array = []
kount = p-5
kk = 93 # i will start taking frames from 93
for cnt in range(kount) :
    image_name = "1skeleton{}.jpg".format(kk)
    filename = os.path.join(processed, image_name)
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img) 
    # print(image_name)
    #print(filename)
    kk = kk + 1

out = cv2.VideoWriter('1weightlift_skel2.avi',cv2.VideoWriter_fourcc(*'DIVX'), 15, size)

for i in range(len(img_array)) :
    out.write(img_array[i])
out.release()

    # return (JsonResponse('1weightlift_skel2.avi', safe=False))