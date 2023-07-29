# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 00:20:13 2023

@author: KUMAR RAHUL
"""

import matplotlib.pyplot as plt
import numpy as np
import nidaqmx
from nidaqmx.constants import AcquisitionType

# Configure acquisition parameters
sample_rate = 10000  # Sample rate in samples per second
duration = 1# Duration of acquisition in seconds
num_samples = int(sample_rate * duration)

# Create task for data acquisition
with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0")  # Configure analog input channel for photodiode 1
    task.ai_channels.add_ai_voltage_chan("Dev1/ai1")  # Configure analog input channel for photodiode 2
    task.timing.cfg_samp_clk_timing(sample_rate, sample_mode=AcquisitionType.CONTINUOUS)

    # Read data from the analog input channels
    data = task.read(number_of_samples_per_channel=num_samples)
    np.array(data)
    data=np.array(data)
print(data.shape)
# Split the acquired data into photodiode 1 and photodiode 2 outputs
laser1_output = data[0,:]  # Output of photodiode 1
laser2_output = data[1,:]  # Output of photodiode 2


# Time array
time = np.arange(num_samples) / sample_rate

# Find the time delay between the two output curves
cross_correlation = np.correlate(laser1_output, laser2_output, mode='same')
time_delay = time[np.argmax(cross_correlation)]

# Plotting the output curves and time delay
plt.figure(figsize=(12, 12))
print(time.shape)
print(laser1_output)
plt.plot(time, laser1_output, label='Photodiode 1')
plt.plot(time, laser2_output, label='Photodiode 2')
plt.xlabel('Time (10^-4)')
plt.ylabel('Output')
plt.title('Output Curves of Photodiodes')
plt.legend()

plt.text(0.1, 0.9, f'Time delay: {time_delay:.2f} *10^-4s', transform=plt.gca().transAxes)
plt.show()
