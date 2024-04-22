import vswitch as vs

sz = 1
net = vs.vCrossBarSwitch('sw0',
        n_i = 2, xi=['a[0]','a[1]'], xi_sz = [sz,sz],
        n_o = 2, xo=['b[0]','b[1]'],xo_sz = [sz,sz])
n = net.get_label((0,1,1))
addr = net.name_to_addr(n)
p = net.addr_to_port(addr)
print(net.P)
print(p.getdat())

G = net.get_graph()
print(f"G = {G}")
x = net.to_addr(a=0,t=0,sz=1)
y = net.to_addr(a=1,t=1,sz=1)
net.link(x,y)
path = net.get_path(a=0,b=1)
print(f"path = {path}")
