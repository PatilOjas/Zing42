from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class API_User(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50, null=False, blank=False)
	mobile = PhoneNumberField(unique=True, null=False, blank=False)
	timestamp = models.DateTimeField(auto_now=True)


	def __str__(self) -> str:
		return self.name


class Company(models.Model):
	symbol = models.CharField(max_length=50, null=False, blank=False, primary_key=True)
	companyName = models.CharField(max_length=50, null=False, blank=False)
	series = models.CharField(max_length=2, null=False, blank=False)
	isInNumber = models.CharField(max_length=12, null=False, blank=False)
	
	def __str__(self) -> str:
		return self.symbol


class EquitySec(models.Model):
	# id = models.AutoField(primary_key=True)
	# symbol = models.CharField(max_length=50, null=False, blank=False)
	symbol = models.ForeignKey(Company, on_delete=models.CASCADE)
	listing_date = models.DateField()
	paidUpValue = models.IntegerField()
	faceValue = models.IntegerField()

	def __str__(self) -> str:
		return self.symbol.symbol

class BhavCopy(models.Model):
	# id = models.AutoField(primary_key=True)
	# symbol = models.CharField(max_length=50, null=False, blank=False)
	symbol = models.ForeignKey(Company, on_delete=models.CASCADE)
	open = models.FloatField()
	high = models.FloatField()
	low = models.FloatField()
	close = models.FloatField()
	last = models.FloatField()
	prevClose = models.FloatField()
	tottrdqty = models.IntegerField()
	tottrdval = models.FloatField()
	timeStamp = models.DateField()
	totalTrades = models.IntegerField()

	def __str__(self) -> str:
		return self.symbol.symbol