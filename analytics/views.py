from analytics.models import Reports, Lessons, Worker
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.utils import simplejson
from django.db.models import Sum
from datetime import date, timedelta, datetime



def all(request):
	if request.POST:
		kwargs = {}
		cat = request.POST['category']
		if cat == "None":
			kwargs['category__isnull'] = True
		elif cat == "Any":
			pass
		else:
			kwargs['category__icontains'] = cat
		try:
			worker = Worker.objects.get(pk = request.POST['worker'])
		except:
			pass
		else:
			kwargs['worker'] = worker
		try:
			task = request.POST['task']
		except:
			pass
		else:
			kwargs['task__icontains'] = task
		start = datetime.strptime(request.POST['start'], "%d.%m.%Y")
		end = datetime.strptime(request.POST['stop'], "%d.%m.%Y")
		day = start
		return threeLines(request, kwargs, start, end)
		#return oneLine(request, kwargs, start, end)
	categorie = Reports.objects.all()
	categories = []
	for category in categorie:
		cat = str(category.category)
		cat = cat.strip()
		if cat in categories:
			continue
		else:
			if cat == "None":
				continue
			else:
				categories.append(cat)
	workers = Worker.objects.all()
	return render_to_response('home.html', {'categories':categories, 'workers':workers}, context_instance=RequestContext(request))

	
	
def individual(request):
	if request.POST:
		kwargs = {}
		try:
			worker = Worker.objects.get(pk = request.POST['worker'])
		except:
			pass
		else:
			kwargs['worker'] = worker
		start = datetime.strptime(request.POST['start'], "%d.%m.%Y")
		end = datetime.strptime(request.POST['stop'], "%d.%m.%Y")
		day = start
		return threeLines(request, kwargs, start, end)
		#return oneLine(request, kwargs, start, end)
	workers = Worker.objects.all()
	return render_to_response('worker.html', {'workers':workers}, context_instance=RequestContext(request))



def category(request):
	if request.POST:
		kwargs = {}
		cat = request.POST['category']
		if cat == "None":
			cat = None
			kwargs['category'] = cat
		else:
			kwargs['category__icontains'] = cat
		start = datetime.strptime(request.POST['start'], "%d.%m.%Y")
		end = datetime.strptime(request.POST['stop'], "%d.%m.%Y")
		day = start
		return threeLines(request, kwargs, start, end)
	categorie = Reports.objects.all()#.values_list('category', flat=True)
	categories = []
	for category in categorie:
		cat = str(category.category)
		cat = cat.strip()
		if cat in categories:
			continue
		else:
			if cat == "None":
				continue
			else:
				categories.append(cat)
	return render_to_response('category.html', {'categories':categories}, context_instance=RequestContext(request))



def task(request):
	if request.POST:
		kwargs = {}
		try:
			cat = request.POST['task']
		except:
			pass
		else:
			kwargs['task__icontains'] = cat
		start = datetime.strptime(request.POST['start'], "%d.%m.%Y")
		end = datetime.strptime(request.POST['stop'], "%d.%m.%Y")
		day = start
		return threeLines(request, kwargs, start, end)
	return render_to_response('task.html', context_instance=RequestContext(request))
	
	
	
def threeLines(request, kwargs, start, end):
	day = start
	string = '["Day","Systemized","Unsystemized","On system"],'
	sys_sum = 0
	onsys_sum = 0
	unsys_sum = 0
	while day <= end:
		sys = Reports.objects.filter(type = "SYSTEMIZED", date = day).filter(**kwargs).aggregate(Sum('time'))['time__sum']
		unsys = Reports.objects.filter(type = "UNSYSTEMIZED", date = day).filter(**kwargs).aggregate(Sum('time'))['time__sum']
		onsys = Reports.objects.filter(type = "ON SYSTEM", date = day).filter(**kwargs).aggregate(Sum('time'))['time__sum']
		day_str = str(day.strftime("%d.%m"))
		if sys == None:
			sys = 0
		if onsys == None:
			onsys = 0
		if unsys == None:
			unsys = 0
		string += '["' + day_str + '",' + str(sys)+ ',' + str(unsys)+ ',' + str(onsys)+'],'
		sys_sum += sys
		onsys_sum += onsys
		unsys_sum += unsys
		day = day + timedelta(days = 1)
	string = string[0:len(string)-1]
	string1 = '["Type","Time"],["Systemized",'+str(sys_sum)+',],["Unsystemized",'+str(unsys_sum)+'],["On system",'+str(onsys_sum)+']'
	return render_to_response('graph.html', {'string':string, 'string1':string1})


	
