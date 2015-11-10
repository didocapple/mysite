from django.db import models

# Create your models here.
class Author(models.Model):
    AuthorID = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=70)
    Age = models.IntegerField()
    Country = models.CharField(max_length=50)
    
class Book(models.Model):
    ISBN = models.CharField(max_length=100,primary_key=True)
    Title = models.CharField(max_length=100)
    AuthorID = models.ForeignKey(Author)
    Publisher = models.CharField(max_length=30)
    PublishDate = models.DateField()
    Price = models.FloatField()
