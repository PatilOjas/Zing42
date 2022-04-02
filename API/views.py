from django.contrib.messages.constants import INFO
from django.http import response, JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.serializers import Serializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import UserSerializer, AdminSerializer, CompanySerializer, EquitySerializer, BhavSerializer
from .models import API_User, BhavCopy, Company, EquitySec

import pandas as pd
from datetime import datetime

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
	queryset = API_User.objects.all()
	serializer_class = UserSerializer
	authentication_classes = [JWTAuthentication]
	permission_classes = [IsAuthenticated]

@api_view(['GET'])
def apiOverview(request):
	api_urls = {
		'Register': '/create/',
		'List': '/list/',
	}

	return Response(api_urls)

@api_view(['GET'])
def ShowAll(request):
	users = API_User.objects.all()
	serializer = UserSerializer(users, many=True)
	
	return Response(serializer.data)

@api_view(['POST'])
def createUser(request):
	serializer = UserSerializer(data=request.data)
	print(request.data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data)
	
	elif request.data['mobile'][0] != '+' or len(request.data['mobile']) != 13 or not request.data['mobile'][1:].isdecimal():
		return Response({"message": "Make sure you are entering mobile number with country code without any spaces e.g. +919876543210"})
	
	else:
		return Response({"message": "You are already a registered user."})

@api_view(['GET'])
def updateDB(request):
	bhavURL = "https://archives.nseindia.com/content/historical/EQUITIES/2022/APR/cm01APR2022bhav.csv.zip"
	EquiSecURL = "https://archives.nseindia.com/emerge/corporates/content/SME_EQUITY_L.csv"

	dfEquiSec = pd.read_csv(EquiSecURL)
	for _, data in dfEquiSec.iterrows():
		symbol = data['SYMBOL']
		
		flag = Company.objects.filter(symbol=symbol)
		if not flag:
			companyInstance = Company(companyName=data['NAME_OF_COMPANY'], 
			symbol=data['SYMBOL'], 
			series=data['SERIES'], 
			isInNumber=data['ISIN_NUMBER'])
			companyInstance.save()
		else:
			flag = flag[0]
		flag = EquitySec.objects.filter(symbol=data['SYMBOL'])
		if not flag:
			date = datetime_object = datetime.strptime(data['DATE_OF_LISTING'], '%d-%b-%y')
			equityInstance = EquitySec(symbol=data['SYMBOL'], 
			listing_date=date.strftime("%Y-%m-%d"), 
			paidUpValue=data['PAID_UP_VALUE'], 
			faceValue=data['FACE_VALUE'])
			equityInstance.save()
			print("Equity Saved")
	
	dfBhav = pd.read_csv(bhavURL)
	for _, data in dfBhav.iterrows():
		symbol = data['SYMBOL']
		flag = Company.objects.filter(symbol=symbol)
		if not flag:
			companyInstance = Company(symbol=data['SYMBOL'], 
			companyName='NA', 
			series=data['SERIES'], 
			isInNumber=data['ISIN'])
			companyInstance.save()

		
		flag = BhavCopy.objects.filter(symbol=symbol)
		if not flag:
			BhavInstance = BhavCopy(symbol=data['SYMBOL'], 
			open=data['OPEN'], 
			high=data['HIGH'], 
			low=data['LOW'], 
			close=data['CLOSE'], 
			last=data['LAST'], 
			prevClose=data['PREVCLOSE'], 
			tottrdqty=data['TOTTRDQTY'], 
			tottrdval=data['TOTTRDVAL'], 
			timeStamp=data['TIMESTAMP'], 
			totalTrades=data['TOTALTRADES'])
			BhavInstance.save()
			print("Bhav Saved!")
	return JsonResponse({'Response': "Database Updated successfully!!"}) 


@api_view(['GET'])
def fetchFromDB(request):
	data = dict()
	symbol = request.data['symbol']
	print(symbol)
	company = Company.objects.filter(symbol=symbol)
	print(company)
	if company:
		company = company[0]
		data['SYMBOL'] = company.symbol
		data['COMPANY_NAME'] = company.companyName
		data['SERIES'] = company.series
		data['ISIN_NUMBER'] = company.isInNumber

		equitySec = EquitySec.objects.filter(symbol=company.symbol)
		if equitySec:
			equitySec = equitySec[0]
			data['DATE_OF_LISTING'] = equitySec.listing_date
			data['PAID_UP_VALUE'] = equitySec.paidUpValue
			data['FACE_VALUE'] = equitySec.faceValue	
		
		bhav = BhavCopy.objects.filter(symbol=company.symbol)
		if bhav:
			bhav = bhav[0]
			data['PREVCLOSE'] = bhav.prevClose 
			data['OPEN'] = bhav.open 
			data['CLOSE'] = bhav.close 
			data['LAST'] = bhav.last 
			data['HIGH'] = bhav.high 
			data['LOW'] = bhav.low 
			data['TOTTRDQTY'] = bhav.tottrdqty 
			data['TOTTRDVAL'] = bhav.tottrdval 
			data['TOTALTRADES'] = bhav.totalTrades  
			data['TIMESTAMP'] = bhav.timeStamp 
	else:
		data['RESPONSE'] = "No such symbol found"
	
	return JsonResponse(data)