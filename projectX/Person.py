#coding=utf-8

#以下定义了地址类
import base64
class home(object):
	"""docstring for home"""
	def __init__(self, country='china',province='beijing',city='beijing',road='xueyuanlu'):
		self.country=country
		self.province=province
		self.city=city
		self.road=road
	def getcountry(self):
		return country
	def getprovince(self):
		return province
	def getcity(self):
		return city
	def getroad(self):
		return road
	def setcountry(self,c):
		self.country=c
	def setprovince(self,c):
		self.province=c
	def setcity(self,c):
		self.city=c
	def setroad(self,c):
		self.road=c
	
		
		
#以下定义日期的类
class date(object):
	def __init__(self,year=0,month=0,day=0):
		self.year=year
		self.month=month
		self.day=day
	def getyear(self):
		return year
	def getmonth(self):
		return month 
	def getday(self):
		return day
	def setyear(self,c):
		self.year=c
	def setmonth(self,c):
		self.month=c
	def setday(self,c):
		self.day=c
#person name
#		age
#		phone
#		birthday
#		home
#		relationship			
class Person(object):
	#初始化
	def __init__(self, name="NULL",age=0,phone="00000000000",relationship="NULL"):
		self.name=name
		self.age=age
		self.birthday=date(),
		self.home=home()
		self.phone=phone
		self.relationship=relationship
	def getname(self):
		return self.name
	def getage(self):
		return self.age
	def getbirthday(self):
		return self.birthday
	def gethome(self):
		return self.home
	def getphone(self):
		return self.phone
	def getrelationship(self):
		return self.relationship
	def setname(self,n):
		self.name=n
	def setage(self,n):
		self.age=n
	def setphone(self,n):
		self.phone=n
	def setrelationship(self,n):
		self.relationship=n
	def setbirthday(self,y,m,d):
		self.birthday.year=y
		self.birthday.month=m
		self.birthday.day=d
	def sethome(self,c,p,ci,r):
		self.home.country=c
		self.home.province=p
		self.home.city=ci
		self.home.road=r
	
	


if __name__ == '__main__':
	xiaoming=Person('xiaoming')
	xiaoming.sethome('China','shandong','jinan','yanghu')
	print (xiaoming.gethome().province)
	import pickle
	fp=open('people.dat','wb')
	pickle.dump(xiaoming,fp)
	fp.close()
	fp=open('people.dat','rb')
	e=pickle.load(fp)
	print(e.getname())


		
		