from math import sqrt,asin
from unit_conversion import deg_to_rad
from spherical_coords import *

def EarthRadius(lat):
    phi = lat
    a = 6378137.0 # semi-major axis (equatorial radius)
    b = 6356752.3 # semi-minor axis (polar radius)
    r = (2*a + b)/3.0 # mean radius
    num = (a**2*cos(phi))**2 + (b**2*sin(phi))**2
    den = (a*cos(phi))**2 + (b*sin(phi))**2
    R = sqrt(num/den) # radius
    return R

def EarthDistance(lat1, lon1, lat2, lon2):
     r_earth = 6.371e6 # meters
     r = r_earth
     # lat,lon to spherical coordinates
     lat1 = 90-lat1
     lon1 = 360-lon1
     lat2 = 90-lat2
     lon2 = 360-lon2
     # convert to radians
     lat1, lon1, lat2, lon2 = map(deg_to_rad, [lat1, lon1, lat2, lon2])
     x1 = Spherical_x(r, lat1, lon1)
     y1 = Spherical_y(r, lat1, lon1)
     z1 = Spherical_z(r, lat1, lon1)
     x2 = Spherical_x(r, lat2, lon2)
     y2 = Spherical_y(r, lat2, lon2)
     z2 = Spherical_z(r, lat2, lon2)
     d = sqrt( (x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2 )
     y = d/2
     theta = asin(y/r) # right triangle centered at Earth
     theta = theta*2
     distance = r*theta # meters
     return distance
