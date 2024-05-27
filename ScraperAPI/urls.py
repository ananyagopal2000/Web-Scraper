from django.urls import path,include
from .views import ResultAPIViews
from .views import BulkCrawlAPIView
from .views import ReportAPIViews
from .views import SummarizeAPIView


urlpatterns = [
    path('crawling/', BulkCrawlAPIView.as_view(), name='crawl_api'),
    path('summarize/', SummarizeAPIView.as_view(), name='crawl-result_api'),
    path('result/', ResultAPIViews.as_view(), name='crawl-result'),
    path('report/', ReportAPIViews.as_view(), name='pagination-result'),
]