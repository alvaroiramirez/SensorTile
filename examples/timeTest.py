# import time

# current_time = time.localtime()
# print(time.strftime('%y%m%d%H%M%S', current_time))


from datetime import datetime, timedelta

# data = 40051
# timestamp = datetime(2021,12,10,11,00,00,data)
# print(timestamp)

# now = datetime.now()
# data_str = '%09.6f' % (data / 1000000)
# dt = now.strftime("%m/%d/%Y, %H:%M:") + data_str
# print(dt)


ms = 40051
print(f'%02f:%02f:%02f.%03f', ms/(60*60*1000)%24, ms/(60*1000)%60, (ms/1000)%60, ms%1000)

now = datetime.now()
new = now + timedelta(milliseconds=2500)

print(f'now: {now}')
print(f'new: {new}')
