# serializers.py
from rest_framework import serializers
from .models import url_details

class PageInfoSerializer(serializers.Serializer):
    url = serializers.URLField()
    summary = serializers.CharField()
    title = serializers.CharField()
    links = serializers.ListField(child=serializers.URLField())

# UrlDataSerializer:Converts url_details model instances to a JSON-compatible format that can be easily rendered into JSON responses in your API views.
# The Meta inner class is used to provide metadata to the UrlDataSerializer
# model = url_details: tells the serializer to use the url_details model to determine which fields to include in the serialization and deserialization process.

class UrlDataSerializer(serializers.ModelSerializer):    
    class Meta:
        model = url_details
        fields = ['urls']