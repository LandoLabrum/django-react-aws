import json
from datetime import datetime
import time
from django.shortcuts import render, redirect

from django.http import JsonResponse
from .serializers import F101Serializer, LeadSerializer
from .models import F101
from lead.models import Lead
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def F101View(request):
    context = {}
    if request.method == 'POST':
        d = json.loads(request.body)['body']
        time_str=datetime.strptime(d['appointment']['time'], "%H:%M").strftime("%I:%M %p")
        date_str = f"{d['appointment']['date']} at {time_str}"
        d['teachable'] = int(d['teachable'])
        d['appointment']['src'] = 'F101'
        lSerializer = LeadSerializer(data=d['appointment'])
        if lSerializer.is_valid():
            lSerializer.save()
            context={
                "status":"success",
                'appointment': date_str
                }
            format = "%Y-%m-%d at %H:%M"
            d['meeting'] = int(time.mktime(datetime.strptime(date_str, format).timetuple()))
            d['lead'] = d['appointment']['email']
            d.pop('appointment')
            fSerializer = F101Serializer(data=d) 
            if fSerializer.is_valid():
                fSerializer.save()
                context={
                    "status":"success",
                    'appointment': date_str
                    }
            else:
                context={
                    "status":"error",
                    'appointment': date_str,
                    'errors': fSerializer.errors
                }
        else:
            context={
                "status":"error",
                'appointment': date_str,
                'errors': lSerializer.errors
            }
    return JsonResponse(context)

