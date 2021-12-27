# FingerPy

FingerPy is a algorithm using python, scipy and fft to measure, analyse and monitor heart-beat using only a video of the user's finger on a mobile cellphone camera.


## Setup
On the repository directory:
```pip3 install -r requirements.txt```


## Usage
1. Record a video pressing your finger against the camera
2. Copy video to ```/samples```
3. ```python3 main.py samples/your_video.mp4|avi|MOV```


### Example
Video on ```/samples```

```python3 main.py samples/test_finger.avi```

![finger gif on camera](https://media0.giphy.com/media/gXzebxu2b6ZCgd8uUl/giphy.gif?cid=790b76114d6f1ae5ce4db8e03bf93cd99f7e25594edb00a7&rid=giphy.gif&ct=g)


###Result:
 (1) Number of Beats per minute  |  (2) [Heart-rate variability](https://en.wikipedia.org/wiki/Heart_rate_variability) in milliseconds  | (3) [Signal-to-noise ratio](https://en.wikipedia.org/wiki/Signal-to-noise_ratio) in decibels
![result](results.png)



