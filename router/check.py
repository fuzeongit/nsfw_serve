import json

from django.shortcuts import HttpResponse
from unit.nsfw import main
from unit.nsfw import path_split
import requests


def index(request):
    paths_2d = path_split(request.GET.get("path"), 20)
    for i, image_paths in enumerate(paths_2d):
        requests.post('http://localhost:6001/picture/save/', json={'list': main(image_paths)})
    return HttpResponse("ok", content_type="application/json")
