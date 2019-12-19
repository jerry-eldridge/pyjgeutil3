from math import sqrt
##  public domain function by Darel Rex Finley, 2006
##  Determines the intersection point of the line segment defined by points A and B
##  with the line segment defined by points C and D.
##  Returns YES if the intersection point was found, and stores that point in X,Y.
##  Returns NO if there is no determinable intersection point, in which case X,Y will
##  be unmodified. [with minor edits by JGE]
def SegmentIntersect(Ax, Ay, Bx, By, Cx, Cy, Dx,  Dy):
    X = Y = -999
    #  Fail if either line segment is zero-length.
    if (Ax==Bx and Ay==By or Cx==Dx and Cy==Dy):
        return False,X,Y;

    #  Fail if the segments share an end-point.
    if (Ax==Cx and Ay==Cy or Bx==Cx and By==Cy
    or  Ax==Dx and Ay==Dy or Bx==Dx and By==Dy):
        return False,X,Y;


    #  (1) Translate the system so that point A is on the origin.
    Bx-=Ax; By-=Ay;
    Cx-=Ax; Cy-=Ay;
    Dx-=Ax; Dy-=Ay;

    #  Discover the length of segment A-B.
    distAB=sqrt(Bx*Bx+By*By);

    #  (2) Rotate the system so that point B is on the positive X axis.
    theCos=Bx/distAB;
    theSin=By/distAB;
    newX=Cx*theCos+Cy*theSin;
    Cy  =Cy*theCos-Cx*theSin; Cx=newX;
    newX=Dx*theCos+Dy*theSin;
    Dy  =Dy*theCos-Dx*theSin; Dx=newX;

    #  Fail if segment C-D doesn't cross line A-B.
    if (Cy<0. and Dy<0. or Cy>=0. and Dy>=0.):
        return False,X,Y;

    #  (3) Discover the position of the intersection point along line A-B.
    ABpos=Dx+(Cx-Dx)*Dy/(Dy-Cy);

    #  Fail if segment C-D crosses line A-B outside of segment A-B.
    if (ABpos<0. or ABpos>distAB):
        return False,X,Y;

    #  (4) Apply the discovered position to line A-B in the original coordinate system.
    X=Ax+ABpos*theCos;
    Y=Ay+ABpos*theSin;

    #  Success.
    return True,X,Y; 

def Intersect(line1,line2):
    A,B = line1
    C,D = line2
    flag,x,y = SegmentIntersect(
        A[0],A[1],
        B[0],B[1],
        C[0],C[1],
        D[0],D[1])
    E = [x,y]
    return flag,E
