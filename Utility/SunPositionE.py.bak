from math import sqrt,cos,sin,pi,tan,acos,asin,floor,fmod
import datetime
import time

local_timezone = -6 # local time is -6 GMT. Set to location.
luminous_efficacy_sun = 93

# http://www.pveducation.org/pvcdrom/properties-of-sunlight/suns-position
# https://en.wikipedia.org/wiki/Air_mass_(solar_energy)
# https://en.wikipedia.org/wiki/Luminous_efficacy

AU = 149597871.0

seasons = [(3,20),(6,21),(9,22),(12,21)] #equinox, solstice,equinox,solstice
season_names = ["winter","spring","summer","autumn"]

def SunPositionXYZdays(lat,lon,days,hrs,dst=0):
    local_timezone = TimeZoneEstimate(lat,lon)
    local_time = hrs + local_timezone + dst
    zenith = GetZenith(days,local_time,lat,lon)
    AM = Airmass(zenith)
    lux = Lux(zenith)
    S_sunlight = lux/luminous_efficacy_sun
    azimuth = GetAzimuth(days,local_time,lat,lon)
    r = 1
    theta = zenith
    phi = 360 - azimuth
    theta = theta*pi/180.0
    phi = phi*pi/180.0
    x = r*sin(theta)*cos(phi)
    y = r*sin(theta)*sin(phi)
    z = r*cos(theta)
    return [x,y,z]

def SunPositionXYZ(lat,lon,hrs,dst=0):
    year = datetime.date.today().year
    month = datetime.date.today().month
    day = datetime.date.today().day
    days = DayOfYear(year,month,day)
    return SunPositionXYZdays(lat,lon,days,hrs,dst)

# This is only approximate as Daylight Savings Time at
# 2 am on the second Sunday in March and reverts to
# standard time on first Sunday in November. I set
# it to noon, or midnight, March 1 and Nov 1.
def EstimateDST():
    t1 = datetime.datetime.now()
    secs = time.mktime(t1.timetuple())
    secs1 = Seconds(t1.year,3,1) # make start of dst
    secs2 = Seconds(t1.year,11,1) # make end of dst
    if secs >= secs1 and secs <= secs2:
        dst = 1
    else:
        dst = 0
    return dst

def CurrentSunPosition(lat,lon,dst=0):
    t1 = datetime.datetime.now()
    secs = time.mktime(t1.timetuple())
    minute = 60
    hour = 60*minute
    day = 24*hour
    secs = fmod(secs,day)
    hrs = 1.0*secs/hour
    dst = EstimateDST()
    pt = SunPositionXYZ(lat,lon,hrs,dst)
    return pt

def Seconds(year,month,day, hour=0, minute=0, second=0):
    t = datetime.datetime(year,month,day,hour,minute,second)
    seconds = time.mktime(t.timetuple())
    return seconds

def Date(seconds):
    date = datetime.datetime.fromtimestamp(seconds).strftime('%Y-%m-%d %H:%M:%S')
    return date

def DayOfYear(year,month,day):
    t = datetime.datetime(year,month,day,0,0,0)
    day_of_year = t.timetuple().tm_yday
    return day_of_year

def EarthOrbitDistance(seconds):
    day = 86400
    year = day*365.25 #seconds (Julian year)
    deg = seconds*360.0/year
    angle = deg*pi/180
    perihelion = 147098290.0 #jan 3 m
    aphelion = 152098232.0 #july 4 m
    a0 = (perihelion + aphelion)
    c0 = a0 - perihelion
    b0 = sqrt(a0**2- c0**2)
    x1 = a0*cos(angle)
    y1 = b0*sin(angle)
    x2 = c0
    y2 = 0
    r = sqrt((x1-x2)**2+(y1-y2)**2) # meters
    return r

def S(airmass):
    """
    Solar intensity
    """
    I0 = 1353 # Watts/meter**2
    AM = airmass
    return 1.1 * I0 * 0.7**(AM**0.678)

def Airmass(zenith_angle):
    z = zenith_angle*pi/180.0
    r_earth = 6371 #km
    y_atm = 9 # km
    r = 1.0*r_earth/y_atm
    AM = sqrt((r*cos(z))**2 + 2*r + 1) - r*cos(z)
    return AM

def Lux(zenith_angle):
    """
    luminous_efficacy_sun = 93
    lux = S*luminous_efficacy_sun
    """
    z = zenith_angle
    AM = Airmass(z)
    S_sunlight = S(AM)
    lux = S_sunlight*luminous_efficacy_sun
    return lux

def LSTM(local_timezone):
    """
    Local Standard Time Meridian
    """
    GMT = 24 # greenwich mean time in hours
    LT = 24-local_timezone 
    dTGMT = GMT-LT
    lstm = 15*dTGMT
    return lstm

