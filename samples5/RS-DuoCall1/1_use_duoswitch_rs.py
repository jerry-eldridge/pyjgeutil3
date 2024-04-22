import duoswitch_rs as ds
import parse_duo_rs as dsp

def demo(net,cmds0):
    print(f"-"*60)
    net = dsp.parse(net,cmds0)
    print(f"-"*60)
    return

def demo_shell(net):
    done = False
    while not done:
        print(f"Enter 'q' to quit.")
        cmd = input("cmd> ")
        if cmd.strip() == 'q':
            done = True
            break
        print(f"cmd> {cmd}")
        net = dsp.parse(net,cmd)
    return

sz = 1
net = ds.DuoSwitch('swc0',
            n_i = 2,
            xi=['a[0]','a[1]'],
            xi_sz = [sz,sz],
            n_o = 2,
            xo=['b[0]','b[1]'],
            xo_sz = [sz,sz],
            n_c = 3,
            xc=['c[0]','c[1]','c[2]'],
            xc_sz = [sz,sz,sz],
            )

cmds0 = """
?
assign:0:1:2:5:.1
g:0
g:1
graph
path:0:1
switches:0
switches:1
tracert:0:1
tracert_n:a[0]:swc0.sw1.i.2
chat:0:1:hello
"""
cmds = cmds0
demo(net,cmds)
demo_shell(net)

    
        
