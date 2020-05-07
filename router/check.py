from django.shortcuts import HttpResponse
from unit.nsfw import main


def index(request):
    return HttpResponse(main(request.GET.get("path")), content_type="application/json")
