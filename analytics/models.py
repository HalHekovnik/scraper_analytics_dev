from django.db import models

class Worker(models.Model):
	name = models.CharField(max_length = 50)
	tag = models.CharField(max_length = 5)
	class Meta:
		db_table = 'workers'

class Reports(models.Model):
	task = models.CharField(max_length = 150)
	type = models.CharField(max_length = 50)
	category = models.CharField(max_length = 50)
	worker = models.ForeignKey(Worker, db_column = "worker")
	time = models.FloatField()
	date = models.DateField()
	tag = models.CharField(max_length = 100)
	class Meta:
		db_table = 'reports'
		
class Lessons(models.Model):
	worker = models.ForeignKey(Worker, db_column = "worker")
	lesson = models.CharField(max_length = 140)
	date = models.DateField()
	class Meta:
		db_table = 'lessons'