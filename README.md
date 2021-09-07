========================================================================

# BioSensor-Grouplevel-Emotion-Recognition

========================================================================

| author | mizukiyuta | <br />   
| department | Tokyo Metropolitan University System Design |  <br />

========================================================================

## Introduction 
Use bioSensors for group-level emotion recognition 

## Used device
### [Beacon]
for detecting people in the same room<br />  

### [Brainwave Mobile 2]
brain wave(EEG)->Attention,Mediation<br />  
 
### [Polar H10]
heart rate(LF/HF),Accelerometer<br />  

### [Sensor]
BME280 sensor based on raspberry pi4,to get environment data(temperature,humidity,pressure)<br />  

### [VR device]
for emotion Arousal<br />
oculus quest2
 
## Code
[polar H10]use python‘s bleak library to detect polar h10，get its Mac address,and record ECG or Accelerometer.<br />  

[PI_SENSOR]BME280 sensor based on raspberry pi4,to get environment data(temperature,humidity,pressure).<br />  

