from django.shortcuts import render

# Create your views here.
# import the necessary packages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import numpy as np
import urllib
from django.conf import settings
import json
import cv2
import os


from omr_api import image_reg, template



def _grab_image(path=None, stream=None, url=None):
    # if the path is not None, then load the image from disk
    if path is not None:
        image = cv2.imread(path)


    # otherwise, the image does not reside on disk
    else:
        # if the URL is not None, then download the image
        if url is not None:
            resp = urllib.urlopen(url)
            data = resp.read()

        # if the stream is not None, then the image has been uploaded
        elif stream is not None:
            data = stream.read()

        # convert the image to a NumPy array and then read it into
        # OpenCV format
        image = np.asarray(bytearray(data), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)


    # return the image

    return image


alpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
		 'W', 'X', 'Y', 'Z']







def name_(orginal):


	h, w = orginal.shape
	crop = orginal[155:h - 20, 28:w - 30]
	th, im_th = cv2.threshold(crop, 127, 255, 0)
	im_th = ~im_th
	kernel = np.ones((5, 5), np.uint8)
	binary = cv2.erode(im_th, kernel, iterations=2)

	h1, w1 = crop.shape
	name = []

	# cv2.imshow("Foreground", crop )
	#    cv2.waitKey(0)

	for y in range(0, w1, np.uint(np.floor(w1 / 29))):

		if (y + int(w1 / 29) > w1):
			break
		column = binary[10:h1, y: y + int(w1 / 29)]
		visc = crop[10:h1, y: y + int(w1 / 29)]
		countn = 0

		for x in range(0, h1, np.uint(np.floor(h1 / 26))):

			if (x + int(h1 / 26) > h1):
				break
			row = column[x:x + int(h1 / 26), :]
			visr = visc[x:x + int(h1 / 26), :]
			countn += 1
			#        cv2.imshow("Foreground", visr )
			#        cv2.waitKey(1)

			cnts, hierarchy = cv2.findContours(row, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
			if len(cnts) == 1:
				name.append(alpha[countn - 1])

	name = ''.join(name)
	return name


def answer(x):
	if 0 < x < 90:
		ans = "a"
	if 90 < x < 180:
		ans = "b"
	if 180 < x < 270:
		ans = "c"
	if 270 < x < 360:
		ans = "d"

	return ans


def questions(orginal):


	th, im_th = cv2.threshold(orginal, 127, 255, 0)

	im_th = ~im_th
	kernel = np.ones((4, 4), np.uint8)
	binary = cv2.erode(im_th, kernel, iterations=2)

	h, w = binary.shape

	question = 0
	question_array = [""] * 201
	for y in range(0, w, np.uint(np.floor(w / 5))):

		if (y + int(w / 5 - 15) > w):
			break

		if y == 0:
			column = binary[14:h - 6, y + 75: y + int(w / 5 - 15)]
			visc = orginal[14:h - 6, y: y + int(w / 5 - 15)]

		else:
			column = binary[14:h - 6, y + 90: y + int(w / 5 - 15)]
		#            visc= orginal[14:h-6, y+14: y +int(w/5-15)]

		#    cv2.imshow("Foreground", visc)
		#    cv2.waitKey(0)
		##column = orginal[15:1696, 0:420]

		for x in range(0, column.shape[0], np.uint(np.floor(h / 40))):

			if (x + 40 > h):
				break

			question += 1
			row = column[x:x + 40, :]
			#            visr=visc[x:x+40,:]
			#        cv2.imshow("Foreground", visr)
			#        cv2.waitKey(0)

			cnts, hierarchy = cv2.findContours(row, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

			if len(cnts) <= 0:

				question_array[question] = ""

			# if cv2.contourArea(cnts[0])>950 or cv2.contourArea(cnts[0]) <600:
			#
			elif len(cnts) == 1:

				M = cv2.moments(row)
				cX = int(M["m10"] / M["m00"])
				cY = int(M["m01"] / M["m00"])

				question_array[question] = answer(cX)

			elif len(cnts) == 2:

				M1 = cv2.moments(cnts[1])
				cX1 = int(M1["m10"] / M1["m00"])
				cY1 = int(M1["m01"] / M1["m00"])

				M2 = cv2.moments(cnts[0])
				cX2 = int(M2["m10"] / M2["m00"])
				cY2 = int(M2["m01"] / M2["m00"])

				question_array[question] = answer(cX1) + answer(cX2)

			elif len(cnts) == 3:

				M1 = cv2.moments(cnts[2])
				cX1 = int(M1["m10"] / M1["m00"])
				cY1 = int(M1["m01"] / M1["m00"])

				M2 = cv2.moments(cnts[1])
				cX2 = int(M2["m10"] / M2["m00"])
				cY2 = int(M2["m01"] / M2["m00"])

				M3 = cv2.moments(cnts[0])
				cX3 = int(M3["m10"] / M3["m00"])
				cY3 = int(M3["m01"] / M3["m00"])

				question_array[question] = answer(cX1) + answer(cX2) + answer(cX3)
			else:
				question_array[question] = "a,b,c,d"
	#            print(question,question_array[question])

	return question_array


def mobile(orginal):


	h, w = orginal.shape
	crop = orginal[200:h - 9, 15:w - 15]
	th, im_th = cv2.threshold(crop, 127, 255, 0)
	im_th = ~im_th
	kernel = np.ones((5, 5), np.uint8)
	binary = cv2.erode(im_th, kernel, iterations=2)
	h1, w1 = crop.shape

	number = []

	for y in range(0, w1, np.uint(np.floor(w1 / 10))):

		if (y + int(w1 / 10) > w1):
			break
		column = binary[0:h1, y: y + int(w1 / 10)]
		visc = crop[0:h1, y: y + int(w1 / 10)]
		countn = 0
		for x in range(0, h1, np.uint(np.floor(h1 / 10))):

			if (x + int(h1 / 10) > h1):
				break
			row = column[x:x + int(h1 / 10), :]
			visr = visc[x:x + int(h1 / 10), :]
			countn += 1
			cnts, hierarchy = cv2.findContours(row, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
			if len(cnts) == 1:
				number.append(str(countn))

	number = [0 if x == 10 else x for x in number]
	number = ''.join(number)
	number = int(number)

	return number


def roll_no(orginal):

	h, w = orginal.shape
	crop = orginal[165:h - 15, 25:w - 25]

	th, im_th = cv2.threshold(crop, 127, 255, 0)
	im_th = ~im_th
	kernel = np.ones((5, 5), np.uint8)
	binary = cv2.erode(im_th, kernel, iterations=2)

	h1, w1 = crop.shape

	roll_no = []
	for y in range(0, w1, np.uint(np.floor(w1 / 7))):
		if (y + int(w1 / 7) > w1):
			break
		column = binary[0:h1, y: y + int(w1 / 7)]
		visc = crop[0:h1, y: y + int(w1 / 7)]

		count = 0
		for x in range(0, h1, np.uint(np.floor(h1 / 10))):

			if (x + int(h1 / 10) > h1):
				break
			row = column[x:x + int(h1 / 10), :]
			visr = visc[x:x + int(h1 / 10), :]
			count += 1
			cnts, hierarchy = cv2.findContours(row, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
			if len(cnts) == 1:
				roll_no.append(str(count))

	#        cv2.imshow("Foreground", visr )
	#        cv2.waitKey(0)
	roll_no = [0 if x == 10 else x for x in roll_no]
	roll_no = ''.join(roll_no)
	roll_no = int(roll_no)
	return roll_no


def ccode(orginal):

	h, w = orginal.shape
	crop = orginal[158:h - 5, 18:w - 18]
	th, im_th = cv2.threshold(crop, 127, 255, 0)
	im_th = ~im_th
	kernel = np.ones((5, 5), np.uint8)
	binary = cv2.erode(im_th, kernel, iterations=2)

	h1, w1 = crop.shape
	code = []
	for y in range(0, w1, np.uint(np.floor(w1 / 4))):
		if (y + int(w1 / 4) > w1):
			break
		column = binary[0:h1, y: y + int(w1 / 4)]
		visc = crop[0:h1, y: y + int(w1 / 4)]
		count = 0
		for x in range(0, h1, np.uint(np.floor(h1 / 10))):

			if (x + int(h1 / 10) > h1):
				break
			row = column[x:x + int(h1 / 10), :]
			visr = visc[x:x + int(h1 / 10), :]
			count += 1
			cnts, hierarchy = cv2.findContours(row, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
			if len(cnts) == 1:
				if count==10:
					count=0
				code.append(str(count))

	# code = [0 if x == 10 else x for x in code]
	code = ''.join(code)
	code = int(code)
	return code


def category(orginal):

	c = ["GEN", "OBC1", "OBC2", "SC", "ST", "PH"]

	h, w = orginal.shape
	crop = orginal[140:h - 5, 140:w - 5]
	h1, w1 = crop.shape

	th, im_th = cv2.threshold(crop, 127, 255, 0)
	im_th = ~im_th
	kernel = np.ones((5, 5), np.uint8)
	binary = cv2.erode(im_th, kernel, iterations=2)

	count = 0
	for x in range(0, h1, np.uint(np.floor(h1 / 6))):

		if (x + int(h1 / 6) > h1):
			break
		row = binary[x:x + int(h1 / 6), :]
		visr = crop[x:x + int(h1 / 6), :]
		count += 1
		cnts, hierarchy = cv2.findContours(row, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		if len(cnts) == 1:
			cat = c[count - 1]

	return cat


@csrf_exempt
def detect(request):
	# initialize the data dictionary to be returned by the request
	data = {"success": False}

	# check to see if this is a post request
	if request.method == "POST":
		# check to see if an image was uploaded
		if request.FILES.get("image", None) is not None:
			# grab the uploaded image
			image = _grab_image(stream=request.FILES["image"])

		# otherwise, assume that a URL was passed in
		else:
			# grab the URL from the request
			url = request.POST.get("url", None)

			# if the URL is None, then return an error
			if url is None:
				data["error"] = "No URL provided."
				return JsonResponse(data)

			# load the image and convert
			image = _grab_image(url=url)

		# convert the image to grayscale, load the face cascade detector,
		# and detect faces in the image
		# image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

		frame_image = cv2.imread(settings.FRAME_URL)
		category_image = cv2.imread(settings.CAT_URL)



		input_img = image_reg.alignImages(image, frame_image)
		detect = template.match(input_img, category_image)
		result = image_reg.alignImages(detect, category_image)
		result = cv2.resize(detect, (category_image.shape[1], category_image.shape[0]))




		result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

		# name = name_(image)
		# ques = questions(image)
		# mobi = mobile(image)
		# code = ccode(image)
		cate_ = category(result)
		# rollno = roll_no(image)




		# update the data dictionary with the faces detected
		data.update({"name":cate_, "success": True})

	# return a JSON response
	return JsonResponse(data)