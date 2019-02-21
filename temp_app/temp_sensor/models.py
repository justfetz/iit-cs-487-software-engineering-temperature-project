from django.db import models
#from django.db import models
from django.utils import timezone
from django.urls import reverse
# Create your models here.
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class tempSensor(models.Model):
	lowerBound = models.IntegerField()
	upperBound = models.IntegerField()
	currentTemp = models.IntegerField()
	timeChanged = models.DateTimeField(default=timezone.now)

	def validateBounds(value):
		if value < self.currentTemp:
			raise ValidationError(_('%(value)s is out of bounds'),
				params={'value':value},
				)
	

	def publishTime(self):
		self.timeChanged = timezone.now()
		self.save()

	def clean(self):
		if (self.currentTemp > self.upperBound) or (self.currentTemp < self.lowerBound):
			#self.add_error('Error in Bounds')
			raise ValidationError('You need to update your bounds to perform this operation.')
	
	def __str__(self):
		return "{}, {}, {}".format(str(self.currentTemp), str(self.lowerBound), str(self.upperBound))
	
class Users(models.Model):
	first_name = models.TextField(max_length=256)
	last_name = models.TextField(max_length=256)
	email = models. EmailField()
	password = models.CharField(max_length=10)