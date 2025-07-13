import diff_forms as dff

import sympy as sp

var_names = sp.symbols('x,y,z')
x,y,z = var_names
wpt = dff.WedgeProductTerm
Form = dff.Form
d = dff.d
n0 = 3
names0 = ["d"+str(var_names[i]) \
          for i in range(len(var_names))]

# book{Tu17,
# author = "Tu, Loring W.",
# title = "Differential Geometry: Connections,
# Curvature, and Characteristic Classes (GTM)",
# publisher = "Springer",
# year = "2017"
# }

# where d(F) <-> grad(F) for F a 0-form
# d(F) <-> curl(F) for F a 1-form
# d(F) <-> div(F) for F a 2-form

g = lambda expr,s: sp.diff(expr,s)

f = lambda x,y,z: x**2 + y*x*z + z**2
a = wpt(f(x,y,z),[],n0,names0) # 0-form
F = Form([a],n0,names0)
print(f"F = {F} a 0-form")
print(f"grad(F) = {d(F)} a 1-form")
grad_F = [g(f(x,y,z),x),g(f(x,y,z),y),g(f(x,y,z),z)]
print(f"grad_F = {grad_F} the usual way")

f = lambda x,y,z: [x**2,y*x*z,x*z**2]
F = Form([wpt(f(x,y,z)[i],[i],n0,names0) \
          for i in range(n0)],n0,names0)
print(f"F = {F} a 1-form")
print(f"curl(F) = {d(F)} a 2-form")

e = f(x,y,z)
curl_F = [(g(e[2],y)-g(e[1],z)),
          -(g(e[2],x)-g(e[0],z)),
          (g(e[1],x)-g(e[0],y))]
print(f"curl_F = {curl_F} via usual way")


f = lambda x,y,z: [x**2,y*x*z,z**2]
F = Form([wpt(f(x,y,z)[i],[(i+1)%n0,(i+2)%n0],
        n0,names0) \
        for i in range(n0)],n0,names0)
print(f"F = {F} a 2-form")
print(f"div(F) = {d(F)} a 3-form")
div_F = sum([g(f(x,y,z)[0],x),g(f(x,y,z)[1],y),
             g(f(x,y,z)[2],z)])
print(f"div_F = {div_F} the usual way")


