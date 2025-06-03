from rest_framework.serializers  import ModelSerializer
from .models import Documents

class DocumentSerializer(ModelSerializer):
    class Meta:
        model = Documents
        fields = ['docid', 'patentNumber', 'uploadTime', 'documentPath']
        read_only_fields = ['docid', 'uploadTime']
        
        
    def create(self, validated_data):
        """  Create a new Document instance with the provided validated data.
        """
        return Documents.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """
        Update an existing Document instance with the provided validated data.
        """
        instance.patentNumber = validated_data.get('patentNumber', instance.patentNumber)
        instance.documentPath = validated_data.get('documentPath', instance.documentPath)
        instance.save()
        return instance
    
    def delete(self, instance):
        """
        Delete the specified Document instance.
        """
        instance.delete()
        return instance