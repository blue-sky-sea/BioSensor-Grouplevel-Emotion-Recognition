
========================================================================

# BioSensor-Grouplevel-Emotion-Recognition

========================================================================

![image](https://user-images.githubusercontent.com/26008298/132282618-0440b99c-af47-4e75-9c45-2253ba94f59d.png)

========================================================================

| author | mizukiyuta | <br />   
| department | Tokyo Metropolitan University System Design |  <br />

========================================================================

<img src="https://user-images.githubusercontent.com/26008298/132282518-24095b5c-eae4-4fde-ab66-089d8a446ec4.png" width="180">

## Introduction 
Use bioSensors for group-level emotion recognition <br />

## Used device
### [Beacon]
for detecting people in the same room <br />  
<img src="https://user-images.githubusercontent.com/26008298/132282742-d21cea84-a607-4038-b9f2-69ddf8d408b0.png" width="160">

### [Muse Mind Monitor]
brain wave(EEG)->Attention,Mediation <br />  
<img src="https://user-images.githubusercontent.com/26008298/132282807-9775c223-0d4b-48eb-9d75-a308ffea37d1.png" width="160">
### [Polar H10]
heart rate(LF/HF),Accelerometer <br />  
<img src="https://user-images.githubusercontent.com/26008298/132282872-a2a6b140-0707-4bd1-9bda-5e4b4e778d64.png" width="150">

### [Sensor]
BME280 sensor based on raspberry pi4,to get environment data(temperature,humidity,pressure) <br />
<img src="https://user-images.githubusercontent.com/26008298/132282977-fd54ee04-b335-455b-bf5e-32b5e313fb84.png" width="170">
![image](https://user-images.githubusercontent.com/26008298/132282884-ba2faa0c-b897-4cab-b360-0220d821504e.png)

### [VR device]
for emotion Arousal <br />
oculus quest2 <br />
<img src="https://user-images.githubusercontent.com/26008298/132283403-9d1f2ed8-8238-4ca3-aedc-af52e3fc1ef1.png" width="160">

## Code
[polar H10]use python‘s bleak library to detect polar h10，get its Mac address,and record ECG or Accelerometer. <br />  

[PI_SENSOR]BME280 sensor based on raspberry pi4,to get environment data(temperature,humidity,pressure). <br />  

[ECG_EEG_PROCESS]EEG and ECG data process program. ECG->lfhf,pnn50... EEG->Attention,Meditation...<br />
process to 60s data,one second one row<br /> 
