import cayleydickson as cd

CD = cd.CayleyDickson
L2CD = cd.List2CD

def Display(title,aa,bb):
    print(f"{title}:")
    print(f"aa = {aa}")
    print(f"bb = {bb}")
    cc = aa * bb
    print(f"cc = aa * bb = {cc}")
    cc = aa + bb
    print(f"cc = aa + bb = {cc}")
    cc = aa - bb
    print(f"cc = aa - bb = {cc}")
    dd = cc*4
    print(f"dd = cc*4 = {dd}")
    print()
    return

# length must be 2**n for integer n

# complex numbers
A = [2,3]
B = [4,12]
aa = L2CD(A)
bb = L2CD(B)
Display("Complex Numbers",aa,bb)

# quaternions
A = [2,3,2,5]
B = [4,12,2,-1]
aa = L2CD(A)
bb = L2CD(B)
Display("Quaternions",aa,bb)

# octonions
A = [2,3,2,5, 8,1,2,3]
B = [4,12,2,-1, 5,2,0,2]
aa = L2CD(A)
bb = L2CD(B)
Display("Octonions",aa,bb)

# sedenions
A = [2,3,2,5, 8,1,2,3, 5,6,1,0, 1,2,3,4]
B = [4,12,2,-1, 5,2,0,2, 0,0,1,0, 1,1,1,0]
aa = L2CD(A)
bb = L2CD(B)
Display("Sedenions",aa,bb)

