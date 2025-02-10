#include "vector3d.h"
#include <math.h>

// Magnitude or Length of vector v
float VectorMagnitude(Vector3D v)
{
	float magn = 0;
	magn = sqrt( v.x*v.x + v.y*v.y + v.z*v.z);
	return magn;
}

// Unit vector in the v direction
Vector3D VectorNormalize(Vector3D v)
{
	float length = VectorMagnitude(v);
	if (length == 0) return v;

	return VectorScalarMult( v, 1.0/length);

}

// Vector Space. Add, Subtract, Scalar Mult., Zero Vector.
Vector3D VectorAdd(Vector3D v0, Vector3D v1)
{
	Vector3D v;
	v.x = v0.x + v1.x;
	v.y = v0.y + v1.y;
	v.z = v0.z + v1.z;
	return v;
}
Vector3D VectorSubtract(Vector3D v0, Vector3D v1)
{
	Vector3D v;
	v.x = v0.x - v1.x;
	v.y = v0.y - v1.y;
	v.z = v0.z - v1.z;
	return v;
}
Vector3D VectorScalarMult(Vector3D v0, float scalar)
{
	Vector3D v;
	v.x = v0.x*scalar;
	v.y = v0.y*scalar;
	v.z = v0.z*scalar;
	return v;
}

