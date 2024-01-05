"""
# local
zip -q mturk.zip -r requirements.txt solver.py model.keras model_labels.dat

# ubuntu
sudo apt-get update -qq
sudo apt-get install -qq python3-pip curl unzip libgl1-mesa-glx
pip3 install -r requirements.txt --no-cache-dir

# CloudShell (Amazon Linux 2023)
# `pip install` to /home directory is failed because it is limited to 1 GB.
# It's successful to install to /usr/local/lib{64} by becoming root user.
sudo su -
cd /tmp
yum install libglvnd-glx -y
pip3 install -r requirements.txt --no-cache-dir
"""

import os

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")

import cv2
import pickle
import os
import numpy as np

from keras.models import load_model

import requests

MODEL_FILENAME = "model.keras"
MODEL_LABELS_FILENAME = "model_labels.dat"
TRAIN_DATASET_DIR = "datasets/train"
TEST_DATASET_DIR = "datasets/test"
BASE_URL = "https://ac185e5fdb155d78.247ctf.com"


with open(MODEL_LABELS_FILENAME, "rb") as f:
    lb = pickle.load(f)

model = load_model(MODEL_FILENAME)

requests.packages.urllib3.disable_warnings()
s = requests.Session()
s.verify = False

import time
import re


def predict(org_image, bounding_boxes):
    predictions = []
    for bounding_box in bounding_boxes:
        x, y, w, h = bounding_box

        # Extract the letter from the original image with a 2-pixel margin around the edge
        image = org_image[y : y + h, x : x + w]

        image = cv2.resize(image, (20, 20))

        image = np.expand_dims(image, axis=2)
        image = np.expand_dims(image, axis=0)

        prediction = model.predict_on_batch(image)

        letter = lb.inverse_transform(prediction)[0]
        predictions.append(letter)

    return predictions


def process_image(raw_image):
    image = np.frombuffer(raw_image, np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    # erase background points and lines
    image[np.all(image == (140, 140, 140), axis=-1)] = (255, 255, 255)

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, image = cv2.threshold(image, 140, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    _, thresh = cv2.threshold(image, 140, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # sort
    bounding_boxes = [cv2.boundingRect(c) for c in contours]
    (contours, bounding_boxes) = zip(
        *sorted(zip(contours, bounding_boxes), key=lambda b: b[1][0])
    )

    return image, bounding_boxes


for _ in range(9999):
    t1 = time.time()

    res = s.get(f"{BASE_URL}/mturk.php")
    print(f"[+] download time: {time.time()-t1}")

    image, bounding_boxes = process_image(res.content)

    # predict
    t2 = time.time()
    predictions = predict(image, bounding_boxes)
    captcha_text = "".join(predictions)
    print(f"[+] predict time: {time.time()-t2}")

    try:
        result = eval(captcha_text)
    except:
        print(f"error occures, captcha text result: {captcha_text}")
        continue

    res = s.post(f"{BASE_URL}/", data={"captcha": result})

    m = re.findall(r"text-center'>(.*?)</div>", res.text)
    if not m:
        print("not matched")
        continue

    msg = m[0]
    print(msg)

    if "247CTF" in msg:
        break

    print(f"[+] All processing time: {time.time() - t1}\n")
