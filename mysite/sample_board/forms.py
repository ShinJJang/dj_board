# -*- coding: utf-8 -*-
from django import forms

class UploadFileForm(forms.Form):
	subject = forms.CharField(label='제목', max_length=50)
	name = forms.CharField(label='이름', max_length=50)
	mail = forms.CharField(label='이메일', max_length=50)
	memo = forms.CharField(label='내용', max_length=200)
	#file_1 = forms.FileField(
	#	label = 'Select a file',
	#	help_text = 'max. 42 megabytes'
	#)
	#file_2 = forms.FileField(
	#	label = 'Select a file',
	#	help_text = 'max. 42 megabytes'
	#)