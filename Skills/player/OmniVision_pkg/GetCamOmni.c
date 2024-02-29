//=============================================================================
// Copyright (c) 2001-2022 FLIR Systems, Inc. All Rights Reserved.
//
// This software is the confidential and proprietary information of FLIR
// Integrated Imaging Solutions, Inc. ("Confidential Information"). You
// shall not disclose such Confidential Information and shall use it only in
// accordance with the terms of the license agreement you entered into
// with FLIR Integrated Imaging Solutions, Inc. (FLIR).
//
// FLIR MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE SUITABILITY OF THE
// SOFTWARE, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE
// IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
// PURPOSE, OR NON-INFRINGEMENT. FLIR SHALL NOT BE LIABLE FOR ANY DAMAGES
// SUFFERED BY LICENSEE AS A RESULT OF USING, MODIFYING OR DISTRIBUTING
// THIS SOFTWARE OR ITS DERIVATIVES.
//=============================================================================

/**
 *  @example Acquisition_C.c
 *
 *  @brief Acquisition_C.c shows how to acquire images. It relies on
 *  information provided in the Enumeration_C example. Following this, check
 *  out the NodeMapInfo_C example if you haven't already. It explores
 *  retrieving information from various node types.
 *
 *  This example touches on the preparation and cleanup of a camera just
 *  before and just after the acquisition of images. Image retrieval and
 *  conversion, grabbing image data, and saving images are all covered.
 *
 *  Once comfortable with Acquisition_C and NodeMapInfo_C, we suggest checking
 *  out AcquisitionMultipleCamera_C, NodeMapCallback_C, or SaveToAvi_C.
 *  AcquisitionMultipleCamera_C demonstrates simultaneously acquiring images
 *  from a number of cameras, NodeMapCallback_C acts as a good introduction to
 *  programming with callbacks and events, and SaveToAvi_C exhibits video
 *  creation.
 *
 *  *** NOTE ***
 *  When using Visual Studio 2010, our solution will use the /TP flag to
 *  compile this example as C++ code instead of C code. This is because our C
 *  examples adhere to post-C89 standard which is not supported in Visual
 *  Studio 2010. You can still use our 2010 libraries to write your own C
 *  application as long as it follows the Visual Studio 2010 C compiler
 *  standard.
 *
 */
//gcc -I../../include/spinc -I/opt/spinnaker/include/spinc -Wall -D LINUX -c Acquisition_C.c -o .obj/build/Acquisition_C.o
//gcc -o GetCamOmni .obj/build/GetCamOmni.o -Wl,-Bdynamic -L/opt/spinnaker/lib -lSpinnaker -lSpinnaker_C  -Wl,-rpath-link=../../lib


#include "GetCamOmni.h"

spinCamera hCam = NULL;
spinImageProcessor hImageProcessor = NULL;
spinImage outImage = NULL;
void ** data = NULL;
void indent(unsigned int level)
{
    unsigned int i = 0;

    for (i = 0; i < level; i++)
    {
        printf("   ");
    }
}

// This function retrieves and prints the display name and value of an integer
// node.
spinError printIntegerNode(spinNodeHandle hNode, unsigned int level)
{
    spinError err = SPINNAKER_ERR_SUCCESS;

    // Retrieve display name
    char displayName[MAX_BUFF_LEN];
    size_t displayNameLength = MAX_BUFF_LEN;

    err = spinNodeGetDisplayName(hNode, displayName, &displayNameLength);
    if (err != SPINNAKER_ERR_SUCCESS)
    {
        return err;
    }

    //
    // Retrieve integer node value
    //
    // *** NOTES ***
    // Keep in mind that the data type of an integer node value is an
    // int64_t as opposed to a standard int. While it is true that the two
    // are often interchangeable, it is recommended to use the int64_t
    // to avoid the introduction of bugs into software built with the
    // Spinnaker SDK.
    //
    int64_t integerValue = 0;

    err = spinIntegerGetValue(hNode, &integerValue);
    if (err != SPINNAKER_ERR_SUCCESS)
    {
        return err;
    }

    // Print value
    indent(level);
    printf("%s: %d\n", displayName, (int)integerValue);

    return err;
}

