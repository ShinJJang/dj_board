# -*- coding: utf-8 -*-
from django import forms

class UploadFileForm(forms.Form):
	file_1 = forms.FileField(
		label = 'Select a file',
		help_text = 'max. 42 megabytes'
	)
	file_2 = forms.FileField(
		label = 'Select a file',
		help_text = 'max. 42 megabytes'
	)