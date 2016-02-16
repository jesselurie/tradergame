import re
import string 
import datetime
def open_files():
	x = []
	#https://www.dailyfx.com/calendar
	LAST = open(str("data.txt"))
	regex = re.compile("\d\d:\d\d");
	for L in zip(LAST):
		last_interval = regex.search(str(L))
		try:
			last_interval = regex.search(str(L))
			last_interval = last_interval.group(0)
			x.append(last_interval)
		except Exception as E:
			#x.append(L)
			pass
	return x

sun = ['16:30', '18:50', '19:01', '19:30', '19:30', '21:00', '21:05', '23:30', ]
mon = ['03:00', '05:00','09:00', '16:45', '17:30', '19:30', '21:00', '23:00']
tues = ['02:00', '04:30', '05:00',  '08:30', '09:00', '10:00', '11:30','16:00', '18:30', '18:50', '19:00']
wed = ['04:30','05:00', '07:00', '08:30',  '09:15', '11:30', '14:00', '16:00','16:45', '18:50','19:30',  '20:00', '20:30']
thurs = ['02:00', '04:00', '07:30', '08:30', '10:00', '10:30', '11:00', '13:00', '15:30', '23:30']
fri = [ '00:30', '02:00',  '04:30', '08:00', '08:30', '10:00', '13:00']

week = []
for i in sun:
	week.append(datetime.datetime.strptime(i, "%H:%M"))
for i in mon:
	week.append(datetime.datetime.strptime(i, "%H:%M"))
for i in tues:
	week.append(datetime.datetime.strptime(i, "%H:%M"))
for i in wed:
	week.append(datetime.datetime.strptime(i, "%H:%M"))
for i in thurs:
	week.append(datetime.datetime.strptime(i, "%H:%M"))
for i in fri:
	week.append(datetime.datetime.strptime(i, "%H:%M"))

lvc = 1
diff = []
for i in week:
	try:
		x = week[lvc]-i
		print x
	except Exception as e:
		pass
	lvc = lvc + 1
print diff

