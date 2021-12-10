import time

current_time = time.localtime()
print(time.strftime('%y%m%d%H%M%S', current_time))