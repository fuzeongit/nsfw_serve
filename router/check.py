import json

from django.db import IntegrityError
from django.shortcuts import HttpResponse

from model.nsfw_level import NsfwLevel
from unit.nsfw import main
from unit.nsfw import path_split
import requests


def index(request):
    paths_2d = path_split(request.GET.get("path"), 20)
    for i, image_paths in enumerate(paths_2d):
        for j, item in enumerate(main(image_paths)):
            nsfw_level = NsfwLevel()
            # # 给对象赋值
            nsfw_level.url = str(item['url']).split("\\")[-1]
            nsfw_level.drawings = item['probability']['drawings']
            nsfw_level.hentai = item['probability']['hentai']
            nsfw_level.neutral = item['probability']['neutral']
            nsfw_level.porn = item['probability']['porn']
            nsfw_level.sexy = item['probability']['sexy']
            nsfw_level.classify = __getClassify(item['probability'])
            # 插入数据
            try:
                nsfw_level.save()
            except IntegrityError:
                print(nsfw_level.url + "重复插入")
    return HttpResponse("ok", content_type="application/json")


def __getClassify(probability):
    level_list = [float(probability["drawings"]), float(probability["hentai"]), float(probability["neutral"]),
                  float(probability["porn"]), float(probability["sexy"])]
    max_level = max(level_list)
    classify = ""
    if float(probability["drawings"]) == max_level:
        classify = "drawings"
    if float(probability["hentai"]) == max_level:
        classify = "hentai"
    if float(probability["neutral"]) == max_level:
        classify = "neutral"
    if float(probability["porn"]) == max_level:
        classify = "porn"
    if float(probability["sexy"]) == max_level:
        classify = "sexy"
    return classify
