from django.shortcuts import render, redirect
from django.http.response import HttpResponse, JsonResponse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from . import settings
from pathlib import Path

import mysql.connector
from mysql.connector import Error

import json
import os
import random

import sys
from subprocess import run,PIPE

import mimetypes
from django import forms

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.storage import default_storage
# Create your views here.

import psycopg2
import pandas as pd
import re
#import reverse_geocoder as rg

import urllib
from urllib import request
import requests
#from bs4 import BeautifulSoup
import time

import stripe

stripe.api_key='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'

def Homepage(request):
	items=[]
	price=[]
	item_path=[]
	dict={}
	
	try:
		connection = mysql.connector.connect(host='localhost',database='Jarvis',user='root',password='Suhu@2016')                                         
		if connection.is_connected():
			db_Info = connection.get_server_info()
			print("Connected to MySQL Server version ", db_Info)
			cursor = connection.cursor()
			cursor.execute("select database();")
			record = cursor.fetchone()
			fetch_query="select item_name,price,item_path from items;"
			print(fetch_query)
			cursor.execute(fetch_query)
			records = cursor.fetchall()
			print(records)
			for i in range(0,len(records)):
				dict['product_no_'+str(i+1)]=records[i][0]
				dict['price_'+str(i+1)]=records[i][1]
				dict['item_path_'+str(i+1)]=records[i][2]
				items.append(records[i][0])
				price.append(records[i][1])
				item_path.append(records[i][2])
			connection.commit()
	except Error as e:
		print("Error while connecting to MySQL", e)
	finally:
		if (connection.is_connected()):
			cursor.close()
			connection.close()
			print("MySQL connection is closed")
	
	count_imgs=len(items)
	item_paths=''
	for i in range(1,(len(dict)//3)+1):
		item_paths=item_paths+(dict['item_path_'+str(i)])+','
	
	item_paths=item_paths[:len(item_paths)-1]
	dict['item_paths']=item_paths
	#print(item_paths)
	#print(dict)
	#count_imgs=40
	if(count_imgs>1000):
		count_imgs=1000
	dict['total_no_products']=count_imgs
	return render(request,'HomePage.html',dict)

def Email_Cred(request):
	text=request.POST.get('email')
	To_ADDRESS=str(text)
	text1='gopisairam999@gmail.com'
	MY_ADDRESS=str(text1)
	dict={}
	dict['login_invalid']='Password sent to the given Email.'
	try:
		connection = mysql.connector.connect(host='localhost',database='Jarvis',user='root',password='Suhu@2016')                                         
		if connection.is_connected():
			db_Info = connection.get_server_info()
			print("Connected to MySQL Server version ", db_Info)
			cursor = connection.cursor()
			cursor.execute("select database();")
			record = cursor.fetchone()
			fetch_query="select username, password from user_login where email_id = '"+To_ADDRESS+"';"
			print(fetch_query)
			cursor.execute(fetch_query)
			records = cursor.fetchone()
			print(records)
	except Error as e:
		print("Error while connecting to MySQL", e)
	finally:
		if (connection.is_connected()):
			cursor.close()
			connection.close()
			print("MySQL connection is closed")
	username=records[0]
	password=records[1]
	PASSWORD="pqhylspdtjskergd"
	try:
		context=ssl.create_default_context()
		# set up the SMTP server
		s = smtplib.SMTP(host='smtp.gmail.com', port=587)
		s.ehlo()
		s.starttls(context=context)
		s.ehlo()
		s.login(MY_ADDRESS, PASSWORD)
		msg = MIMEMultipart()
		msg['From']=MY_ADDRESS
		msg['To']=To_ADDRESS
		print("To Address:",msg['To'])
		text="iClothing - Retreive Credentials - Includes password"
		msg['Subject']=str(text)
		print(msg['Subject'])
		complete_str='Hi '+str(username)+" ,\n\nYour Password is: "+str(password)
		msge=complete_str
		msge=msge+"\n\nThanks,\niClothing Team"
		message=str(msge)
		# add in the message body
		msg.attach(MIMEText(message, 'plain'))
		print('sending mail')        
		# send the message via the server set up earlier.
		s.send_message(msg)
		del msg

		# Terminate the SMTP session and close the connection
		s.quit()
		return render(request,'LoginPage.html',dict)
	except Error as e:
		print("Error while connecting to MySQL : ", e)
	return render(request,'Retrieve_credentials.html')

def login(request):
	return render(request,'LoginPage.html')

def abt_cmpy(request):
	return render(request,'abtpage.html')

def rld_hmpg(request):
	items=[]
	price=[]
	item_path=[]
	dict={}
	
	try:
		connection = mysql.connector.connect(host='localhost',database='Jarvis',user='root',password='Suhu@2016')                                         
		if connection.is_connected():
			db_Info = connection.get_server_info()
			print("Connected to MySQL Server version ", db_Info)
			cursor = connection.cursor()
			cursor.execute("select database();")
			record = cursor.fetchone()
			fetch_query="select item_name,price,item_path from items;"
			print(fetch_query)
			cursor.execute(fetch_query)
			records = cursor.fetchall()
			print(records)
			for i in range(0,len(records)):
				dict['product_no_'+str(i+1)]=records[i][0]
				dict['price_'+str(i+1)]=records[i][1]
				dict['item_path_'+str(i+1)]=records[i][2]
				items.append(records[i][0])
				price.append(records[i][1])
				item_path.append(records[i][2])
			connection.commit()
	except Error as e:
		print("Error while connecting to MySQL", e)
	finally:
		if (connection.is_connected()):
			cursor.close()
			connection.close()
			print("MySQL connection is closed")
	
	count_imgs=len(items)
	item_paths=''
	for i in range(1,(len(dict)//3)+1):
		item_paths=item_paths+(dict['item_path_'+str(i)])+','
	
	item_paths=item_paths[:len(item_paths)-1]
	dict['item_paths']=item_paths
	#print(item_paths)
	#print(dict)
	#count_imgs=40
	if(count_imgs>1000):
		count_imgs=1000
	dict['total_no_products']=count_imgs
	return render(request,'HomePage.html',dict)

def register(request):
	reg_usr= request.POST.get('reg_username')
	reg_email= request.POST.get('reg_email')
	reg_pass= request.POST.get('reg_password')
	reg_pass1= request.POST.get('reg_password1')
	reg_type= request.POST.get('UserAcct')
	if(reg_pass == reg_pass1):
		try:
			connection = mysql.connector.connect(host='localhost',database='Jarvis',user='root',password='Suhu@2016')                                         
			if connection.is_connected():
				db_Info = connection.get_server_info()
				print("Connected to MySQL Server version ", db_Info)
				cursor = connection.cursor()
				cursor.execute("select database();")
				record = cursor.fetchone()
				print(reg_usr+' '+reg_pass+' '+reg_email)
				if(reg_type=='User'):
					acct_status_Active='Active'
					fail_creation='Account Created'
				else:
					acct_status_Active='Inactive'
					fail_creation='Account requested and awaiting for admin approval'
				insrt_qry='insert into user_login values("'+reg_usr+'","'+reg_pass+'","'+reg_email+'","'+reg_type+'","'+acct_status_Active+'");'
				print(insrt_qry)
				cursor.execute(insrt_qry)
				connection.commit()
		except Error as e:
			print("Error while connecting to MySQL", e)
			usr_exist='Username Already Taken'
			return render(request,'LoginPage.html',{'fail_creation':usr_exist})
		finally:
			if (connection.is_connected()):
				cursor.close()
				connection.close()
				print("MySQL connection is closed")
		return render(request,'LoginPage.html',{'fail_creation':fail_creation})
	else:
		pass_not_matched='Both Passwords not matched'
		return render(request,'LoginPage.html',{'fail_creation':pass_not_matched})

def login_check(request):
	login_usr= request.POST.get('login_username')
	login_pass= request.POST.get('login_password')
	dict={}
	dict['user_name']=login_usr
	dict['user_password']=login_pass
	otp_str=str(random.randint(100000, 999999))
	try:
		connection = mysql.connector.connect(host='localhost',database='Jarvis',user='root',password='Suhu@2016')                                         
		if connection.is_connected():
			db_Info = connection.get_server_info()
			print("Connected to MySQL Server version ", db_Info)
			cursor = connection.cursor()
			cursor.execute("select database();")
			record = cursor.fetchone()
			delet_qry='delete from user_login_check_email where username="'+login_usr+'";'
			print(delet_qry)
			cursor.execute(delet_qry)
			insrt_qry='insert into user_login_check_email values("'+login_usr+'","'+otp_str+'");'
			print(insrt_qry)
			cursor.execute(insrt_qry)
			fet_qry='select email_id from user_login where username="'+login_usr+'";'
			print(fet_qry)
			cursor.execute(fet_qry)
			record=cursor.fetchone()
			connection.commit()
	except Error as e:
		print("Error while connecting to MySQL", e)

	text='gopisairam999@gmail.com'
	MY_ADDRESS=str(text)
	TO_ADDRESS=record[0]
	#print(MY_ADDRESS)    
	text='pqhylspdtjskergd'
	PASSWORD=str(text)
	#print(PASSWORD)
	item_nm=''
	item_descrptn=''
	item_qnt=''
	itm_price=''
	complete_str='Hi,<br><br>YOur OTP to Login:'+otp_str+'<br><br>Thanks,eShopping Team.'
	try:
		context=ssl.create_default_context()
		# set up the SMTP server
		s = smtplib.SMTP(host='smtp.gmail.com', port=587)
		s.ehlo()
		s.starttls(context=context)
		s.ehlo()
		s.login(MY_ADDRESS, PASSWORD)

		#Gmail SMTP server address: smtp.gmail.com
		#Gmail SMTP port (TLS): 587.
		#Gmail SMTP port (SSL): 465.

		msg = MIMEMultipart()       # create a message

		# setup the parameters of the message
		msg['From']=MY_ADDRESS
		msg['To']=TO_ADDRESS
		print("To Address:",msg['To'])
		text="OTP to Login to eShopping"
		msg['Subject']=str(text)
		print(msg['Subject'])
		body = MIMEText(complete_str, 'html')
		#msge=MIMEMultipart()
		msg.attach(body)
		#msge.attach("\n\nThanks,\niClothing Team")
		#message=str(msge)
		# add in the message body
		#msg.attach(MIMEText(message, 'plain'))
		print('sending mail')        
		smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
		smtp_server.starttls()
		smtp_server.login(MY_ADDRESS, PASSWORD)
		smtp_server.sendmail(msg['From'], msg['To'], msg.as_string())
		smtp_server.quit()
		# send the message via the server set up earlier.
		#s.send_message(msg)
		#del msg

		# Terminate the SMTP session and close the connection
		#s.quit()
	
			
		#return render(request,'Admin_after_login.html',dict)
	except Error as e:
		print("Error while connecting to MySQL : ", e)
	return render(request,'Login_Check_Email_Verify.html',dict)

def login_request(request):
	login_usr= request.POST.get('login_username')
	login_pass= request.POST.get('login_password')
	login_otp= request.POST.get('login_otp')
	items=[]
	price=[]
	item_path=[]
	dict={}
	login_invalid='UnSuccessful Login'
	admin_approv_reqsts=''
	user_orders=''
	db_otp=''
	fl2=0
	try:
		connection = mysql.connector.connect(host='localhost',database='Jarvis',user='root',password='Suhu@2016')
		if connection.is_connected():
			db_Info = connection.get_server_info()
			print("Connected to MySQL Server version ", db_Info)
			cursor = connection.cursor()
			cursor.execute("select database();")
			record = cursor.fetchone()
			get_otp='select otp from user_login_check_email where username="'+login_usr+'";'
			print(get_otp)
			cursor.execute(get_otp)
			record = cursor.fetchone()
			db_otp=record[0]
			if(db_otp is not None):
				if(str(db_otp)!=str(login_otp)):
					login_invalid='The Entered OTP is Incorrect.'
					fl2=1
			login_chk_qry='select count(*),account_type,account_status from user_login where username="'+login_usr+'" and password="'+login_pass+'";'
			print(login_chk_qry)
			cursor.execute(login_chk_qry)
			record = cursor.fetchone()
			print(record)
			if(record[0]==1 and fl2==0):
				if(record[2]=='Active'):
					if(record[1]=='User'):
						fetch_query="select item_name,price,item_path from items;"
						print(fetch_query)
						cursor.execute(fetch_query)
						records = cursor.fetchall()
						print(records)
						for i in range(0,len(records)):
							dict['product_no_'+str(i+1)]=records[i][0]
							dict['price_'+str(i+1)]=records[i][1]
							dict['item_path_'+str(i+1)]=records[i][2]
							items.append(records[i][0])
							price.append(records[i][1])
							item_path.append(records[i][2])
						count_imgs=len(items)
						item_paths=''
						for i in range(1,(len(dict)//3)+1):
							item_paths=item_paths+(dict['item_path_'+str(i)])+','
						item_paths=item_paths[:len(item_paths)-1]
						dict['item_paths']=item_paths
						if(count_imgs>1000):
							count_imgs=1000
						dict['total_no_products']=count_imgs
						#dict['total_no_products']=22
						dict['user_name']=login_usr
						#print(dict)
						return render(request,'User_after_login.html',dict)
					elif(record[1]=='Admin'):
						dict={}
						dict['user_name']=login_usr
						login_chk_qry="select username,email_id from user_login where account_type='Admin' and account_status='Inactive';"
						cursor.execute(login_chk_qry)
						record=cursor.fetchall()
						print(record)
						for i in range(1,len(record)+1):
							admin_approv_reqsts=admin_approv_reqsts+str(record[i-1][0])+','+record[i-1][1]+','
							dict['user_name_'+str(i)]=record[i-1][0]
							dict['Email_id_'+str(i)]=record[i-1][1]
						dict['total_no_users']=len(record)
						dict['admin_approv_reqsts']=admin_approv_reqsts[:len(admin_approv_reqsts)-1]
						
						if(len(record)==0):
							dict['no_requests']='No requests Approval Pending'
						
						#ord_chck_qry='select order_id,username,item_name,item_path,item_price,quantity,no_of_days_item_deliver,size from orders limit 20;'
						#ord_chck_qry='select order_id,username,item_name,item_path,item_price,quantity,no_of_days_item_deliver,size from orders;'
						ord_chck_qry="select order_id,username,item_name,item_path,item_price,quantity,no_of_days_item_deliver,size from orders where status='Not Placed';"
						print(ord_chck_qry)
						cursor.execute(ord_chck_qry)
						record=cursor.fetchall()
						dict['tot_orders']=len(record)
						print(record)
						for i in range(0,len(record)):
							dict['od'+str(i+1)]=record[i][1]
							dict['us'+str(i+1)]=record[i][0]
							dict['itm'+str(i+1)]=record[i][2]
							dict['ppq'+str(i+1)]=record[i][4]
							dict['qn'+str(i+1)]=record[i][5]
							dict['sz'+str(i+1)]=record[i][7]
							user_orders=user_orders+str(record[i][0])+','+record[i][1]+','+record[i][2]+','+record[i][4]+','+record[i][5]+','+record[i][7]+','
							tia_chk="select no_of_items_available from items where item_path='"+record[i][3]+"';"
							print(tia_chk)
							try:
								cursor.execute(tia_chk)
								dict['tia'+str(i+1)]=cursor.fetchone()[0]
								user_orders=user_orders+cursor.fetchone()[0]+','
							except:
								dict['tia'+str(i+1)]=0
								user_orders=user_orders+str(0)+','
						dict['user_orders']=user_orders[:len(user_orders)-1]
						print(dict)
						return render(request,'Admin_after_login.html',dict)
					else:
						return render(request,'LoginPage.html')
				else:
					login_invalid='Account is inactive'
			elif(fl2==0):
				login_invalid='Invalid Credentials'
	except Error as e:
		print("Error while connecting to MySQL : ", e)
	return render(request,'LoginPage.html',{'login_invalid':login_invalid})

def retrieve_cred(request):
	return render(request,'Retrieve_credentials.html')

def logout_request(request):
	return render(request,'LoginPage.html',{'login_invalid':'Logged out Successfully'})

def saved_Address(request):
	usernm=request.POST.get('user_name1')
	print(usernm)
	dict={}
	dict['user_name']=usernm
	try:
		connection = mysql.connector.connect(host='localhost',database='Jarvis',user='root',password='Suhu@2016')
		if connection.is_connected():
			db_Info = connection.get_server_info()
			print("Connected to MySQL Server version ", db_Info)
			cursor = connection.cursor()
			cursor.execute("select database();")
			record = cursor.fetchone()
			login_chk_qry='select address_street,address_apt,address_city,address_state,address_pincode,mobile_number,id from user_address where username="'+usernm+'";'
			print(login_chk_qry)
			cursor.execute(login_chk_qry)
			record = cursor.fetchall()
			print(record)
			if(record is not None):
				for i in range(len(record)):
					dict['Apt_Street_'+str(i+1)]='Apt '+record[i][1]+', '+record[i][0]+','
					dict['city_state_zip_'+str(i+1)]=record[i][2]+', '+record[i][3]+', '+record[i][4]+'.'
					dict['mobile'+str(i+1)]=record[i][5]
					dict['id'+str(i+1)]=record[i][6]
				return render(request,'saved_Address.html',dict)
	except Error as e:
		print("Error while connecting to MySQL", e)
	return render(request,'saved_Address.html',{'user_name':usernm})

def add_Address(request):
	print('Add Address')
	usernm=request.POST.get('user_name1')
	street=request.POST.get('street')
	apt=request.POST.get('Apt')
	city=request.POST.get('city')
	state=request.POST.get('state')
	pincode=request.POST.get('pincode')
	mobile=request.POST.get('mobile')
	dict={}
	dict['user_name']=usernm
	try:
		connection = mysql.connector.connect(host='localhost',database='Jarvis',user='root',password='Suhu@2016')
		if connection.is_connected():
			db_Info = connection.get_server_info()
			print("Connected to MySQL Server version ", db_Info)
			cursor = connection.cursor()
			cursor.execute("select database();")
			record = cursor.fetchone()
			login_chk_qry="select count(*) from user_login where username='"+usernm+"';"
			print(login_chk_qry)
			cursor.execute(login_chk_qry)
			record = cursor.fetchone()
			print(record)
			if(record[0]==1):
				login_chk_qry="select max(id) from user_address;"
				print(login_chk_qry)
				cursor.execute(login_chk_qry)
				record = cursor.fetchone()
				print(record)
				if(record[0] is None):
					id=1
				else:
					id=record[0]+1
				if(len(record)<6):
					insert_qry="insert into user_address values("+str(id)+",'"+usernm+"','"+street+"','"+apt+"','"+city+"','"+state+"','"+pincode+"','"+mobile+"');"
					print(insert_qry)
					cursor.execute(insert_qry)
					login_chk_qry='select address_street,address_apt,address_city,address_state,address_pincode,mobile_number,id from user_address where username="'+usernm+'";'
					print(login_chk_qry)
					cursor.execute(login_chk_qry)
					record = cursor.fetchall()
					connection.commit()
					print(record)
					if(record is not None):
						for i in range(len(record)):
							dict['Apt_Street_'+str(i+1)]='Apt '+record[i][1]+', '+record[i][0]+','
							dict['city_state_zip_'+str(i+1)]=record[i][2]+', '+record[i][3]+', '+record[i][4]+'.'
							dict['mobile'+str(i+1)]=record[i][5]
							dict['id'+str(i+1)]=record[i][6]
							dict['Status_of_address']='Address saved successfully'
						return render(request,'saved_Address.html',dict)
					else:
						dict['Status_of_address']='Addresses are Full, Please delete any 1 address and add new Address'
						return render(request,'saved_Address.html',{'user_name':usernm,'Status_of_address':'Addresses are Full, Please delete any 1 address and add new Address'})
	except Error as e:
		print("Error while connecting to MySQL", e)
	return render(request,'saved_Address.html',{'user_name':usernm,'Status_of_address':'Address not saved successfully, Please try again'})

def rld_hmpg_after_login(request):
	usernm=request.POST.get('user_name1')
	print(usernm)
	items=[]
	price=[]
	item_path=[]
	dict={}
	dict['user_name']=usernm
	try:
		connection = mysql.connector.connect(host='localhost',database='Jarvis',user='root',password='Suhu@2016')
		if connection.is_connected():
			db_Info = connection.get_server_info()
			print("Connected to MySQL Server version ", db_Info)
			cursor = connection.cursor()
			cursor.execute("select database();")
			record = cursor.fetchone()
			fetch_query="select item_name,price,item_path from items;"
			print(fetch_query)
			cursor.execute(fetch_query)
			records = cursor.fetchall()
			print(records)
			for i in range(0,len(records)):
				dict['product_no_'+str(i+1)]=records[i][0]
				dict['price_'+str(i+1)]=records[i][1]
				dict['item_path_'+str(i+1)]=records[i][2]
				items.append(records[i][0])
				price.append(records[i][1])
				item_path.append(records[i][2])
			count_imgs=len(items)
			item_paths=''
			for i in range(1,(len(dict)//3)+1):
				item_paths=item_paths+(dict['item_path_'+str(i)])+','
			item_paths=item_paths[:len(item_paths)-1]
			dict['item_paths']=item_paths
			if(count_imgs>1000):
				count_imgs=1000
			dict['total_no_products']=count_imgs
			#dict['total_no_products']=22
			#print(dict)
			return render(request,'User_after_login.html',dict)
	except Error as e:
		print("Error while connecting to MySQL", e)
	return render(request,'User_after_login.html',{'user_name':usernm})

def approve_reject(request):
	data=request.POST.get('user_apr_rej')
	approv=request.POST.get('Approve1')
	user_name=request.POST.get('admn_name')
	print(approv)
	rejct=request.POST.get('Reject1')
	print(rejct)
	print(data)
	admin_approv_reqsts=''
	user_orders=''
	if(approv is not None):
		user_name1=approv.split(' ')[1]
		stat=approv.split(' ')[0]
	else:
		user_name1=rejct.split(' ')[1]
		stat=rejct.split(' ')[0]
	dict={}
	dict['user_name']=user_name	
	status=''
	if(stat=='approve'):
		stat='Active'
		status='Approved'
	else:
		stat='Rejected'
		status='Rejected'
	try:
		connection = mysql.connector.connect(host='localhost',database='Jarvis',user='root',password='Suhu@2016')
		if connection.is_connected():
			db_Info = connection.get_server_info()
			print("Connected to MySQL Server version ", db_Info)
			cursor = connection.cursor()
			cursor.execute("select database();")
			record = cursor.fetchone()
			login_chk_qry="update user_login set account_status='"+stat+"' where username='"+user_name1+"';"
			print(login_chk_qry)
			cursor.execute(login_chk_qry)
			login_chk_qry="select username,email_id from user_login where account_type='Admin' and account_status='Inactive';"
			cursor.execute(login_chk_qry)
			record=cursor.fetchall()
			print(len(record))
			connection.commit()
			if record is not None:
				dict['total_no_users']=len(record)
				for i in range(1,len(record)+1):
					dict['user_name_'+str(i)]=record[i-1][0]
					dict['Email_id_'+str(i)]=record[i-1][1]
					admin_approv_reqsts=admin_approv_reqsts+str(record[i-1][0])+','+record[i-1][1]+','
					dict['done_stat']='User '+status+' Successfully'
					dict['admin_approv_reqsts']=admin_approv_reqsts[:len(admin_approv_reqsts)-1]
					print(dict)
			if(len(record)==0):
				dict['no_requests']='No requests Approval Pending'
				#dict['total_no_users']=0
			ord_chck_qry="select order_id,username,item_name,item_path,item_price,quantity,no_of_days_item_deliver,size from orders where status='Not Placed';"
			print(ord_chck_qry)
			cursor.execute(ord_chck_qry)
			record=cursor.fetchall()
			dict['tot_orders']=len(record)
			print(record)
			for i in range(0,len(record)):
				user_orders=user_orders+str(record[i][0])+','+record[i][1]+','+record[i][2]+','+record[i][4]+','+record[i][5]+','+record[i][7]+','
				tia_chk="select no_of_items_available from items where item_path='"+record[i][3]+"';"
				print(tia_chk)
				try:
					cursor.execute(tia_chk)
					dict['tia'+str(i+1)]=cursor.fetchone()[0]
					user_orders=user_orders+cursor.fetchone()[0]+','
				except:
					dict['tia'+str(i+1)]=0
					user_orders=user_orders+str(0)+','
					dict['user_orders']=user_orders[:len(user_orders)-1]
					print(dict)
			return render(request,'Admin_after_login.html',dict)
	except Error as e:
		print("Error while connecting to MySQL", e)
	dict['done_stat']='User Approval Not Completed, Please try again'
	return render(request,'Admin_after_login.html',dict)

def upld_new(request):
	user_name=request.POST.get('user_name1')
	print(user_name)
	return render(request,'Admin_Upload_New.html',{'user_name':user_name})

def upload_file(request):
	print(request.FILES)
	dict={}
	dict['stat_new_item']='Item not Successfully added to database, Please try again'
	item_name=request.POST.get('item_name')
	department_name1=request.POST.get('category1')
	department_name2=request.POST.get('category2')
	department_name3=request.POST.get('category3')
	path='static/Women/Top Wear'
	item_brand=request.POST.get('item_brand')
	item_size=request.POST.get('item_size')
	item_price=request.POST.get('item_price')
	item_description=request.POST.get('item_des')
	item_tot=request.POST.get('item_tot')
	item_del=request.POST.get('item_del')
	
	dict2={}
	dict2['Men_top_wear']=['T Shirt','Casual Shirt','Men Sweaters','Suits','Jackets','Formal Shirt']
	dict2['Men_Indian_Festive_Wear']=['Men Kurtas','Sherwanis','Dhothis']
	dict2['Men_Bottom_Wear']=['Men Jeans','Track Pants','Boxers','Shorts']
	dict2['Men_Foot_Wear']=['Shoes','Flip Flops','Sandals','Men Socks']

	dict2['Women_Fusion_Wear']=['Sarees','Women Kurtas','Leggings & Churidars','Skirts','Lehenga','Dupattas']
	dict2['Women_Western_Wear']=['Women Dresses','Women Tops','Women Sweaters']
	dict2['Women_Beauty_Care']=['Makeup','Skin Care','Lipsticks','Fragrences']
	dict2['Women_Foot_Wear']=['Casual Shoes','Flats','Heels','Women Sports Shoes']

	dict2['Kids_Infants']=['Body Suites','Kids Dresses','Winter Wear','Inner Wear','Tshirts','Rompers']
	dict2['Kids_Boys_Clothing']=['Shirts','Ethnic Wear','Jeans','Kids Sweaters']
	dict2['Kids_girls_Clothing']=['Tops','TShirt','Dresses','Party wear']
	dict2['Kids_Foot_Wear']=['School Shoes','Sports Shoes','Socks']
	department_name=''
	name_no=0
	try:
		connection = mysql.connector.connect(host='localhost',database='Jarvis',user='root',password='Suhu@2016')
		if connection.is_connected():
			db_Info = connection.get_server_info()
			print("Connected to MySQL Server version ", db_Info)
			cursor = connection.cursor()
			cursor.execute("select database();")
			record = cursor.fetchone()
			login_chk_qry="select max(item_no) from items;"
			print(login_chk_qry)
			cursor.execute(login_chk_qry)
			record=cursor.fetchone()
			print(record)
			if record[0] is not None:
				name_no=record[0]
			name_no=int(name_no)+1
			tab_dep_name=''
			if(department_name1 != 'select'):
				department_name=department_name1
			elif(department_name2 != 'select'):
				department_name=department_name2
			else:
				department_name=department_name3
			for i in dict2:
				if(department_name in dict2[i]):
					tab_dep_name=i
					break
			tab_dep_name=tab_dep_name[:tab_dep_name.find('_')]+'/'+tab_dep_name[tab_dep_name.find('_')+1:]
			path='/static/'+tab_dep_name+'/'+department_name+'/'+department_name+str(time.strftime("%Y%m%d-%H%M"))+str(name_no)+'.png'
			print(item_name+' '+item_brand+' '+item_size+' '+item_price+' '+item_description)
			print('Departments:')
			print(department_name1)
			print(department_name2)
			print(department_name3)
			path='static/'+tab_dep_name+'/'+department_name
			filenm1=department_name+str(time.strftime("%Y%m%d-%H%M"))+str(name_no)+'.png'
			if request.method == 'POST' and request.FILES['myfile']:
				print('if loop')
				myfile = request.FILES['myfile']
				BASE_DIR = Path(__file__).resolve().parent.parent
				print(path)
				settings.MEDIA_ROOT=os.path.join(BASE_DIR, path)
				fs = FileSystemStorage()
				print(myfile)
				filename = fs.save(filenm1, myfile)
				#file_name = default_storage.save(filenm1, file)
				print(filename)
				uploaded_file_url = fs.url(filename)
				dict['stat_new_item']='Item Successfully added to database.'
				insrt_qry="insert into items values ("+str(name_no)+",'"+item_name+"','"+tab_dep_name+"','/"+path+"/"+filenm1+"','"+item_brand+"','"+item_size+"','"+str(item_price)+"','"+item_description+"',"+item_tot+","+item_del+");"
				print(insrt_qry)
				cursor.execute(insrt_qry)
				connection.commit()
				return render(request,'Admin_Upload_New.html',dict)
	except Error as e:
		print("Error while connecting to MySQL", e)
	return render(request,'Admin_Upload_New.html',dict)

def open_cart(request):
	usernm=request.POST.get('user_name1')
	#no_of_items_cart=request.POST.get('cart_val')
	item_paths=request.POST.get('cart_click')
	print(usernm)
	#print(no_of_items_cart)
	item_name=''
	item_price=''
	dict={}
	dict['user_name']=usernm
	item_paths=item_paths.split(',')
	no_of_items_cart=len(item_paths)-1
	query=[]
	for i in range(0,len(item_paths)):
		item_paths[i]=item_paths[i][item_paths[i].find('static')-1:]
		item_paths[i]=item_paths[i].replace('%20',' ')
	print(item_paths)
	try:
		connection = mysql.connector.connect(host='localhost',database='Jarvis',user='root',password='Suhu@2016')
		if connection.is_connected():
			db_Info = connection.get_server_info()
			print("Connected to MySQL Server version ", db_Info)
			cursor = connection.cursor()
			cursor.execute("select database();")
			record = cursor.fetchone()
			login_chk_qry="select item_name,price,item_path,no_of_items_available,no_of_days_item_deliver,size from items;"
			print(login_chk_qry)
			cursor.execute(login_chk_qry)
			record=cursor.fetchall()
			#print(record)
			k=0
			if record[0] is not None:
				for i in range(0,no_of_items_cart):
					for j in range(0,len(record)):
						if(k<no_of_items_cart):
							if(item_paths[i]==record[j][2]):
								k=k+1
								print(record[j][2])
								qry="insert into shopping_cart values('"+usernm+"','"+record[j][0]+"','"+record[j][2]+"','"+record[j][1]+"',1,"+str(record[j][4])+",'L');"
								query.append(qry)
				
				print(query)
				print('no_of_tems_in_cart:'+str(no_of_items_cart))
				for i in range(0,len(query)):
					cursor.execute(query[i])
				#query1="select item_name,item_path,item_price,quantity,no_of_days_item_deliver from shopping_cart where username='"+usernm+"';"
				query1="select sc1.item_name,sc1.item_path,sc1.item_price,sc1.quantity,sc1.no_of_days_item_deliver,it1.no_of_items_available from shopping_cart sc1,items it1 where sc1.item_path=it1.item_path and username='"+usernm+"';"
				print(query1)
				cursor.execute(query1)
				record=cursor.fetchall()
				print(record)
				shp_crt_len=len(record)
				dict['tot_cart_ord']=len(record)
				for i in range(1,len(record)+1):
					dict['item_name'+str(i)]=record[i-1][0]
					dict['price'+str(i)]=record[i-1][2]
					dict['q'+str(i)]=record[i-1][3]
					dict['img_cart_path'+str(i)]=record[i-1][1]
					dict['deliver'+str(i)]=str(record[i-1][4])+' Days to deliver'
					dict['chck_max'+str(i)]=str(record[i-1][5])
					qnt_chk=record[i-1][2]
					if('$' in qnt_chk):
						a=''
						for m in qnt_chk:
							if('$'==m):
								pass
							else:
								a=a+str(m)
						qnt_chk=float(a)
					#print(qnt_chk)
					dict['q_price'+str(i)]=float(int(qnt_chk)*int(record[i-1][3]))
					#print(dict['q'+str(i)])
					#print(dict['price'+str(i)])
					#print(dict['q_price'+str(i)])
				query1="select address_apt,address_street,address_city,address_state,address_pincode,mobile_number from user_address where id = (select max(id) from user_address where username='"+usernm+"');"
				print(query1)
				cursor.execute(query1)
				record=cursor.fetchall()
				print(record)
				dict['user_def_address']=''
				if len(record)==0:
					dict['user_def_address']='Please add the delivery address from profile dropdown'
				else:
					for i in range(0,len(record)):
						dict['add_'+str(i+1)]=''
						for j in record[i]:
							dict['add_'+str(i+1)]=dict['add_'+str(i+1)]+j+','
						dict['add_'+str(i+1)]=dict['add_'+str(i+1)][:len(dict['add_'+str(i+1)])-1]
				connection.commit()
				img_cart_paths=''
				price_str=''
				item_name_str=''
				qnt_str=''
				del_str=''
				q_pr_str=''
				chck_max_str=''
				
				for i in range(0,shp_crt_len):
					img_cart_paths=img_cart_paths+dict['img_cart_path'+str(i+1)]+','
					price_str=price_str+str(dict['price'+str(i+1)])+','
					item_name_str=item_name_str+dict['item_name'+str(i+1)]+','
					qnt_str=qnt_str+str(dict['q'+str(i+1)])+','
					del_str=del_str+dict['deliver'+str(i+1)]+','
					q_pr_str=q_pr_str+str(dict['q_price'+str(i+1)])+','
					chck_max_str=chck_max_str+str(dict['chck_max'+str(i+1)])+','
				
				img_cart_paths=img_cart_paths[:len(img_cart_paths)-1]
				price_str=price_str[:len(price_str)-1]
				item_name_str=item_name_str[:len(item_name_str)-1]
				qnt_str=qnt_str[:len(qnt_str)-1]
				del_str=del_str[:len(del_str)-1]
				q_pr_str=q_pr_str[:len(q_pr_str)-1]
				chck_max_str=chck_max_str[:len(chck_max_str)-1]
				
				dict['img_cart_paths']=img_cart_paths
				dict['price_str']=price_str
				dict['item_name_str']=item_name_str
				dict['qnt_str']=qnt_str
				dict['del_str']=del_str
				dict['q_pr_str']=q_pr_str
				dict['chck_max_str']=chck_max_str
				tot_p=0.0
				for i in range(0,shp_crt_len):
					tot_p=tot_p+float(dict['q_price'+str(i+1)])
				
				tax=round(float(0.2*tot_p),2)
				dict['tax_tot']=tax
				dict['tot_p']=tot_p+tax
				print(dict)
				return render(request,'User_Shopping_Cart.html',dict)
	except Error as e:
		print("Error while connecting to MySQL", e)
	return render(request,'User_Shopping_Cart.html')

def update_addrs(request):
	usernm=request.POST.get('user_name1')
	add_inp=request.POST.get('Address_Any')
	print(add_inp)
	print(usernm)
	add_inp=add_inp.split(',')
	exec_qry=''
	dict={}
	for i in range(len(add_inp)):
		add_inp[i]=add_inp[i].strip()
	if(add_inp[0]=='Delete'):
		exec_qry='Delete from user_address where id = '+add_inp[1]+';'
	else:
		exec_qry="Update user_address set address_street = '"+add_inp[3]+"',address_apt='"+add_inp[2]+"',address_city='"+add_inp[4]+"',address_state='"+add_inp[5]+"',address_pincode='"
		exec_qry=exec_qry+add_inp[6][:add_inp[6].find('.')]+"',mobile_number='"+add_inp[6][add_inp[6].find('.')+1:]+"' where id = "+add_inp[1]+";"
	try:
		connection = mysql.connector.connect(host='localhost',database='Jarvis',user='root',password='Suhu@2016')
		if connection.is_connected():
			db_Info = connection.get_server_info()
			print("Connected to MySQL Server version ", db_Info)
			cursor = connection.cursor()
			cursor.execute("select database();")
			record = cursor.fetchone()
			print(exec_qry)
			cursor.execute(exec_qry)
			login_chk_qry='select address_street,address_apt,address_city,address_state,address_pincode,mobile_number,id from user_address where username="'+usernm+'";'
			print(login_chk_qry)
			cursor.execute(login_chk_qry)
			record = cursor.fetchall()
			print(record)
			if(record is not None):
				for i in range(len(record)):
					dict['Apt_Street_'+str(i+1)]=record[i][1]+', '+record[i][0]+','
					dict['city_state_zip_'+str(i+1)]=record[i][2]+', '+record[i][3]+', '+record[i][4]+'.'
					dict['mobile'+str(i+1)]=record[i][5]
					dict['id'+str(i+1)]=record[i][6]
			connection.commit()
			dict['Status_of_address']='Address Update or Delete Done'
			return render(request,'saved_Address.html',dict)
	except Error as e:
		print("Error while connecting to MySQL", e)
	return render(request,'saved_Address.html',{'user_name':usernm,'Status_of_address':'Address Update or Delete Not Complete Successfully'})
	
def save_cart_checkout(request):
	usernm=request.POST.get('user_name1')
	print(usernm)
	data=request.POST.get('all_data')
	print(data)
	dict={}
	dict['user_name']=usernm
	it_nm=''
	it_pth=''
	it_prce=''
	qnt=0
	it_del_days=0
	sze=''
	tot_no_valid_items=0
	a=data
	try:
		connection = mysql.connector.connect(host='localhost',database='Jarvis',user='root',password='Suhu@2016')
		if connection.is_connected():
			db_Info = connection.get_server_info()
			print("Connected to MySQL Server version ", db_Info)
			cursor = connection.cursor()
			cursor.execute("select database();")
			record = cursor.fetchone()
			delete_qry="delete from shopping_cart where username='"+usernm+"';"
			cursor.execute(delete_qry)
			sel_count="select max(order_id) from orders;"
			cursor.execute(sel_count)
			record=cursor.fetchone()
			print(record)
			if record[0] is None:
				ord_id=0
			else:
				ord_id=int(record[0])+1
			print('ord_id'+str(ord_id))
			for i in range(0,len(data.split('(')[1:])):
				it_nm=((a.split('(')[1:])[i].split(','))[0]
				it_pth=((a.split('(')[1:])[i].split(','))[2]
				it_pth=it_pth[it_pth.find('static')-1:]
				it_pth=it_pth.replace('%20',' ')
				it_prce=((a.split('(')[1:])[i].split(','))[5]
				qnt=int(((a.split('(')[1:])[i].split(','))[3])
				temp=((a.split('(')[1:])[i].split(','))[4]
				it_del_days=int(temp[:temp.find(' ')])
				sze=((a.split('(')[1:])[i].split(','))[1]
				insrt_qry="insert into shopping_cart values('"+usernm+"','"+it_nm+"','"+it_pth+"','"+it_prce+"',"+str(qnt)+","+str(it_del_days)+",'"+sze+"');"
				print(insrt_qry)
				ins_order_qry="insert into orders values("+str(ord_id)+",'"+usernm+"','"+it_nm+"','"+it_pth+"','"+it_prce+"',"+str(qnt)+","+str(it_del_days)+",'"+sze+"','Not Placed');"
				ord_id=ord_id+1
				print(ins_order_qry)
				if(qnt==0):
					pass
				else:
					cursor.execute(insrt_qry)
					cursor.execute(ins_order_qry)
					tot_no_valid_items=tot_no_valid_items+1
			query1="select item_name,item_path,item_price,quantity,no_of_days_item_deliver,size from shopping_cart where username='"+usernm+"';"
			print(query1)
			cursor.execute(query1)
			record=cursor.fetchall()
			print(record)
			shp_crt_len=len(record)
			dict['tot_cart_ord']=len(record)
			for i in range(1,len(record)+1):
				dict['item_name'+str(i)]=record[i-1][0]
				dict['price'+str(i)]=record[i-1][2]
				dict['q'+str(i)]=record[i-1][3]
				dict['img_cart_path'+str(i)]=record[i-1][1]
				dict['size_'+str(i)]=record[i-1][5]
				dict['deliver'+str(i)]=str(record[i-1][4])+' Days to deliver'
				qnt_chk=record[i-1][2]
				if('$' in qnt_chk):
					a=''
					for m in qnt_chk:
						if('$'==m):
							pass
						else:
							a=a+str(m)
					qnt_chk=float(a)
				#print(qnt_chk)
				dict['q_price'+str(i)]=float(int(qnt_chk)*int(record[i-1][3]))
				#print(dict['q'+str(i)])
				#print(dict['price'+str(i)])
				#print(dict['q_price'+str(i)])size_select
			query1="select address_apt,address_street,address_city,address_state,address_pincode,mobile_number from user_address where id = (select max(id) from user_address where username='"+usernm+"');"
			print(query1)
			cursor.execute(query1)
			record=cursor.fetchall()
			print(record)
			dict['user_def_address']=''
			if len(record)==0:
				dict['user_def_address']='Please add the delivery address from profile dropdown'
			else:
				for i in range(0,len(record)):
					dict['add_'+str(i+1)]=''
					for j in record[i]:
						dict['add_'+str(i+1)]=dict['add_'+str(i+1)]+j+','
					dict['add_'+str(i+1)]=dict['add_'+str(i+1)][:len(dict['add_'+str(i+1)])-1]
			connection.commit()
			img_cart_paths=''
			price_str=''
			item_name_str=''
			qnt_str=''
			del_str=''
			q_pr_str=''
			size_select=''
			
			for i in range(0,shp_crt_len):
				img_cart_paths=img_cart_paths+dict['img_cart_path'+str(i+1)]+','
				price_str=price_str+str(dict['price'+str(i+1)])+','
				item_name_str=item_name_str+dict['item_name'+str(i+1)]+','
				qnt_str=qnt_str+str(dict['q'+str(i+1)])+','
				del_str=del_str+dict['deliver'+str(i+1)]+','
				q_pr_str=q_pr_str+str(dict['q_price'+str(i+1)])+','
				size_select=size_select+dict['size_'+str(i+1)]+','
			
			img_cart_paths=img_cart_paths[:len(img_cart_paths)-1]
			price_str=price_str[:len(price_str)-1]
			item_name_str=item_name_str[:len(item_name_str)-1]
			qnt_str=qnt_str[:len(qnt_str)-1]
			del_str=del_str[:len(del_str)-1]
			q_pr_str=q_pr_str[:len(q_pr_str)-1]
			size_select=size_select[:len(size_select)-1]
			
			dict['img_cart_paths']=img_cart_paths
			dict['price_str']=price_str
			dict['item_name_str']=item_name_str
			dict['qnt_str']=qnt_str
			dict['del_str']=del_str
			dict['q_pr_str']=q_pr_str
			dict['size_select']=size_select
			
			tot_p=0.0
			for i in range(0,shp_crt_len):
				tot_p=tot_p+float(dict['q_price'+str(i+1)])
			
			tax=round(float(0.2*tot_p),2)
			dict['tax_tot']=tax
			dict['tot_p']=tot_p+tax
			print(dict)
			return render(request,'User_Shopping_Cart_Save.html',dict)
	except Error as e:
		print("Error while connecting to MySQL", e)
	return render(request,'User_Shopping_Cart_Save.html',{'user_name':usernm})

def pay_page(request):
	usernm=request.POST.get('user_name1')
	return render(request,'payment_form.html',{'user_name':usernm})

def del_ord_email(request):
	usernm=request.POST.get('user_name1')
	#stripe_customer=stripe.Customer.create(email='gopisairam999@gmail.com',source=request.POST['stripeToken'])
	price='prod_Mr6JQ3Yt1MEAOQ'#2$
	YOUR_DOMAIN = 'http://127.0.0.1:8000'
	#price='price_1M8638BgzTJ82KoztYf9Rh4k'request_data['email'],
	checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{'price_data': {'currency': 'usd','product_data': {'name': 'Clothes',},'unit_amount': 50,},'quantity': 1,}],
        mode='payment',success_url='http://127.0.0.1:8000/order_confirm.html',cancel_url='http://127.0.0.1:8000/',)
	#subscription=stripe.Subscription.create(customer=stripe_customer.id,items=[{'price':price}])
	return redirect(checkout_session.url, code=303)
	#return render(request,'order_confirm.html',{'user_name':usernm})

def prod_catalog(request):
	usernm=request.POST.get('user_name1')
	dict={}
	dict['user_name']=usernm
	l=[]
	try:
		connection = mysql.connector.connect(host='localhost',database='Jarvis',user='root',password='Suhu@2016')
		if connection.is_connected():
			db_Info = connection.get_server_info()
			print("Connected to MySQL Server version ", db_Info)
			cursor = connection.cursor()
			cursor.execute("select database();")
			record = cursor.fetchone()
			fetch_qry="select item_name,department_name,brand,size,price,description,no_of_items_available,no_of_days_item_deliver,item_no,item_path from items;"
			cursor.execute(fetch_qry)
			record=cursor.fetchall()
			#print(record)
			dict['total_no_items']=len(record)
			for i in range(0,dict['total_no_items']):
				dict1={}
				dict1["item_no"]=record[i][8]
				dict1["item_name"]=record[i][0]
				dict1["Department"]=record[i][1]
				dict1["Brand"]=record[i][2]
				dict1["Size"]=record[i][3]
				dict1["Price"]=record[i][4]
				dict1["Description"]=record[i][5]
				dict1["Items_Available"]=record[i][6]
				dict1["Items_Delivery_Days"]=record[i][7]
				dict['itnm'+str(i+1)]=record[i][0]
				dict['dpt'+str(i+1)]=record[i][1]
				dict['brnd'+str(i+1)]=record[i][2]
				dict['size'+str(i+1)]=record[i][3]
				dict['price'+str(i+1)]=record[i][4]
				dict['des'+str(i+1)]=record[i][5]
				dict['itmsavl'+str(i+1)]=record[i][6]
				dict['itmsdel'+str(i+1)]=record[i][7]
				dict['itno'+str(i+1)]=record[i][8]
				l.append(dict1)			
			item_no_str=''
			item_name_str=''
			dept_str=''
			brnd_str=''
			size_str=''
			price_str=''
			desc_str=''
			avail_str=''
			no_days_deliver_str=''
			for i in range(0,len(record)):
				item_no_str=item_no_str+str(dict['itno'+str(i+1)])+','
				item_name_str=item_name_str+dict['itnm'+str(i+1)]+','
				#print(dict['itnm'+str(i+1)])
				dept_str=dept_str+dict['dpt'+str(i+1)]+','
				brnd_str=brnd_str+dict['brnd'+str(i+1)]+','
				size_str=size_str+dict['size'+str(i+1)]+','
				price_str=price_str+dict['price'+str(i+1)]+','
				desc_str=desc_str+dict['des'+str(i+1)]+','
				avail_str=avail_str+str(dict['itmsavl'+str(i+1)])+','
				no_days_deliver_str=no_days_deliver_str+str(dict['itmsdel'+str(i+1)])+','
			
			dict['items_val']=json.dumps(l)
			item_no_str=item_no_str[:len(item_no_str)-1]
			item_name_str=item_name_str[:len(item_name_str)-1]
			dept_str=dept_str[:len(dept_str)-1]
			brnd_str=brnd_str[:len(brnd_str)-1]
			size_str=size_str[:len(size_str)-1]
			price_str=price_str[:len(price_str)-1]
			desc_str=desc_str[:len(desc_str)-1]
			avail_str=avail_str[:len(avail_str)-1]
			no_days_deliver_str=no_days_deliver_str[:len(no_days_deliver_str)-1]

			dict['item_no_str']=item_no_str
			dict['item_name_str']=item_name_str
			dict['dept_str']=dept_str
			dict['brnd_str']=brnd_str
			dict['size_str']=size_str
			dict['price_str']=price_str
			dict['desc_str']=desc_str
			dict['avail_str']=avail_str
			dict['no_days_deliver_str']=no_days_deliver_str
			#print(dict)
			return render(request,'Admin_product_catalog.html',dict)
	except Error as e:
		print("Error while connecting to MySQL", e)
	return render(request,'Admin_product_catalog.html',dict)

def prod_cat(request):
	data=request.POST.get('all_data_ed_del')
	print(data)
	usernm=request.POST.get('user_name1')
	dict={}
	dict['user_name']=usernm
	temp_data=data.split('(')[1:]
	l=[]
	list_tuples=[]
	status='Product Catalog Successfully Updated'
	for i in temp_data:
		list_tuples.append(i.split(',')[:-1])
	try:
		connection = mysql.connector.connect(host='localhost',database='Jarvis',user='root',password='Suhu@2016')
		if connection.is_connected():
			db_Info = connection.get_server_info()
			print("Connected to MySQL Server version ", db_Info)
			cursor = connection.cursor()
			cursor.execute("select database();")
			record = cursor.fetchone()
			if('Delete' in data.split(',')[0]):
				for i in list_tuples:
					del_qry='Delete from items where item_no='+str(int(i[0]))+';'
					print(del_qry)
					cursor.execute(del_qry)
			else:
				for i in list_tuples:
					upd_qry="Update items set item_name='"+i[1]+"', department_name='"+i[2]+"', brand='"+i[3]+"',  size='"+i[4]+"', price='"+i[5]+"', description='"+i[6]+"', no_of_items_available='"+str(i[7])+"', no_of_days_item_deliver='"+str(i[8])+"' where item_no="+str(int(i[0]))+";"
					print(upd_qry)
					cursor.execute(upd_qry)
			fetch_qry="select item_name,department_name,brand,size,price,description,no_of_items_available,no_of_days_item_deliver,item_no,item_path from items;"
			cursor.execute(fetch_qry)
			record=cursor.fetchall()
			#print(record)
			dict['total_no_items']=len(record)
			for i in range(0,dict['total_no_items']):
				dict1={}
				dict1["item_no"]=record[i][8]
				dict1["item_name"]=record[i][0]
				dict1["Department"]=record[i][1]
				dict1["Brand"]=record[i][2]
				dict1["Size"]=record[i][3]
				dict1["Price"]=record[i][4]
				dict1["Description"]=record[i][5]
				dict1["Items_Available"]=record[i][6]
				dict1["Items_Delivery_Days"]=record[i][7]
				dict['itnm'+str(i+1)]=record[i][0]
				dict['dpt'+str(i+1)]=record[i][1]
				dict['brnd'+str(i+1)]=record[i][2]
				dict['size'+str(i+1)]=record[i][3]
				dict['price'+str(i+1)]=record[i][4]
				dict['des'+str(i+1)]=record[i][5]
				dict['itmsavl'+str(i+1)]=record[i][6]
				dict['itmsdel'+str(i+1)]=record[i][7]
				dict['itno'+str(i+1)]=record[i][8]
				l.append(dict1)			
			item_no_str=''
			item_name_str=''
			dept_str=''
			brnd_str=''
			size_str=''
			price_str=''
			desc_str=''
			avail_str=''
			no_days_deliver_str=''
			for i in range(0,len(record)):
				item_no_str=item_no_str+str(dict['itno'+str(i+1)])+','
				item_name_str=item_name_str+dict['itnm'+str(i+1)]+','
				#print(dict['itnm'+str(i+1)])
				dept_str=dept_str+dict['dpt'+str(i+1)]+','
				brnd_str=brnd_str+dict['brnd'+str(i+1)]+','
				size_str=size_str+dict['size'+str(i+1)]+','
				price_str=price_str+dict['price'+str(i+1)]+','
				desc_str=desc_str+dict['des'+str(i+1)]+','
				avail_str=avail_str+str(dict['itmsavl'+str(i+1)])+','
				no_days_deliver_str=no_days_deliver_str+str(dict['itmsdel'+str(i+1)])+','
			
			dict['items_val']=json.dumps(l)
			item_no_str=item_no_str[:len(item_no_str)-1]
			item_name_str=item_name_str[:len(item_name_str)-1]
			dept_str=dept_str[:len(dept_str)-1]
			brnd_str=brnd_str[:len(brnd_str)-1]
			size_str=size_str[:len(size_str)-1]
			price_str=price_str[:len(price_str)-1]
			desc_str=desc_str[:len(desc_str)-1]
			avail_str=avail_str[:len(avail_str)-1]
			no_days_deliver_str=no_days_deliver_str[:len(no_days_deliver_str)-1]

			dict['item_no_str']=item_no_str
			dict['item_name_str']=item_name_str
			dict['dept_str']=dept_str
			dict['brnd_str']=brnd_str
			dict['size_str']=size_str
			dict['price_str']=price_str
			dict['desc_str']=desc_str
			dict['avail_str']=avail_str
			dict['no_days_deliver_str']=no_days_deliver_str
			dict['status']=status
		connection.commit()
	except Error as e:
		status='Product Catalog Update is not Successful, Please try again.'
		print("Error while connecting to MySQL", e)
	return render(request,'Admin_product_catalog.html',dict)

def del_order(request):
	login_usr=request.POST.get('admn_name')
	data_str_aprv=request.POST.get('Approve2')
	data_str_rej=request.POST.get('Reject2')
	print(data_str_aprv)
	print(data_str_rej)
	items=[]
	price=[]
	item_path=[]
	print('del order')
	dict={}
	data_str=''
	dict['user_name']=login_usr
	print(dict)
	user_orders=''
	admin_approv_reqsts=''
	text='gopisairam999@gmail.com'
	MY_ADDRESS=str(text)
	TO_ADDRESS=''
	#print(MY_ADDRESS)    
	text='pqhylspdtjskergd'
	PASSWORD=str(text)
	#print(PASSWORD)
	item_nm=''
	item_descrptn=''
	item_qnt=''
	itm_price=''
	complete_str='Hi,<br><br>Please find your Order details below:<br><br>'
	if(data_str_aprv is not None):
		status=data_str_aprv.split(' ')[0]
		data_str=data_str_aprv
	else:
		status=data_str_rej.split(' ')[0]
		data_str=data_str_rej
	print(data_str)
	try:
		connection = mysql.connector.connect(host='localhost',database='Jarvis',user='root',password='Suhu@2016')
		if connection.is_connected():
			db_Info = connection.get_server_info()
			print("Connected to MySQL Server version ", db_Info)
			cursor = connection.cursor()
			cursor.execute("select database();")
			record = cursor.fetchone()
			if(status=='Approve'):
				if(data_str.split(' ')[1]):
					idk=int(data_str.split(' ')[1])
					minus_qnt_qry="select item_path,quantity from orders where order_id="+str(idk)+";"
					print(minus_qnt_qry)
					cursor.execute(minus_qnt_qry)
					record=cursor.fetchall()
					minus_path=record[0][0]
					minus_qnt=record[0][1]
					upd_items="update items set no_of_items_available=no_of_items_available-"+str(minus_qnt)+" where item_path='"+minus_path+"';"
					print(upd_items)
					cursor.execute(upd_items)
					upd_qry_ord="Update orders set status='Placed' where order_id='"+str(idk)+"';"
					cursor.execute(upd_qry_ord)
					#fetch_qry="select item_name,item_path,item_price,quantity,no_of_days_item_deliver,size from orders where order_id="+str(idk)+";"
					fetch_qry="select o.item_name,o.item_path,o.item_price,o.quantity,o.no_of_days_item_deliver,o.size,description from orders o,items i where i.item_path=o.item_path and order_id="+str(idk)+";"
					print(fetch_qry)
					cursor.execute(fetch_qry)
					record=cursor.fetchall()
					for i in range(0,len(record)):
						item_nm=record[i][0]
						item_qnt=record[i][3]
						itm_price=record[i][2]
						item_descrptn=record[i][6]
						#complete_str=complete_str+item_nm+' '+str(item_qnt)+' '+itm_price+' '+item_descrptn+'\n'
						complete_str=complete_str+"<table><thead><tr><th>Product_Name</th><th>Quantity</th><th>Price_per_Unit</th><th>Total_Price</th><th>Description</th></tr></thead><tbody><tr><td>"
						complete_str=complete_str+str(item_nm)+"</td><td>"+str(item_qnt)+"</td><td>$"+str(itm_price)+"</td><td>$"+str(float(itm_price)*float(item_qnt))+"</td><td>"+item_descrptn+"</td></tr></tbody></table><br><br>Your Order has been Approved by Admin.<br><br>Thanks,<br>eShopping Team."
			else:
				if(data_str.split(' ')[1]):
					idk=int(data_str.split(' ')[1])
					print(idk)
					upd_qry_ord="Update orders set status='Rejected' where order_id='"+str(idk)+"';"
					print(upd_qry_ord)
					cursor.execute(upd_qry_ord)
					fetch_qry="select o.item_name,o.item_path,o.item_price,o.quantity,o.no_of_days_item_deliver,o.size,description from orders o,items i where i.item_path=o.item_path and order_id="+str(idk)+";"
					cursor.execute(fetch_qry)
					record=cursor.fetchall()
					print(record)
					for i in range(0,len(record)):
						item_nm=record[i][0]
						item_qnt=record[i][3]
						itm_price=record[i][2]
						item_descrptn=record[i][6]
						#complete_str=complete_str+item_nm+' '+str(item_qnt)+' '+itm_price+'\n'
						#complete_str=complete_str+item_nm+"</td><td>"+str(item_qnt)+"</td><td>$"+str(itm_price)+"</td><td>$"+str(float(itm_price)*float(item_qnt))+"</td></tr></tbody></table>"
						complete_str=complete_str+"<table><thead><tr><th>Product_Name</th><th>Quantity</th><th>Price_per_Unit</th><th>Total_Price</th><th>Description</th></tr></thead><tbody><tr><td>"
						complete_str=complete_str+str(item_nm)+"</td><td>"+str(item_qnt)+"</td><td>$"+str(itm_price)+"</td><td>$"+str(float(itm_price)*float(item_qnt))+"</td><td>"+item_descrptn+"</td></tr></tbody></table><br><br>Your Order has Not been Approved by Admin, Please try to order Again or contact Admin for details!<br><br>Thanks,<br>eShopping Team."
			print(complete_str)
			get_to_email_qry="select email_id from user_login u,orders o where u.username=o.username and o.order_id="+str(idk)+";"
			cursor.execute(get_to_email_qry)
			record=cursor.fetchone()
			print(record)
			if(record is not None):
				pass
			else:
				admin_email_qry="select email_id from user_login where username='"+login_usr+"';"
				cursor.execute(admin_email_qry)
				record=cursor.fetchone()
			TO_ADDRESS=record[0]
			login_chk_qry="select username,email_id from user_login where account_type='Admin' and account_status='Inactive';"
			cursor.execute(login_chk_qry)
			record=cursor.fetchall()
			print(record)
			for i in range(1,len(record)+1):
				dict['user_name_'+str(i)]=record[i-1][0]
				dict['Email_id_'+str(i)]=record[i-1][1]
				admin_approv_reqsts=admin_approv_reqsts+str(record[i-1][0])+','+record[i-1][1]+','
				dict['admin_approv_reqsts']=admin_approv_reqsts[:len(admin_approv_reqsts)-1]

			if record is None:
				dict['total_no_users']=0
			else:
				dict['total_no_users']=len(record)
					
			if(len(record)==0):
				dict['no_requests']='No requests Approval Pending'
			
			#ord_chck_qry='select order_id,username,item_name,item_path,item_price,quantity,no_of_days_item_deliver,size from orders limit 20;'
			ord_chck_qry="select order_id,username,item_name,item_path,item_price,quantity,no_of_days_item_deliver,size from orders where status='Not Placed';"
			print(ord_chck_qry)
			cursor.execute(ord_chck_qry)
			record=cursor.fetchall()
			dict['tot_orders']=len(record)
			print(record)
			for i in range(0,len(record)):
				user_orders=user_orders+str(record[i][0])+','+record[i][1]+','+record[i][2]+','+record[i][4]+','+record[i][5]+','+record[i][7]+','
				tia_chk="select no_of_items_available from items where item_path='"+record[i][3]+"';"
				print(tia_chk)
				try:
					cursor.execute(tia_chk)
					dict['tia'+str(i+1)]=cursor.fetchone()[0]
					user_orders=user_orders+cursor.fetchone()[0]+','
				except:
					dict['tia'+str(i+1)]=0
					user_orders=user_orders+str(0)+','
					dict['user_orders']=user_orders[:len(user_orders)-1]
					print(dict)
			connection.commit()
	except Error as e:
		print("Error while connecting to MySQL", e)
		print("Some error occured and could not send mail. Sorry!")		
			
	try:
		context=ssl.create_default_context()
		# set up the SMTP server
		s = smtplib.SMTP(host='smtp.gmail.com', port=587)
		s.ehlo()
		s.starttls(context=context)
		s.ehlo()
		s.login(MY_ADDRESS, PASSWORD)

		#Gmail SMTP server address: smtp.gmail.com
		#Gmail SMTP port (TLS): 587.
		#Gmail SMTP port (SSL): 465.

		msg = MIMEMultipart()       # create a message

		# setup the parameters of the message
		msg['From']=MY_ADDRESS
		msg['To']=TO_ADDRESS
		print("To Address:",msg['To'])
		text="Invoice of your Order"
		msg['Subject']=str(text)
		print(msg['Subject'])
		body = MIMEText(complete_str, 'html')
		#msge=MIMEMultipart()
		msg.attach(body)
		#msge.attach("\n\nThanks,\niClothing Team")
		#message=str(msge)
		# add in the message body
		#msg.attach(MIMEText(message, 'plain'))
		print('sending mail')        
		smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
		smtp_server.starttls()
		smtp_server.login(MY_ADDRESS, PASSWORD)
		smtp_server.sendmail(msg['From'], msg['To'], msg.as_string())
		smtp_server.quit()
		# send the message via the server set up earlier.
		#s.send_message(msg)
		#del msg

		# Terminate the SMTP session and close the connection
		#s.quit()
	
			
		return render(request,'Admin_after_login.html',dict)
	except Error as e:
		print("Error while connecting to MySQL : ", e)
	return render(request,'LoginPage.html',dict)

def Orders_Login(request):
	usernm=request.POST.get('user_name1')
	item_name=''
	item_price=''
	dict={}
	dict['user_name']=usernm
	query=[]
	try:
		connection = mysql.connector.connect(host='localhost',database='Jarvis',user='root',password='Suhu@2016')
		if connection.is_connected():
			db_Info = connection.get_server_info()
			print("Connected to MySQL Server version ", db_Info)
			cursor = connection.cursor()
			cursor.execute("select database();")
			record = cursor.fetchone()
			query1="select item_name,item_path,item_price,quantity,no_of_days_item_deliver,size,status from orders;"
			print(query1)
			cursor.execute(query1)
			record=cursor.fetchall()
			print(record)
			shp_crt_len=len(record)
			dict['tot_cart_ord']=len(record)
			for i in range(1,len(record)+1):
				dict['item_name'+str(i)]=record[i-1][0]
				dict['price'+str(i)]=record[i-1][2]
				dict['q'+str(i)]=record[i-1][3]
				dict['img_cart_path'+str(i)]=record[i-1][1]
				dict['deliver'+str(i)]=str(record[i-1][4])+' Days to deliver'
				dict['size'+str(i)]=record[i-1][5]
				dict['status'+str(i)]=record[i-1][6]
				qnt_chk=record[i-1][2]
				if('$' in qnt_chk):
					a=''
					for m in qnt_chk:
						if('$'==m):
							pass
						else:
							a=a+str(m)
					qnt_chk=float(a)
				#print(qnt_chk)
			#dict['q_price'+str(i)]='1'
				#print(dict['q'+str(i)])
				#print(dict['price'+str(i)])
			#print(dict['q_price'+str(i)])
			img_cart_paths=''
			price_str=''
			item_name_str=''
			qnt_str=''
			del_str=''
			q_pr_str=''
			chck_max_str=''
			size_str=''
			stat_str=''
			
			for i in range(0,shp_crt_len):
				img_cart_paths=img_cart_paths+dict['img_cart_path'+str(i+1)]+','
				price_str=price_str+str(dict['price'+str(i+1)])+','
				item_name_str=item_name_str+dict['item_name'+str(i+1)]+','
				qnt_str=qnt_str+str(dict['q'+str(i+1)])+','
				del_str=del_str+dict['deliver'+str(i+1)]+','
				size_str=size_str+dict['size'+str(i+1)]+','
				stat_str=stat_str+dict['status'+str(i+1)]+','
				
			
			img_cart_paths=img_cart_paths[:len(img_cart_paths)-1]
			price_str=price_str[:len(price_str)-1]
			item_name_str=item_name_str[:len(item_name_str)-1]
			qnt_str=qnt_str[:len(qnt_str)-1]
			del_str=del_str[:len(del_str)-1]
			q_pr_str=q_pr_str[:len(q_pr_str)-1]
			size_str=size_str[:len(size_str)-1]
			stat_str=stat_str[:len(stat_str)-1]
			
			dict['img_cart_paths']=img_cart_paths
			dict['price_str']=price_str
			dict['item_name_str']=item_name_str
			dict['qnt_str']=qnt_str
			dict['del_str']=del_str
			dict['q_pr_str']=q_pr_str
			dict['size_str']=size_str
			dict['stat_str']=stat_str
			
			#print(dict)
			return render(request,'User_Orders_View.html',dict)
	except Error as e:
		print("Error while connecting to MySQL", e)
	return render(request,'User_Orders_View.html')

def Query_Form(request):
	usernm=request.POST.get('user_name1')
	usr_qry=request.POST.get('user_qry1')
	print(usernm)
	print(usr_qry)
	try:
		connection = mysql.connector.connect(host='localhost',database='Jarvis',user='root',password='Suhu@2016')
		if connection.is_connected():
			db_Info = connection.get_server_info()
			print("Connected to MySQL Server version ", db_Info)
			cursor = connection.cursor()
			cursor.execute("select database();")
			record = cursor.fetchone()
			fet_qry="select max(usr_qry_id) from usr_qry;"
			cursor.execute(fet_qry)
			record=cursor.fetchone()
			print(record)
			if(record[0] is None):
				id1=1;
			else:
				id1=int(record[0])+1
			insrt_qry="insert into usr_qry values("+str(id1)+",'"+usernm+"','"+usr_qry+"');"
			cursor.execute(insrt_qry)
			connection.commit()
	except Error as e:
		print("Error while connecting to MySQL", e)
	return render(request,'User_Orders_qry_after.html',{'user_name':usernm})
def Feedback_Form(request):
	usernm=request.POST.get('user_name1')
	usr_feed=request.POST.get('user_feed1')
	print(usr_feed)
	data=usr_feed.split(')')
	try:
		connection = mysql.connector.connect(host='localhost',database='Jarvis',user='root',password='Suhu@2016')
		if connection.is_connected():
			db_Info = connection.get_server_info()
			print("Connected to MySQL Server version ", db_Info)
			cursor = connection.cursor()
			cursor.execute("select database();")
			record = cursor.fetchone()
			for i in range(0,len(data)-1):
				path_1=data[i][:data[i].find('-')]
				fdbk1=data[i][data[i].find('-')+1:]
				if(fdbk1==''):
					pass
				else:
					insrt_qry="insert into usr_feed_bck values('"+usernm+"','"+path_1+"','"+fdbk1+"');"
					cursor.execute(insrt_qry)
		connection.commit()
	except Error as e:
		print("Error while connecting to MySQL", e)
	return render(request,'User_feedback_qry_after.html',{'user_name':usernm})

def Search_Items(request):
	usernm=request.POST.get('user_name1')
	usr_srch=request.POST.get('search1')
	print(usernm)
	print(usr_srch)
	items=[]
	price=[]
	item_path=[]
	dict={}
	login_invalid=''
	dict['user_name']=usernm
	try:
		connection = mysql.connector.connect(host='localhost',database='Jarvis',user='root',password='Suhu@2016')
		if connection.is_connected():
			db_Info = connection.get_server_info()
			print("Connected to MySQL Server version ", db_Info)
			cursor = connection.cursor()
			cursor.execute("select database();")
			record = cursor.fetchone()
			fetch_query="select item_name,price,item_path,brand,description from items;"
			print(fetch_query)
			cursor.execute(fetch_query)
			records = cursor.fetchall()
			print(records)
			flag=0
			k=0
			for i in range(0,len(records)):
				print(i)
				if(usr_srch.lower() in records[i][2].lower() or usr_srch.lower() in records[i][0] or usr_srch.lower() in records[i][3] or usr_srch.lower() in records[i][4]):
					dict['product_no_'+str(k+1)]=records[i][0]
					dict['price_'+str(k+1)]=records[i][1]
					dict['item_path_'+str(k+1)]=records[i][2]
					items.append(records[i][0])
					price.append(records[i][1])
					item_path.append(records[i][2])
					flag=1
					k=k+1
			if(flag==0):
				print('single not fornd')
				for i in range(0,len(records)):
					flag1=0
					for j in usr_srch.split(' '):
						if((j in records[i][2] or j in records[i][0] or j in records[i][3] or j in records[i][4]) and flag1==0):
							dict['product_no_'+str(k+1)]=records[i][0]
							dict['price_'+str(k+1)]=records[i][1]
							dict['item_path_'+str(k+1)]=records[i][2]
							items.append(records[i][0])
							price.append(records[i][1])
							item_path.append(records[i][2])
							flag1=1
							k=k+1
							
			print(items)
			count_imgs=len(items)
			item_paths=''
			for i in range(1,(len(dict)//3)+1):
				item_paths=item_paths+(dict['item_path_'+str(i)])+','
			item_paths=item_paths[:len(item_paths)-1]
			dict['item_paths']=item_paths
			if(count_imgs>1000):
				count_imgs=1000
			dict['total_no_products']=count_imgs
			print(dict)
			return render(request,'User_after_Search.html',dict)
	except Error as e:
		print("Error while connecting to MySQL", e)
	return render(request,'User_after_Search.html')

def Search_Items2(request):
	usernm=request.POST.get('user_name1')
	usr_srch=request.POST.get('srch_str_1')
	print(usernm)
	print(usr_srch)
	items=[]
	price=[]
	item_path=[]
	dict={}
	login_invalid=''
	dict['user_name']=usernm
	try:
		connection = mysql.connector.connect(host='localhost',database='Jarvis',user='root',password='Suhu@2016')
		if connection.is_connected():
			db_Info = connection.get_server_info()
			print("Connected to MySQL Server version ", db_Info)
			cursor = connection.cursor()
			cursor.execute("select database();")
			record = cursor.fetchone()
			fetch_query="select item_name,price,item_path,brand,description from items;"
			print(fetch_query)
			cursor.execute(fetch_query)
			records = cursor.fetchall()
			print(records)
			flag=0
			k=0
			for i in range(0,len(records)):
				print(i)
				if(usr_srch.lower() in records[i][2].lower() or usr_srch.lower() in records[i][0] or usr_srch.lower() in records[i][3] or usr_srch.lower() in records[i][4]):
					dict['product_no_'+str(k+1)]=records[i][0]
					dict['price_'+str(k+1)]=records[i][1]
					dict['item_path_'+str(k+1)]=records[i][2]
					items.append(records[i][0])
					price.append(records[i][1])
					item_path.append(records[i][2])
					flag=1
					k=k+1
			if(flag==0):
				print('single not fornd')
				for i in range(0,len(records)):
					flag1=0
					for j in usr_srch.split(' '):
						if((j in records[i][2] or j in records[i][0] or j in records[i][3] or j in records[i][4]) and flag1==0):
							dict['product_no_'+str(k+1)]=records[i][0]
							dict['price_'+str(k+1)]=records[i][1]
							dict['item_path_'+str(k+1)]=records[i][2]
							items.append(records[i][0])
							price.append(records[i][1])
							item_path.append(records[i][2])
							flag1=1
							k=k+1
							
			print(items)
			count_imgs=len(items)
			item_paths=''
			for i in range(1,(len(dict)//3)+1):
				item_paths=item_paths+(dict['item_path_'+str(i)])+','
			item_paths=item_paths[:len(item_paths)-1]
			dict['item_paths']=item_paths
			if(count_imgs>1000):
				count_imgs=1000
			dict['total_no_products']=count_imgs
			print(dict)
			return render(request,'User_after_Search.html',dict)
	except Error as e:
		print("Error while connecting to MySQL", e)
	return render(request,'User_after_Search.html')









	

















	