def EoT(days):
    """
    Equation of Time(Eot)
    """
    d = days
    B = 360/365.0*(d-81)
    B = B*pi/180.0
    eot = 9.87*sin(2*B)-7.53*cos(B)-1.5*sin(B)
    return eot

def LST(days,local_time,local_timezone,longitude):
    """
    Local Solar Time(LST)
    """
    LT = local_time # hours
    TC = 4*(longitude-LSTM(local_timezone))+EoT(days)
    lst = LT + TC/60.0
    time_correction = TC
    return lst,time_correction

def HRA(local_solar_time):
    """
    Hour Angle
    """
    lst = local_solar_time
    hra = 15*(lst-12)
    return hra

def Declination(days):
    """
    days is number of days since start of year
    """
    delta = 23.45*sin(360/365.0*(days-81)*pi/180.0)
    return delta

def Elevation(latitude,declination,hra):
    """
    Elevation of sun at latitude and declination
    """
    psi = latitude*pi/180.0
    delta = declination*pi/180.0
    hra_rad = hra*pi/180.0
    alpha = asin(sin(delta)*sin(psi)+\
                 cos(delta)*cos(psi)*cos(hra_rad))
    alpha = alpha*180/pi
    return alpha

def Azimuth(latitude,declination,hra):
    """
    Elevation of sun at latitude and declination

    https://en.wikipedia.org/wiki/Solar_azimuth_angle
    phi = local latitude
    delta = declination
    h = hra = hour angle
    theta_s = alpha = solar elevation angle
    phi_s = azimuth = solar azimuth angle

    azimuth returned is in degrees which is degrees
    clockwise from north 0. East is 90, South is 180,
    West is 270.
    """
    phi = latitude*pi/180.0
    delta = declination*pi/180.0
    hra_rad = hra*pi/180.0
    alpha = Elevation(latitude,declination,hra_rad)*pi/180.0
    try:
        azimuth = acos((sin(delta)*cos(phi)-\
        cos(delta)*sin(phi)*cos(hra_rad))/cos(alpha))
        azimuth = azimuth*180/pi
        return azimuth
    except:
        return 0

def Zenith(latitude,declination,hra):
    """
    Zenith of sun at latitude and declination
    up direction.
    """
    alpha = Elevation(latitude,declination,hra)
    zenith = 90-alpha
    return zenith

def SunriseSunset(latitude,declination,time_correction):
    latitude = max(-88,latitude)
    latitude = min(88,latitude)
    psi = latitude*pi/180.0
    delta = declination*pi/180.0
    tc = time_correction
    a = -tan(psi)*tan(delta)
    try:
        sunrise = 12 - 1/15.0*acos(a)*180/pi-tc/60.0
        sunset = 12 + 1/15.0*acos(a)*180/pi-tc/60.0
    except:
        print "Error (SunriseSunset):lat,declination=",latitude,declination
        sunrise,sunset = 0,0
    return sunrise,sunset

def GetSunriseSunset(days,local_time,latitude,longitude):
    declination = Declination(days)
    local_timezone = TimeZoneEstimate(latitude,longitude)
    lst,time_correction = LST(days,local_time,local_timezone,longitude)
    return SunriseSunset(latitude,declination,time_correction)
def GetZenith(days,local_time,latitude,longitude):
    declination = Declination(days)
    local_timezone = TimeZoneEstimate(latitude,longitude)
    lst,tc = LST(days,local_time,local_timezone,longitude)
    hra = HRA(lst)
    return Zenith(latitude,declination,hra)
def GetAzimuth(days,local_time,latitude,longitude):
    declination = Declination(days)
    local_timezone = TimeZoneEstimate(latitude,longitude)
    lst,tc = LST(days,local_time,local_timezone,longitude)
    hra = HRA(lst)
    azimuth = Azimuth(latitude,declination,hra)
    if lst <= 12 or hra <= 0:
        return azimuth
    if lst > 12 or hra > 0:
        return 360-azimuth

