from django.db import models
import datetime

class Poll(models.Model):
	question = models.CharField(max_length=200)
	pub_date = models.DateTimeField('data published')
	def __unicode__(self):
		return self.question
	def was_published_today(self):
		return self.pub_date.date() == datetime.date.today()

class Choice(models.Model):
	poll = models.ForeignKey(Poll)
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)
	def __unicoide__(self):
		return self.Choice