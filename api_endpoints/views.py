from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from api_endpoints.serializers import apiSerailizer
import requests
import extcolors
from PIL import Image
def find_avg_border(image_url):
    im = Image.open(requests.get(image_url, stream=True).raw)
    h,w=im.size
    pix = im.load()
    r_avg=int((pix[0,0][0]+pix[0,w-1][0]+pix[h-1,0][0]+pix[h-1,w-1][0])/4)
    g_avg=int((pix[0,0][1]+pix[0,w-1][1]+pix[h-1,0][1]+pix[h-1,w-1][1])/4)
    b_avg=int((pix[0,0][2]+pix[0,w-1][2]+pix[h-1,0][2]+pix[h-1,w-1][2])/4)
    return (r_avg,g_avg,b_avg)
def euclid_dist(rgb1,rgb2):
	sum=0
	for i in range(3):
		sum=sum+pow(rgb1[i]-rgb2[i],2)
	return pow(sum,0.5)
def rgbToHex(rgb):
	return '#%02x%02x%02x' % (rgb)
@api_view(['GET', ])
def apiView(request):
    image_url=request.GET['src']
    colors, pixel_count = extcolors.extract_from_path(requests.get(image_url, stream=True).raw)
    border_avg=find_avg_border(image_url)
    border_color=(0,0,0)
    dominant_color=(0,0,0)
    for color in colors:
        if euclid_dist(border_avg,color[0])<20:
            border_color=(color[0])
            break
    for color in colors:
        if color[0]!=border_color:
            dominant_color=(color[0])
            break

    data={"logo_border":rgbToHex(border_color),"dominant_color":rgbToHex(dominant_color)}
    result=apiSerailizer(data).data
    return Response(result)
