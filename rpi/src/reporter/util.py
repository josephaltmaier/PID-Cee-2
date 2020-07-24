import time

__gps_last_load_time = 0 # initialize to 0 so we reload when we start up
__gps_location = None
__gps_reload_duration = 300 # 5 minutes

def __load_gps_location():
    return "Joseph Rules"

def get_gps_location():
    global __gps_location
    now = time.time()
    if __gps_location is None or now - __gps_last_load_time > __gps_reload_duration:
        __gps_location = __load_gps_location()
        __gps_load_time = now

    return __gps_location
