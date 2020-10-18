import base64
import random
import numpy as np
from io import BytesIO
from PIL import Image
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings


def get_web_data():
	model = settings.MODEL
	x, y = settings.MODEL_DATA
	index = random.randrange(x.shape[0])
	img, ori_label = x[index], y[index]
	image = Image.fromarray(img)
	data = BytesIO()
	image.save(data, 'png')
	data64 = base64.b64encode(data.getvalue())
	uri = u'data:img/jpeg;base64,'+ data64.decode('utf-8')
	img = img.reshape(1, 28, 28, 1)
	img = img.astype('float')
	img /= 255
	pred_label = np.argmax(model.predict(img), axis=-1)[0]
	return uri, ori_label, pred_label


# Create your views here.
def index(request):
	uri, ori_label, pred_label = get_web_data()

	times_count = int(request.COOKIES.get('times-count', '0'))
	pred_score = int(request.COOKIES.get('pred-score', '0'))
	
	if(pred_label == ori_label):
		pred_score += 1
	times_count += 1
	
	context = {
		'image_uri' : uri,
		'ori_label' : ori_label,
		'pred_label' : pred_label,
		'pred_score' : pred_score,
		'times_count' : times_count
	}
	
	response = render(request, 'app/index.html', context)
	
	response.set_cookie('times-count', times_count)
	response.set_cookie('pred-score', pred_score)

	return response