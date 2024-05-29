from celery import shared_task
from ScraperAPI.models import request_details, url_details
from .models import WebScrapermodel
import asyncio
from asgiref.sync import async_to_sync
from celery import Celery
import time
from urllib.parse import quote

@shared_task
def background_work(request_id_, urls, is_last_batch):

    print('background work has started')       
            
    for url in urls: 

        time.sleep(2) 
        
        url_det_obj = url_details(request_ids=request_id_, urls=url,status='In Progress')
        url_det_obj.save()

    for url in urls:
        webScraper=WebScrapermodel(url)
        resp = webScraper.get_response()

        if resp != None:
            url_link=url
            title_= webScraper.extract_title()
            summary_ = webScraper.summarization()  
            links_ = webScraper.extract_link()

            url_details.objects.filter(request_ids = request_id_, urls = url_link).update(title=title_, summary=summary_ , links=links_ , status="Success")      
        else:
            url_details.objects.filter(request_ids = request_id_, urls = url_link).update(status = "Failed")

    if is_last_batch:

        url_details_status = url_details.objects.filter(request_ids = request_id_).values_list('status', flat = True)

        if all(status == 'Success' for status in url_details_status):
            request_details_status = 'Success'

        elif any(status == 'Failed' for status in url_details_status):
            request_details_status = 'Partial Success'

        else:
            request_details_status='In Prog'

        request_details.objects.filter(request_id = request_id_).update(status = request_details_status)

    print('background work has ended')
  
