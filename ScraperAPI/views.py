from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Q
import requests
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from WebScraper.models import WebScrapermodel
from .serializer import PageInfoSerializer
import uuid
import json
from .models import request_details, url_details
import asyncio
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.pagination import PageNumberPagination
from django.core.serializers import serialize
from .serializer import  UrlDataSerializer
from WebScraper.tasks import background_work
import time


class SummarizeAPIView(APIView):
    def generate_unique_id(self):
        return uuid.uuid4()
    
    def get(self,requests):
        
        response_res=[]
        url = requests.GET.get('url')        
        request_id_=self.generate_unique_id()        

        request_details(request_id=request_id_, no_urls_requested=1, no_urls_suubmitted=1, status='In progress')

        WebScraper=WebScrapermodel(url)
        resp = WebScraper.get_response()

        if resp != None:
            url_link=url
            title_= WebScraper.extract_title()
            summary_ = WebScraper.summarization()  
            links_ = WebScraper.extract_link()

            url_details.objects.create(request_ids = request_id_, urls = url_link, title = title_ ,summary = summary_ ,links = links_ ,status = "SUCCESS")
        
        
        request_details.objects.update(status="Success")        
        
        url_data = url_details.objects.filter(request_ids=request_id_).values('request_ids','title','summary','links').first()

        return JsonResponse(url_data, safe=False) 


class BulkCrawlAPIView(APIView):
    def generate_unique_id(self):
        return uuid.uuid4()      
    
    def post(self, requests):

        print('recieved request. foreground work started')

        response={}
        status_='In progress'

        mydata = json.loads(requests.body)
        print(mydata)
        urls  = mydata.get('urls')  

        request_id_=self.generate_unique_id()
        response = ({'message': 'Success. Crawling initiated successfully',
                    'request_id':request_id_,
                    'status':status_})   
             
        # updating  request_id and status in REQUEST_details table
        request_det_obj = request_details(request_id=request_id_, no_urls_requested=len(urls), no_urls_suubmitted=len(urls), status=status_)
        request_det_obj.save()

        # request_details.objects.update(status="In progress")
        batches=[]
        no_batches=10
        batch_size = len(urls)//no_batches
        no_extra_urls=len(urls) % no_batches
        extra=urls[(len(urls) - no_extra_urls):]     

        if len(urls)<=10:
            background_work.delay(request_id_,urls) 

        else:
            for i in range(0, len(urls), batch_size):
                batches.append(urls[i:i + batch_size]) 
            
            for batch in batches:
                print(request_id_)
                background_work.delay(request_id_,batch)
        
        # time.sleep(30)
        # request_details.objects.update(status="Success") 

        print('after filling fields')

        return JsonResponse(response) 
    
    
class ResultAPIViews(APIView):
    
    def get(self,requests): 

        response_res=[]
        req_id = requests.GET.get('request_id')
        print(req_id)
        
        request_details_data = request_details.objects.get(request_id=req_id)
        print(request_details_data.request_id)     

        # if request_details_data.status=='In progress':
        #     return Response({'status':'In progress'})  
                
        if request_details_data.status=='Success':
            url_data = url_details.objects.filter(request_ids=req_id) 
                                   
            for url in url_data:
                response_res.append(
                    {
                    'url':url.urls,
                    'title':url.title,
                    'summary':url.summary,
                    'links':url.links
                }
                )
            
            return JsonResponse(response_res,safe=False) 
        else:
            return Response({'status':'In progress'})

        
        

#PageNumberPagination() provides a way to paginate querysets, meaning it can split a large set of results into manageable pages
#paginate_queryset method processes the queryset according to the pagination settings and the current request. It splits the queryset into pages and returns only the items for the current page, based on the page parameter in the request UR
class ReportAPIViews(APIView):
     
     def get(self,requests):
        
        page_num = requests.GET.get('page')
      
        unique_urls = url_details.objects.values('urls').distinct()

        paginator = PageNumberPagination()
        paginator.page_size = 10
        result = paginator.paginate_queryset(unique_urls, requests)

        serializer = UrlDataSerializer(result,many=True)   
       
        return paginator.get_paginated_response(serializer.data)
       