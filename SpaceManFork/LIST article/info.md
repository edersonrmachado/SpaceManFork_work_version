

### ANOTAÇOES

EIRP refers to the Equivalent Isotropically Radiated Power, which is the radiated output591
power referenced to an isotropic antenna radiating power equally in all directions and whose592
gain is expressed in dBi. [fonte:file:///home/vnr/Downloads/rp002-1-0-4-regional-parameters.pdf ]

### Lora settings

![alt text](image.png)

PHYPayload

$$
PHYPayload = MHDR + MPayload + MIC    
$$
M = MPayload  
MIC = Message Integrity Code (4 octets)  
MHDR = MAC header (1 octet)  


$$
PHYPayload = 1 + MPayload + 4   
$$
![alt text](image-7.png)


## 1.  EU868-870

Escolhida 868.3 MHz

### Frequency

![alt text](image-1.png)
### DRs
![alt text](image-2.png)

### Power 
![alt text](image-4.png)

### Duty cycle
The current LoRaWAN specification exclusively uses duty-cycled limited554
transmissions to comply with the ETSI regulations.

![alt text](image-6.png)
## Payload size

- REPEATER allowed  

  ![alt text](image-5.png)


## 2. EU433
### Frequency e Duty Cycle
![alt text](image-9.png)

### DRs  and Power
![alt text](image-8.png)
![alt text](image-12.png)

### PAYLOAD SIZE
 - REPEATER ALLOWED     
![alt text](image-13.png)

### 3. AU915-928 MHz

### Frequency
To use central freq: 

ch 31 921.4 MHz or ch32 921.6 MHz   
![alt text](image-14.png)

### DR and Power

EIRP MAX = 30dBm
![alt text](image-15.png)

![alt text](image-16.png)


### Duty cycle ????


### PAYLOAD MAX

- REPEATER ALLOWED 

![alt text](image-17.png)


## 4. CN470-510 MHz

The transmission time shall1100
not exceed one second and is limited to one channel at a time. For interference mitigation, 
access to the physical medium requires a Listen Before Talk (LBT) with Adaptive Frequency
Agility (AFA) transmission management or other similar mechanisms like channels


** ONLY TX time up to 1s**  

ver questao do dwell time de outros 

## 5.  US902 -928 (US915)

### Frequency 
![alt text](image-18.png)

f(31)=908.5 MHz  
f(32)=908.7 MHz  

## POWER E DR 

![alt text](image-19.png)

![alt text](image-20.png)

![alt text](image-21.png)

![alt text](image-22.png)

# PAYLOAD 

- REPEATER ALLOWED  
![alt text](image-23.png)

# DUTY CYCLE ==? 400ms para FHSS mas nao diz nada pra o lora


## 6 AS923

### Freequency 
![alt text](image-24.png)


### DR e power

![alt text](image-25.png)

![alt text](image-26.png)

### PAYLOAD 

![alt text](image-27.png)