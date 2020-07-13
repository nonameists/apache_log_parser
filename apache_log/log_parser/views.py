from django.db.models import Sum, Count
from django.shortcuts import render

from .models import LogData


def index(request):
    most_common = LogData.objects.values("ip").annotate(count=Count('ip')).order_by("-count")[:10]
    unique_ip = LogData.objects.values('ip').distinct().count()
    methods = LogData.objects.values("http_method").annotate(count=Count('http_method')).order_by("-count")
    resopnse_size = LogData.objects.aggregate(Sum('response_size'))

    context = {
        'most_common_ip': most_common,
        'unique_ip': unique_ip,
        'methods' : methods,
        'response_size': resopnse_size
    }

    return render(request, 'index.html', context)
