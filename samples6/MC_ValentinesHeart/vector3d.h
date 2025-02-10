#ifndef _VECTOR3D_H
#define _VECTOR3D_H

typedef struct Vector3D_ { // 3D space vector
	float x;
	float y;
	float z;
} Vector3D;

Vector3D VectorAdd(Vector3D v0, Vector3D v1);
Vector3D VectorSubtract(Vector3D v0, Vector3D v1);
Vector3D VectorScalarMult(Vector3D v0, float scalar);
Vector3D VectorNormalize(Vector3D v);
float  VectorMagnitude(Vector3D v);

#endif
