========================================================================

# BioSensor-Grouplevel-Emotion-Recognition

========================================================================

<font color="red"> author: <font color="red">mizukiyuta <br />   
<font color="blue">department: <font color="red"> tokyo metropolitan university system design

========================================================================

## Introduction 
Use bioSensors for group-level emotion recognition 

## Used device
### [Beacon]for detect people in the same room<br />  

[Brainwave Mobile]brain wave(EEG),heart rate(HRV)<br />  
 
[Polar H10]heart rate(LF/HF),Accelerometer<br />  

[sensor]BME280 sensor based on raspberry pi4,to get environment data(temperature,humidity,pressure)<br />  

#[Fitbit]heart beat,skin response(GSR),Respiration Rate Analysis (RR),Skin Temperature Measurements (SKT),Electromyogram(EMG)<br />  

[VR device]for emotion Arousal<br />
google 3D glasses or other VR device(quest2)
 
## Code
[polar H10]use python‘s bleak library to detect polar h10，get its Mac address,and record ECG or Accelerometer.<br />  

[PI_SENSOR]BME280 sensor based on raspberry pi4,to get environment data(temperature,humidity,pressure).<br />  