spinError printEnumerationNodeAndCurrentEntry(spinNodeHandle hEnumerationNode, unsigned int level)
{
    spinError err = SPINNAKER_ERR_SUCCESS;

    // Retrieve display name
    char displayName[MAX_BUFF_LEN];
    size_t displayNameLength = MAX_BUFF_LEN;

    err = spinNodeGetDisplayName(hEnumerationNode, displayName, &displayNameLength);
    if (err != SPINNAKER_ERR_SUCCESS)
    {
        return err;
    }

    //
    // Retrieve current entry node
    //
    // *** NOTES ***
    // Returning the current entry of an enumeration node delivers the entry
    // node rather than the integer value or symbolic. The current entry's
    // integer and symbolic need to be retrieved from the entry node because
    // they cannot be directly accessed through the enumeration node in C.
    //
    spinNodeHandle hCurrentEntryNode = NULL;

    err = spinEnumerationGetCurrentEntry(hEnumerationNode, &hCurrentEntryNode);
    if (err != SPINNAKER_ERR_SUCCESS)
    {
        return err;
    }

    //
    // Retrieve current symbolic
    //
    // *** NOTES ***
    // Rather than retrieving the current entry node and then retrieving its
    // symbolic, this could have been taken care of in one step by using the
    // enumeration node's ToString() method.
    //
    char currentEntrySymbolic[MAX_BUFF_LEN];
    size_t currentEntrySymbolicLength = MAX_BUFF_LEN;

    err = spinEnumerationEntryGetSymbolic(hCurrentEntryNode, currentEntrySymbolic, &currentEntrySymbolicLength);
    if (err != SPINNAKER_ERR_SUCCESS)
    {
        return err;
    }

    // Print current entry symbolic
    indent(level);
    printf("%s: %s\n", displayName, currentEntrySymbolic);

    return err;
}

bool8_t IsAvailableAndReadable(spinNodeHandle hNode, char nodeName[])
{
    bool8_t pbAvailable = False;
    spinError err = SPINNAKER_ERR_SUCCESS;
    err = spinNodeIsAvailable(hNode, &pbAvailable);
    if (err != SPINNAKER_ERR_SUCCESS)
    {
        printf("Unable to retrieve node availability (%s node), with error %d...\n\n", nodeName, err);
    }

    bool8_t pbReadable = False;
    err = spinNodeIsReadable(hNode, &pbReadable);
    if (err != SPINNAKER_ERR_SUCCESS)
    {
        printf("Unable to retrieve node readability (%s node), with error %d...\n\n", nodeName, err);
    }
    return pbReadable && pbAvailable;
}

void PrintRetrieveNodeFailure(char node[], char name[])
{
    printf("Unable to get %s (%s %s retrieval failed).\n\n", node, name, node);
}
// This function Open the Camera

