#include "MarchingCubes.h"
#include "Create_OBJ_File_MC.h"

#include <stdio.h>
#include <iostream>
using namespace std;
#include <list>

//#include <windows.h>

FILE *g_prefix, *g_suffix, *g_fp_x;
FILE *g_fp_v, *g_fp_f, *g_fp_n; // *g_fp
int g_v_n = 0;  // output vertex label number . Keeps track of number of vertices
int g_t_n = 0;  // output triangle label number. Keeps track of number of triangles.

list<Vector3D> g_vertices;
list<Vector3D> g_normals;
list<Face> g_faces;

extern int DLOW;
extern int DHI;
extern int DN;
extern int DN_2;

// Note that output using fprintf( ) writes float, iostream might write double,
// causing an error, in .X file. ?. fprintf( ) was used below originally which works

void MC_Create_OBJ_File(const char *filename,
const char *obj_name, const char *mat_filename,
const char *mat_name,float VoxelScaleSize, float Threshold)
{
        g_vertices.clear();
        g_normals.clear();
        g_faces.clear();

        ios::sync_with_stdio();

        FILE *fp = fopen(filename, "wb");

        MC_Initialize();
        MarchingCubes(DN_2, 0.0);

        bool verbose = true;

        if (verbose) cout << "Writing .obj file prefix..." << endl;
        CreatePrefix(fp);

        if (verbose) cout << "Writing vertex data..." << endl;
        fprintf(fp, "o %s\n", obj_name);
        fprintf(fp, "mtllib %s\n", mat_filename);
        while (!g_vertices.empty()) {
                Vector3D vv; vv = g_vertices.front(); g_vertices.pop_front()
;
                fprintf(fp, "v %f %f %f\n", vv.x, vv.y, vv.z);
                bool endlist = (g_vertices.empty());
        }

        if (verbose) cout << "Copying triangle face data..." << endl;
        list<Face> g_faces_copy;
        list<Face>::iterator fi;
        for (fi=g_faces.begin(); fi!=g_faces.end(); fi++) {
                g_faces_copy.push_back(*fi);
        }
        if (verbose) cout << "Writing triangle face data..." << endl;
        fprintf(fp,"usemtl %s\n", mat_name);
        while ( !g_faces.empty() ) {
                Face ff; ff = g_faces.front(); g_faces.pop_front();
                fprintf(fp, "f %d %d %d\n", ff.v1+1, ff.v2+1, ff.v3+1);
                bool endlist = (g_faces.empty());
        }

        if (verbose) cout << "Writing suffix..." << endl;
        CreateSuffix(fp);

        if (verbose) cout << "Closing .obj File..." << endl;

        fclose(fp);
}

void CreatePrefix(FILE *fp)
{
}

void CreateSuffix(FILE *fp)
{
}
