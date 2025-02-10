#include <iostream>
using namespace std;

#include <math.h>
#include "vector3d.h"
#include "Create_OBJ_File_MC.h"

#pragma warning (disable : 4996)

int DLOW = -800;
int DHI  =  800;
int DN   = 4.0; //4.0 EDIT
int DN_2 = 4.0; //4.0 EDIT

float Phi3D(Vector3D pt);
int main();


// Implicit Function loaded or defined here
float Phi3D(Vector3D pt)// EDIT
{
	// range from 200 to -200
	float x, y, z;
	float a, b, c;
	float F;
	x = pt.x; y = pt.y; z = pt.z; 

	x = x/250.0; y = y/250.0; z = z/250.0;

	//F = 2*x*x + y*y + 8*z*z - 20;
	F = pow(pow(x,2)+(9/4)*pow(y,2)+pow(z,2)-1,3)
		-pow(x,2)*pow(z,3)-(9/200)*pow(y,2)*pow(z,3);

	F = pow(2*pow(x,2) + pow(y,2) + pow(z,2) - 1,3) -
	(1/10) * pow(x,2) * pow(x,3) - pow(y,2) * pow(z,3);


	//a = sqrt(x*x + y*y);
	//F = z - (a+3*cos(a)+5);


	//a = 4*x*x+1.5*y*y+z*z-1;
	//b = -1/10.0*x*x*z*z*z;
	//c = -y*y*z*z*z;
	//return -(a*a*a+b+c); // -f(x) has outward normals, f(x) has inward.

	//float F = y*y - (x*x*x - z*z*x);

	//float F = 1.0 - (x*x + y*y + z*z);

	return -F;

}

int main()
{
	MC_Create_OBJ_File("koblitz.obj", "koblitz",
		"koblitz.mtl","koblitz",DN_2, 0.0);

	//system("PAUSE");
	return 0;
}
