# -*- coding: utf-8 -*-
from django.db import models

class DjangoBoard(models.Model):
	subject = models.CharField(max_length=50, blank=True)
	name = models.CharField(max_length=50, blank=True)
	created_date = models.DateField(null=True, blank=True)
	mail = models.CharField(max_length=50, blank=True)
	memo = models.CharField(max_length=200, blank=True)
	hits = models.IntegerField(null=True, blank=True)
	likes = models.IntegerField(null=True, blank=True)
	file_1 = models.FileField(null=True, upload_to = 'upload/%y/%m/%d')
	file_2 = models.FileField(null=True, upload_to = 'upload/%y/%m/%d')

class Settings(models.Model):
	rowsPerPage = models.IntegerField(null=True, blank=True)