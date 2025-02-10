#ifndef _MARCHING_CUBES_H
#define _MARCHING_CUBES_H


#include "vector3d.h"

// Voxel = Cube = G = (V,E)
#define V_CARD 8                                // v = 0 to 8-1. V_CARD is the cardinality of V
#define E_CARD 12
#define VSS_CARD 256    // 2^8 which is the cardinality of VSS
#define ESS_CARD 4096   // 2^12

#define SET_MEMBER(element, set)    ( (set) & (1 << (element)) )
// Row-Major Ordering index / label for matrix[n1][n2] and matrix[n1][n2][n3]
#define IDX2(n1, n2, i1, i2) ((i2) + n2*(i1))
#define IDX3(n1, n2, n3, i1, i2, i3) ( (i3) + (n3)*((i2) + n2*(i1)) )

typedef unsigned char       BYTE;
typedef unsigned short      WORD;
typedef BYTE VertexSubset;              // vSS = 0 to 2^8-1. Subset of Vertices
typedef WORD EdgeSubset;                // eSS = 0 to 2^12-1. Subset of Edges
typedef int VertexLabel;
typedef int EdgeLabel;

typedef struct Face_ {
        int v1;
        int v2;
        int v3;
} Face;

typedef struct Vertex_ {  // point
        float x;                // Vertex xyz position
        float y;
        float z;
        int n;                  // Vertex Label
} Vertex;
typedef struct Edge_ {   // line
        VertexLabel v0;         // edge v0v1
        VertexLabel v1;
        int n;                  // edge label
} Edge;
typedef struct Graph_ {  // drawing of points and lines
        Vertex v[V_CARD];       // V(G) = vertices
        Edge   e[E_CARD];       // E(G) = edges
} Graph;

//EdgeSubset Map_VertexSubset_To_EdgeSubset[VSS_CARD]; // defined at bottom
//VertexLabel Map_VertexSubset_To_TriangleList[VSS_CARD*(3*5+1)];

Vector3D VertexToVector3D(Vertex v);
float fLinearInterpolation(float Phi0, float Phi1, float Threshold);
Vector3D vLinearInterpolation(Vector3D v0, Vector3D v1, float Threshold);

Vector3D Gradient(Vector3D position, float epsilon);
Vector3D VertexPointNormal(Vector3D pt);
void MarchingCubes_Voxel(Vector3D PixelOrigin, float VoxelScaleSize, float Threshold);
VertexSubset VertexSubsetAddElement(VertexSubset set, VertexLabel element);
EdgeSubset EdgeSubsetAddElement(EdgeSubset set, EdgeLabel element);
VertexSubset VertexSubsetRemoveElement(VertexSubset set, VertexLabel element
);
EdgeSubset EdgeSubsetRemoveElement(EdgeSubset set, EdgeLabel element);
void MarchingCubes(float VoxelScaleSize, float Threshold);
float Phi(float x, float y, float z); // Implicit Function F(x,y,z) = Phi(x,y,z) - Threshold = 0.
void MC_Initialize();

extern float Phi3D(Vector3D pt);

#endif
