import nltk
import requests
import os
from django.db import models
from bs4 import BeautifulSoup
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
nltk.download('punkt')
nltk.download("stopwords")


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WebScraper.settings")

class WebScrapermodel(models.Model):

    def __init__(self,url):
        self.url=url        
        self.is_valid=False              #to check if the content is html or not


    def get_response(self):

        self.response=requests.get(self.url) 
        
        if self.response.status_code == 200:
            self.soup = BeautifulSoup(self.response.content, 'html.parser')
            if self.soup: self.is_valid = True
            if self.is_valid: return self.response
        
        return None


    def extract_title(self): 
        title = self.soup.title.string
        return title if title else None 
        

    def extract_link(self):
        
        links=[link.get('href') for link in self.soup.find_all('a') if link.get('href')]
        return ','.join(links)    
           

    # Generating the summary using sumy
    def summarization(self):

        text = self.soup.body.get_text(separator=' ', strip=True)

        if text!=None:
            
            tokenizer = Tokenizer("english")
            parser = PlaintextParser.from_string(text,tokenizer)
            summarizer = TextRankSummarizer()
            summarized_text = summarizer(parser.document, sentences_count=int(len(text)*0.3))

            return summarized_text
        
        else:

            return None
    
 