int CamOmni_Open(int exposure,int gain,int saturation ) {
    //printf("Openning!\n");
     // Retrieve list of cameras from the system
    //spinError errReturn = SPINNAKER_ERR_SUCCESS;
    spinError err = SPINNAKER_ERR_SUCCESS;
   
    //char lastErrorMessage[MAX_BUFF_LEN];
    //size_t lenLastErrorMessage = MAX_BUFF_LEN;
    spinCameraList hCameraList = NULL;

    // Retrieve singleton reference to system object
    spinSystem hSystem = NULL;

    // Maps and Nodes Hanfdlers
    spinNodeMapHandle hNodeMapTLDevice = NULL;
    spinNodeMapHandle hNodeMap = NULL;
    spinNodeMapHandle hNodeStreamMap = NULL;
    spinNodeHandle hAcquisitionMode = NULL;
    spinNodeHandle hAcquisitionModeContinuous = NULL;
    spinNodeHandle hAcquisitionBufferCount = NULL;
    spinNodeHandle hDeviceSerialNumber = NULL;
    
    int64_t acquisitionModeContinuous = 0;
    size_t pvalue;
    char deviceSerialNumber[MAX_BUFF_LEN];
    size_t lenDeviceSerialNumber = MAX_BUFF_LEN;

    err = spinSystemGetInstance(&hSystem);
    if (err != SPINNAKER_ERR_SUCCESS)
    {
        //spinErrorGetLastMessage(lastErrorMessage, &lenLastErrorMessage);
        //printf("Error: %s [%d]\n\n", lastErrorMessage, err);
        return 0;
        //return err;
    }

    // Print out current library version
    spinLibraryVersion hLibraryVersion;

    spinSystemGetLibraryVersion(hSystem, &hLibraryVersion);
    /*printf(
        "Spinnaker library version: %d.%d.%d.%d\n\n",
        hLibraryVersion.major,
        hLibraryVersion.minor,
        hLibraryVersion.type,
        hLibraryVersion.build);
    */
    // Retrieve list of cameras from the system


    err = spinCameraListCreateEmpty(&hCameraList);
    if (err != SPINNAKER_ERR_SUCCESS)
    {
        //spinErrorGetLastMessage(lastErrorMessage, &lenLastErrorMessage);
        //printf("Error: %s [%d]\n\n", lastErrorMessage, err);
        //return err;
        return 0;
    }

    err = spinSystemGetCameras(hSystem, hCameraList);
    if (err != SPINNAKER_ERR_SUCCESS)
    {
        //spinErrorGetLastMessage(lastErrorMessage, &lenLastErrorMessage);
        //printf("Error: %s [%d]\n\n", lastErrorMessage, err);
        //return err;
        return 0;
    }

    // Retrieve number of cameras
    size_t numCameras = 0;

    err = spinCameraListGetSize(hCameraList, &numCameras);
    if (err != SPINNAKER_ERR_SUCCESS)
    {
        //spinErrorGetLastMessage(lastErrorMessage, &lenLastErrorMessage);
        //printf("Error: %s [%d]\n\n", lastErrorMessage, err);
        //return err;
        return 0;
    }

    //printf("Number of cameras detected: %u\n\n", (unsigned int)numCameras);
    
    // Finish if there are no cameras
    if (numCameras == 0)
    {
        // Clear and destroy camera list before releasing system
        err = spinCameraListClear(hCameraList);
        if (err != SPINNAKER_ERR_SUCCESS)
        {
            //spinErrorGetLastMessage(lastErrorMessage, &lenLastErrorMessage);
            //printf("Error: %s [%d]\n\n", lastErrorMessage, err);
            //return err;
            return 0;
        }

        err = spinCameraListDestroy(hCameraList);
        if (err != SPINNAKER_ERR_SUCCESS)
        {
            //spinErrorGetLastMessage(lastErrorMessage, &lenLastErrorMessage);
            //printf("Error: %s [%d]\n\n", lastErrorMessage, err);
            //return err;
            return 0;
        }

        // Release system
        err = spinSystemReleaseInstance(hSystem);
        if (err != SPINNAKER_ERR_SUCCESS)
        {
            //spinErrorGetLastMessage(lastErrorMessage, &lenLastErrorMessage);
            //printf("Error: %s [%d]\n\n", lastErrorMessage, err);
            //return err;
            return 0;
        }

        //printf("Not enough cameras!\n");
       
        
    }
    //Get Camera 0
    err = spinCameraListGet(hCameraList, 0, &hCam);
    
   
    err += spinCameraGetTLDeviceNodeMap(hCam, &hNodeMapTLDevice);
     if (err != SPINNAKER_ERR_SUCCESS)
        {
            //spinErrorGetLastMessage(lastErrorMessage, &lenLastErrorMessage);
            //printf("Error: %s [%d]\n\n", lastErrorMessage, err);
             return 0;
        }

     err= spinCameraGetTLStreamNodeMap(hCam,&hNodeStreamMap);
    if (err != SPINNAKER_ERR_SUCCESS)
        {
            //spinErrorGetLastMessage(lastErrorMessage, &lenLastErrorMessage);
            //printf("Error: %s [%d]\n\n", lastErrorMessage, err);
             return 0;
        }
    spinNodeMapGetNode(hNodeStreamMap, "StreamBufferCountManual", &hAcquisitionBufferCount);
    //printIntegerNode(hAcquisitionBufferCount, 1);
    spinIntegerSetValueEx(hAcquisitionBufferCount, 0, 3);
    //printIntegerNode(hAcquisitionBufferCount, 1);
    
    err = spinCameraInit(hCam);
     if (err != SPINNAKER_ERR_SUCCESS)
        {
            //spinErrorGetLastMessage(lastErrorMessage, &lenLastErrorMessage);
            //printf("Error: %s [%d]\n\n", lastErrorMessage, err);
             return 0;
        }
    spinNodeHandle hExposureTime = NULL;
    spinNodeHandle hSaturation = NULL;
    spinNodeHandle hGain = NULL;
    spinCameraGetNodeMap(hCam, &hNodeMap);
    err = spinCameraBeginAcquisition(hCam);
    spinNodeMapGetNode(hNodeMap, "AcquisitionMode", &hAcquisitionMode);
    err = spinNodeMapGetNode(hNodeMap, "ExposureTime", &hExposureTime);
    err = spinFloatSetValue(hExposureTime, exposure/10);
    err = spinNodeMapGetNode(hNodeMap, "Saturation", &hSaturation);
    err = spinFloatSetValue(hSaturation,saturation/10);
    err = spinNodeMapGetNode(hNodeMap, "Gain", &hGain);
    err = spinFloatSetValue(hGain, gain/10);
    spinNodeMapGetNumNodes(hNodeMap,&pvalue);
    if (err != SPINNAKER_ERR_SUCCESS)
        {
            //spinErrorGetLastMessage(lastErrorMessage, &lenLastErrorMessage);
            //printf("Error: %s [%d]\n\n", lastErrorMessage, err);
            return 0;
        }


    

    err += spinEnumerationGetEntryByName(hAcquisitionMode, "Continuous", &hAcquisitionModeContinuous);
    err += spinEnumerationEntryGetIntValue(hAcquisitionModeContinuous, &acquisitionModeContinuous);
    err += spinEnumerationSetIntValue(hAcquisitionMode, acquisitionModeContinuous);
    err += spinNodeMapGetNode(hNodeMapTLDevice, "DeviceSerialNumber", &hDeviceSerialNumber);
    err += spinStringGetValue(hDeviceSerialNumber, deviceSerialNumber, &lenDeviceSerialNumber);
    //spinImageProcessor hImageProcessor = NULL;
    err += spinImageProcessorCreate(&hImageProcessor);
    err += spinImageProcessorSetColorProcessing(hImageProcessor, SPINNAKER_COLOR_PROCESSING_ALGORITHM_HQ_LINEAR);
    //printf("Test3! %d %p %p \n",err, &hCam ,hImageProcessor);
  	
     err = spinImageCreateEmpty(&outImage);

    
    size_t imageSize;
    spinImageGetBufferSize(outImage, &imageSize);
    data = (void**)malloc(imageSize * sizeof(void*));
    return 1;
}
   
