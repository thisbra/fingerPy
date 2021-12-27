import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import time
from sigMain import sigMain
import sys


cap = cv.VideoCapture(sys.argv[1])

total_frames = cap.get(cv.CAP_PROP_FRAME_COUNT)
fps = cap.get(cv.CAP_PROP_FPS)
duration = total_frames / fps
ret = True

# normal_sum_values = []
hsv_v_values = []
frame_x = []
frame_c = 1

# PERFORMANCE MEASUREMENT
converting_time = 0
indexing_time = 0
summedian_time = 0

while ret:
    ret, frame = cap.read()
    
    if not ret:
        break

    frame_x.append(frame_c)
    frame_c += 1
    
    print(str(round(100*(frame_c/total_frames))) + " %")
    
    # GET HSV Value
    t = time.time()
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    converting_time += time.time() - t
    

    t = time.time()
    hsv_values = hsv[:,:,2]
    indexing_time += time.time() - t

    t = time.time()
    # print(hsv_values)
    mean_hsv_values = np.sum(np.sum(hsv_values, axis=0),axis=0)/hsv_values.size
    summedian_time += time.time() - t


    hsv_v_values.append(mean_hsv_values)
    
    

# print("frame: " + str(frame_x))
# print("NORMAL SUM VALUES: ")
# print(len(normal_sum_values))

print("HSV VALUES: ")
print(len(hsv_v_values))

sigMain(hsv_v_values, duration)

# DISPLAYING PERFORMNACE MEASUREMENT
print("Converting time: " + str(converting_time))
print("Indexing time: " + str(indexing_time))
print("Summedian time: " + str(summedian_time))


# plt.plot(frame_x, normal_sum_values, label="Normal Sum")
plt.plot(frame_x, hsv_v_values,color='lime', label="HSV Value")
plt.legend()
plt.grid()
plt.show()



