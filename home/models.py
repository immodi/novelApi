from django.db import models 

class Directory(models.Model):
    id = models.BigAutoField(primary_key=True)
    path = models.CharField(max_length=9999)
    parent_dir = models.ForeignKey("home.Directory", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.path)

class File(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.DateField(auto_now=True)
    mime_type = models.CharField(max_length=500)
    name = models.CharField(max_length=999)
    size = models.CharField(max_length=500)
    parent_dir = models.ForeignKey(Directory, on_delete=models.CASCADE, null=False, blank=False)
    
    def __str__(self):
        return self.name
    

class Chunk(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=99999)
    file_id = models.CharField(max_length=99999)
    main_file = models.ForeignKey(File, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
