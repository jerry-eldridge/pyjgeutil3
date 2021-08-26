import sympy
from sympy.combinatorics import Permutation

# permutations here map 0,1,2,3 -> 2,1,3,0 etc.
# That is 0 -> 2; 1 -> 1; 2 -> 3; 3 -> 0, etc.
# The mapping is from range(len(L)) -> L.
pi1 = Permutation([2,1,3,0,5,4])
pi2= Permutation([1,2,3,4,5,0])
pi3 = Permutation([0,1,5, 2,3,4])
a = lambda pi: lambda s: ''.join(pi(s))
f = a(pi1)
g = a(pi2)
h = a(pi3)
# do permutation pi3 to write LaTeX
R = lambda s: "$T_{%s%s\ %s%s%s}^{\ \ %s}$" % tuple(list(h(s)))
def bianchi(s):
    L = []
    for i in range(pi1.order()):
        L.append(R(s))
        s = f(s)
    expr = ' + '.join(L) + " = 0"
    return ""+expr+""
t = "abcdef"
s = ""
for i in range(pi2.order()):
    s = s + bianchi(t)+"<p>\n"
    t = g(t)

mathjax = """
<!DOCTYPE html>
<html>
<head>
<title>Symbols</title>
</head>
<body>
<h1>LaTeX and MathJax Document Formatting of Mathematical Text</h1>
<script type="text/x-mathjax-config">
MathJax.Hub.Config({
  tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']]}
});
</script>
<script type="text/javascript" async
src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.2/MathJax.js?config=TeX-MML-AM_CHTML">
</script>

%s

</body>
</html> 

""" % s
create_and_show = False
if create_and_show:
    fn_save = "shuffle_indices-10239.html"
    f = open(fn_save, 'w')
    f.write(mathjax)
    f.close()
    import os
    os.system(fn_save) # double-click on html file
