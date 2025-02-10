#ifndef _CREATE_OBJ_FILE_MC_H
#define _CREATE_OBJ_FILE_MC_H

#include <stdio.h>
#include <iostream>
using namespace std;
#include <fstream>

void CreatePrefix(FILE *fp);
void CreateSuffix(FILE *fp);

void MC_Create_OBJ_File(const char *filename,
    const char *obj_name, const char *mat_filename,
    const char *mat_name,
    float VoxelScaleSize, float Threshold);


#endif
