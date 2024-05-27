from celery import shared_task
from ScraperAPI.models import request_details, url_details
from .models import WebScrapermodel
import asyncio
from asgiref.sync import async_to_sync
from celery import Celery
import time

# async def task_work(request_id, batch, delay=1):
#     for url in batch:
#         WebScraper = WebScrapermodel(url)
#         resp = WebScraper.get_response()

#         print('response of WebScraper.get_response in views is: ', resp)
#         if resp is not None:
#             url_link = url
#             title_ = WebScraper.extract_title()
#             summary_ = WebScraper.summarization()
#             links_ = WebScraper.extract_link()

#             url_details.objects.create(request_ids=request_id, urls=url_link, title=title_, summary=summary_, links=links_, status="SUCCESS")

#         # Introduce a delay between processing each URL
#         await asyncio.sleep(delay)


@shared_task
def background_work(request_id_, urls):

    print('background work has started')    

    success_count = 0  
    failed_count = 0
    
    # updating request_id and status in url_details table              
    for url in urls: 

        time.sleep(10)           
                
        webScraper=WebScrapermodel(url)
        resp = webScraper.get_response()

        print('response of WebScraper.get_response in views is: ',resp)
        if resp != None:
            url_link=url
            title_= webScraper.extract_title()
            summary_ = webScraper.summarization()  
            links_ = webScraper.extract_link()

            # url_details.objects.create(request_ids=request_id_, urls=url_link, title=title_ , summary=summary_ , links=links_ , status="SUCCESS")

        if title_ and summary_ and links_:
            url_details.objects.create(request_ids=request_id_, urls=url_link, title=title_ , summary=summary_ , links=links_ , status="Success")
            success_count+=1

        else:
            url_details.objects.create(request_ids=request_id_, urls=url_link, title=title_ , summary=summary_ , links=links_ , status="Failed")
            failed_count+=1

    
    request_details_obj = request_details.objects.get(request_id = request_id_)

    print(success_count)
    print(failed_count)

    if failed_count>0 and success_count>0:
        request_details_obj.status= 'Partial Success' 

    elif failed_count>0:
        request_details_obj.status= 'Failed'
        
    else:
        request_details_obj.status= 'Success'

    request_details_obj.save()

    print('background work has ended')  