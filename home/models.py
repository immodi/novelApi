from django.db import models 

class File(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.DateField(auto_now=True)
    mime_type = models.CharField(max_length=500)
    name = models.CharField(max_length=999)
    size = models.CharField(max_length=500)

    def __str__(self):
        return self.name
    

class Chunk(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=99999)
    file_id = models.CharField(max_length=99999)
    main_file = models.ForeignKey(File, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)