def DisplayDay(lat,lon,day_of_year):
    local_timezone = TimeZoneEstimate(lat,lon)
    print "DisplayDay"
    days = day_of_year  # "August 2" (wikipedia) is 214. Set to day to calculate for.
    local_time = 12 # hours
    print "lat,lon=",[lat,lon],"timezone=",local_timezone
    year = datetime.date.today().year
    month = datetime.date.today().month
    day = datetime.date.today().day
    d = datetime.date(year, 1, 1) + datetime.timedelta(day_of_year - 1)
    print "day of year = (", day_of_year,")",d
    print "Sunrise,Sunset=",GetSunriseSunset(days,local_time,lat,lon)
    print "As the sun travels the sky, it is at a zenith angle from"
    print "up/sky. It creates light with irradiance (Watts/meter**2) S"
    print "and illuminance (lux) and AM (solar energy atmospheric mass)."
    print "azimuth is sun's position clockwise from north (0 degrees),"
    print "east of 90, south of 180 and west of 270. zenith is angle from up"
    s = "  t zenith irradiance illum.   AM  azimuth      Sun[x,y,z]    window_angle  window_illum."
    print s
    s = "hrs   degs  W/m**2    lux      AM    degs      N/S W/E U/D        degs         lux"
    print s
    t = 0
    dt = 0.5 # hours
    year = d.day
    month = d.month
    day = d.day
    # window
    # obtain the window vector by finding two lat,lon points
    # pointing away from window:
    # import numpy as np
    # W = np.array([lat,lon,0])
    # import vectors as v
    # W = W/v.norm(W)
    # W[1] *= -1 # to switch direction of E/W to get outward normal
    W = [0.71898838,0.6950221,0.] #normal to window
    import vectors as v
    while t <= 24:
        local_time = t
        z = GetZenith(days,local_time,lat,lon)
        AM = Airmass(z)
        lux = Lux(z)
        S_sunlight = lux/luminous_efficacy_sun
        azimuth = GetAzimuth(days,local_time,lat,lon)
        pt = SunPositionXYZ(lat,lon,local_time)
        pt = map(lambda val: round(val*100000)/100000.0, pt)
        window_angle = v.angle(W,pt)
        lux_window = max(0,cos(window_angle*pi/180)*lux)
        s = '%4.1f %5.1f %6.1f %8.1f %6.1f %6.1f  %s  %5.1f %8.1f' % (t,z,S_sunlight,lux,AM,azimuth,str(pt),window_angle,lux_window)
        print s
        t += dt
    print "="*30
    return


def Lux_time(seconds,lat,lon):
    day = 86400
    hour = day/24.0
    t = fmod(seconds/hour,24.0)
    local_time = t
    d = datetime.datetime.fromtimestamp(seconds)
    year0,month0,day0 = d.year,d.month,d.day
    days = DayOfYear(year0,month0,day0)
    z = GetZenith(days,local_time,lat,lon)
    lux = Lux(z)
    return lux
def S_sunlight_time(seconds,lat,lon):
    lux = Lux_time(seconds,lat,lon)
    S_sunlight = lux/luminous_efficacy_sun
    return S_sunlight

def Integral(f,a,b,dx):
    x = a
    s = 0
    while x < b:
        s += f(x)*dx
        x += dx
    return s

def Derivative(f,x,dx):
    slope = 1.0*(f(x+dx)-f(x))/dx
    return slope

def DisplayYear(lat,lon,year1,month1,day1,year2,month2,day2):
    print "DisplayYear"
    print "lat,lon=",[lat,lon]
    print year1,month1,day1,"to",year2,month2,day2
    total_lux = 0
    total_S_sunlight = 0
    seconds1 = Seconds(year1,month1,day1)
    seconds2 = Seconds(year2,month2,day2)
    print "From ",Date(seconds1)," to ",Date(seconds2)
    Tmin = seconds1
    Tmax = seconds2
    day = 86400
    hour = day/24.0
    dT = 0.5*hour # hours
    total_lux = Integral(lambda T: Lux_time(T,lat,lon),Tmin,Tmax,dT)
    total_S_sunlight = Integral(lambda T: S_sunlight_time(T,lat,lon),Tmin,Tmax,dT)
    print "Average Yearly Illuminance (lux) = ", total_lux/(Tmax-Tmin)
    print "Average Yearly Irradiance (W/m**2) = ", total_S_sunlight/(Tmax-Tmin)
    print "="*30
    return

def TimeZoneEstimate(lat,lon):
    tc = int(lon*24/360)
    return tc

sgn = 1
def U(X):
    global sgn
    lat,lon, = X
    print "lat,lon:",int(X[0]*10000)/10000.0,int(X[1]*10000)/10000.0,
    oo = 1e100
    #sgn 1 to minimize, -1 to maximize
    if abs(lat) >= 90:
        total_lux = oo+(abs(lat)-90)**2
        #print total_lux
        print
        return total_lux
    if abs(lon) >= 180:
        total_lux = oo+(abs(lon)-180)**2
        #print total_lux
        print
        return total_lux
    global local_timezone
    local_timezone = TimeZoneEstimate(lat,lon)
    #print "tc=",local_timezone,
    day = 86400
    hour = day/24.0
    Tmin = Seconds(2015,1,1,0,0,0)
    Tmax = Seconds(2015,12,31,23,59,59)
    dT = 0.5*hour # hours
    total_lux = Integral(lambda T: Lux_time(T,lat,lon),Tmin,Tmax,dT)
    print "avg lux:",1.0*total_lux/(Tmax-Tmin)
    return sgn*total_lux
