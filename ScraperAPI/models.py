from django.db import models
# each model is represented by a class that subclasses django.db.models.Model. Each model has a number of class variables, each of which represents a database field in the model.
# Create your models here.

class request_details(models.Model):

    request_id = models.CharField(max_length=300,unique=True)
    no_urls_requested = models.IntegerField(null=True,blank=True)
    no_urls_suubmitted = models.IntegerField(null=True,blank=True)
    status = models.TextField()

    def __str__(self):
        return self.request_id,self.status
    
    
class url_details(models.Model):

    request_ids = models.CharField(max_length=300)
    # request_id = models.ForeignKey(request_details, on_delete=models.CASCADE,to_field='request_id')  #When a record with a ForeignKey relationship is deleted, this option ensures that all related records are also deleted, creating a cascading effect throughout the database
    urls = models.URLField()
    title = models.CharField(max_length=300)
    summary = models.TextField()
    links= models.TextField()
    status = models.TextField()

#     def __str__(self):
#         return self.request_ids,self.status