uint8_t* Get_Frame() {  
    spinImage hResultImage = NULL;
   
    //Wait for image buffer ready
    spinCameraGetNextImage(hCam, &hResultImage);
    // Convert Image from YUV to BGR  !!! Tentar ver se tiro isto
    spinImageProcessorConvert(hImageProcessor, hResultImage, outImage, PixelFormat_BGR8);
    // Get data from image
    spinImageGetData(outImage, data);
    // Release image
    spinImageRelease(hResultImage);
    // Return pointer
    return (uint8_t*)*data;
        
}
/*
int main(){
    spinError err = SPINNAKER_ERR_SUCCESS;
    printf("Init!\n");
uint8_t * datam;
    
 
     
    CamOmni_Open();
    printf("Openning!\n");
    printf("TestFinal! %d %p %p \n",err, &hCam ,&hImageProcessor);
    struct timeval stop, start;
    while(1){
    printf("Loop.\n");
    
    gettimeofday(&start, NULL);
    printf("Loop2.\n");
    
   datam=Get_Frame();
 // printf("Pointer GetF2! %p\n",data);
  //if()
//for(int j = 0; j < 3*480; j+=3){
       
      printf("Teste 1 %d  R:%u ",480, (datam[480]));
        printf("G:%u ", (datam[481]));
    printf("B:%u\n", (datam[482]));
 // }
 gettimeofday(&stop, NULL);
printf("took %lu us\n", (stop.tv_sec - start.tv_sec) * 1000000 + stop.tv_usec - start.tv_usec);
}
    //printf("Finnish\n");
    // Get_Frame(hCam,hImageProcessor, &outImage);
    size_t pSize = 0;
    err= spinImageGetBitsPerPixel(outImage,&pSize);
    if(err>0){
    printf("Finnish1\n %u", (unsigned int)pSize);
    for(int j = 0; j < 2440; ++j){
  //printf("%02x\n", ((uint8_t*) outImage)[j]);
  }
    while(1){}

    return 1;


}
*/
void soma(int a, int* b){
*b=a+*b;

}
