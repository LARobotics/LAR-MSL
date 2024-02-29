#ifndef _GetCamOmni_H
#define _GetCamOmni_H

#include "SpinnakerC.h"
//#include "/opt/spinnaker/include/spinc/SpinnakerC.h"
#include "stdio.h"
#include "string.h"
#include <sys/time.h>
#include <stdlib.h>



//#include "SpinnakerC.h"
//#include "/opt/spinnaker/include/spinc/SpinnakerC.h"
//#include "stdio.h"
//#include "string.h"
//#include <sys/time.h>


// This macro helps with C-strings.
#define MAX_BUFF_LEN 256
int CamOmni_Open(int exposure,int gain,int saturation);
uint8_t* Get_Frame();
void soma(int a, int* b);





#endif
