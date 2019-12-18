


import os.path
import numpy as np
from cv2 import cv2
import json
from flask import Flask,request,Response
import uuid
import tkinter as Tk
from PIL import Image
from PIL import ImageTk


def trait_img(img_bw):


		def rgb_to_hex(rgb):
			return '#%02x%02x%02x' % rgb

		def hex_to_rgb(value):
			value = value.lstrip('#')
			lv = len(value)
			return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

		global hsv
		global couleur
		couleur= "#3f685c"

		def traitement_image(img_bw) :
			global Photo_traitee

			global canvas_photoTraitee
			global hsv
			couleur = "#3F875C"


			hsv = [75, 130, 90]
			H = hsv[0]
			S = hsv[1]
			V = hsv[2]

			HMin = H - 15
			HMax = H + 15
			SMin = S - 70
			SMax = S + 70
			VMin = V - 90
			VMax = V + 90
			minHSV = np.array([HMin, SMin, VMin])
			maxHSV = np.array([HMax, SMax, VMax])
			#img = cv2.imread(img_bw)
			imageHSV = cv2.cvtColor(img_bw, cv2.COLOR_BGR2HSV)
			maskHSV = cv2.inRange(imageHSV, minHSV, maxHSV)
			resultHSV = cv2.bitwise_and(img_bw, img_bw, mask=maskHSV)
			img_gray = cv2.cvtColor(resultHSV, cv2.COLOR_RGB2GRAY)
			(thresh, img_bw) = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
			#path_file=('static/%s.jpg' %uuid.uuid4().hex),
			cv2.imwrite('static/photo.jpg', img_bw)
			return json.dumps('static/photo.jpg')

		traitement_image(img_bw)
		
        

app = Flask(__name__)

#route htt^^post to this method

@app.route('/api/upload', methods=['POST'])
def upload():
	img_bw = cv2.imdecode(np.fromstring(request.files['image'].read(),np.uint8),cv2.IMREAD_UNCHANGED)
	img_processed = trait_img(img_bw)
	return Response(response=img_processed, status=200, mimetype="application/json")

app.run(host="0.0.0.0", port=5000)