def oneLine(request, kwargs, start, end):
	day = start
	string = '["Day","Time","Plan"],'
	while day <= end:
		time = Reports.objects.filter(date = day).exclude(type = "PLAN").filter(**kwargs).aggregate(Sum('time'))['time__sum']
		plan = Reports.objects.filter(date = day).filter(type = "PLAN").filter(**kwargs).aggregate(Sum('time'))['time__sum']
		day_str = str(day.strftime("%d.%m"))
		if time == None:
			time = 0
		if plan == None:
			plan = 0
		string += '["' + day_str + '",' + str(time)+',' + str(plan)+'],'
		day = day + timedelta(days = 1)
	string = string[0:len(string)-1]
	return render_to_response('graph.html', {'string':string})

	

def compareCategories(request):
	categorie = Reports.objects.all()
	categories = []
	workers = Worker.objects.all()
	for category in categorie:
		cat = str(category.category)
		cat = cat.strip()
		cat = cat.lower()
		if cat in categories:
			continue
		else:
			if cat == "none":
				continue
			else:
				categories.append(cat)
	if request.POST:
		kwargs = {}
		#start = datetime.strptime(request.POST['start'], "%d.%m.%Y")
		#end = datetime.strptime(request.POST['stop'], "%d.%m.%Y")
		week = date.today().isocalendar()[1]
		start, end = get_week_days(2013, week-1)
		day = start
		try:
			worker = Worker.objects.get(pk = request.POST['worker'])
		except:
			pass
		else:
			kwargs['worker'] = worker
		end_categories = []
		string = '["Day",'
		for item in categories:
			try:
				cat = request.POST[str(item)]	
			except:
				continue
			else:
				end_categories.append(cat)
				string += '"'+cat+'",'
		string = string[0:len(string)-1]
		string += '],'
		while day <= end:
			day_str = str(day.strftime("%d.%m"))
			string += '["'+day_str+'",'
			for item in end_categories:
				kwargs['category__icontains'] = item
				time = Reports.objects.filter(date = day).exclude(type = "PLAN").filter(**kwargs).aggregate(Sum('time'))['time__sum']
				if time == None:
					time = 0
				string += str(time)+','
			string = string[0:len(string)-1]
			string += '],'
			day = day + timedelta(days = 1)
		string = string[0:len(string)-1]
		string1 = '["Category","Time"],'
		for item in end_categories:
			string1 += '["'+str(item)+'",'
			day = start
			sum = 0
			kwargs['category__icontains'] = item
			while day <= end:
				time = Reports.objects.filter(date = day).exclude(type = "PLAN").filter(**kwargs).aggregate(Sum('time'))['time__sum']
				if time == None:
					time = 0
				sum += time
				day = day + timedelta(days = 1)
			string1 += str(sum)+'],'
		string1 = string1[0:len(string1)-1]
		return render_to_response('graph.html', {'string':string, 'string1':string1})
	return render_to_response('category.html', {'categories':categories, 'workers':workers}, context_instance=RequestContext(request))
			


def table(request):
	if request.POST:
		kwargs = {}
		start = datetime.strptime(request.POST['start'], "%d.%m.%Y")
		end = datetime.strptime(request.POST['stop'], "%d.%m.%Y")
		day = start
		categorie = Reports.objects.filter(date__gte = start).filter(date__lte = end)
		categories = []
		tags = []
		workers = Worker.objects.all()
		for category in categorie:
			cat = str(category.category)
			cat = cat.strip()
			cat = cat.lower()
			if cat in categories:
				continue
			else:
				if cat == "none":
					continue
				else:
					categories.append(cat)
		for category in categorie:
			cat = str(category.tag)
			cat = cat.strip()
			cat = cat.lower()
			if cat in tags:
				continue
			else:
				if cat == "none":
					continue
				else:
					tags.append(cat)
		matrix = []
		line = []
		line.append("")
		for categorija in categories:
			line.append(categorija)
		matrix.append(line)
		for tag in tags:
			line = []
			line.append(tag)
			for categorija in categories:
				time = Reports.objects.filter(category__icontains = categorija, tag__icontains = tag, date__gt = start, date__lt = end).aggregate(Sum('time'))['time__sum']                                          
				if time == None:
					time = "-"
				line.append(time)
			matrix.append(line)
		return render_to_response('table.html', {'matrix':matrix})
	return render_to_response('table.html', context_instance=RequestContext(request))
	


def get_week_days(year, week):
    d = date(year,1,1)
    if(d.weekday()>3):
        d = d+timedelta(7-d.weekday())
    else:
        d = d - timedelta(d.weekday())
    dlt = timedelta(days = (week-1)*7)
    return d + dlt,  d + dlt + timedelta(days=6)




		