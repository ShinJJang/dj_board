# -*- coding: utf-8 -*-
from django import forms

class UploadFileForm(forms.Form):
	file = forms.FileField(
		label = 'Select a file',
		help_text = 'max. 42 megabytes'
	)