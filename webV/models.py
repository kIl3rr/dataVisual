from django.db import models

# Create your models here.
class totalthreeyears(models.Model):
    region = models.CharField(max_length=50)
    graduatesman = models.CharField(max_length=50)
    graduatesfemale = models.CharField(max_length=50)
    entrantsman = models.CharField(max_length=50)
    entrantsfemale = models.CharField(max_length=50)
    graduates = models.CharField(max_length=50)
    entrants = models.CharField(max_length=50)
    graduatesdoctor = models.CharField(max_length=50)
    graduatesmaster = models.CharField(max_length=50)
    degree = models.CharField(max_length=50)
    entrantsdoctor = models.CharField(max_length=50)
    entrantsmaster = models.CharField(max_length=50)
    year = models.CharField(max_length=50)

class classthreeyears(models.Model):
    subject = models.CharField(max_length=50)
    graduates = models.CharField(max_length=50)
    graduatesdoctor	= models.CharField(max_length=50)
    graduatesmaster	= models.CharField(max_length=50)
    entrants = models.CharField(max_length=50)
    entrantsdoctor = models.CharField(max_length=50)
    entrantsmaster = models.CharField(max_length=50)
    rate = models.CharField(max_length=50)
    year = models.CharField(max_length=50)
    
class topprovincerate(models.Model):
    year= models.CharField(max_length=50)
    province= models.CharField(max_length=50)	
    applicants= models.CharField(max_length=50)	
    enrollment= models.CharField(max_length=50)
    rate= models.CharField(max_length=50)


class kyweibo(models.Model):
    content	= models.TextField(max_length=16383)
    topic = models.TextField(max_length=16383)				

class itkyweibo(models.Model):
    content	= models.TextField(max_length=16383)
    topic = models.TextField(max_length=16383)					

class kyzhihu(models.Model):
    content	= models.TextField(max_length=16383)
    title = models.TextField(max_length=16383)

class itkyzhihu(models.Model):
    content	= models.TextField(max_length=16383)
    title = models.TextField(max_length=16383)

class zb(models.Model):
    year = models.CharField(max_length=50)
    applicants = models.CharField(max_length=50)
    enrollment = models.CharField(max_length=50)
    tm = models.CharField(max_length=50)

class jn(models.Model):
    year = models.CharField(max_length=50)
    applicants = models.CharField(max_length=50)
    enrollment = models.CharField(max_length=50)
    tm = models.CharField(max_length=50)    