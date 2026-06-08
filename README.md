\# Battery Management System Simulation



\## Overview



This project is a Python-based Battery Management System (BMS) simulation that models battery discharge behavior under different load currents. The simulation includes electrical modeling, thermal modeling, protection logic, and hysteresis-based cooling control.



\## Features



\* Simulates battery discharge under multiple load current conditions

\* Tracks State of Charge (SOC)

\* Estimates Open-Circuit Voltage (OCV)

\* Models terminal voltage using internal resistance

\* Implements undervoltage, overcurrent, and overtemperature protection

\* Calculates heat generation from internal resistance using I²R losses

\* Estimates battery temperature rise using Q = mcΔT

\* Implements hysteresis-based cooling control

\* Visualizes voltage and temperature behavior over time



\## Key Equations



\### Terminal Voltage



V\_terminal = OCV - I × R\_internal



\### Power Loss from Internal Resistance



P\_loss = I² × R\_internal



\### Heat Energy



Q = P\_loss × t



\### Temperature Rise



ΔT = Q / (m × c)



\## Simulation Logic



The simulation updates battery behavior at each time step by:



1\. Estimating SOC based on load current and time

2\. Calculating OCV from SOC

3\. Applying internal resistance voltage drop

4\. Estimating heat generation from I²R losses

5\. Updating battery temperature using Q = mcΔT

6\. Applying cooling control when the battery exceeds the cooling threshold

7\. Triggering protection logic when safety limits are exceeded



\## Protection Logic



The simulation includes:



\* Undervoltage cutoff

\* Overcurrent cutoff

\* Overtemperature cutoff



\## Cooling Control



The cooling system uses hysteresis control:



\* Cooling turns ON when battery temperature reaches the upper threshold

\* Cooling turns OFF when battery temperature drops below the lower threshold



This prevents rapid ON/OFF switching near a single temperature threshold.



\## Technologies Used



\* Python

\* Matplotlib



\## How to Run



```bash

python battery_sim.py

```



\## What I Learned



Through this project, I learned how load current affects battery runtime, terminal voltage, efficiency, and temperature. Higher load currents increase internal resistance losses, reduce terminal voltage, accelerate discharge, and generate more heat. I also learned how thermal modeling and cooling control can be integrated into a simplified BMS simulation.



