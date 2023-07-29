# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 01:32:17 2023

@author: KUMAR RAHUL
"""


import matplotlib.pyplot as plt
import csv
import numpy as np
import nidaqmx
from nidaqmx.constants import AcquisitionType, Edge
import pandas as pd

def moving_average(data, window_size):
    """
    Apply a simple moving average filter to the input data.

    Args:
        data (list): Input data as a list or array.
        window_size (int): Size of the moving average window.

    Returns:
        list: Filtered data as a list.
    """
    filtered_data = []
    window = []
    window_sum = 0

    for i in range(len(data)):
        window.append(data[i])
        window_sum += data[i]

        if i >= window_size:
            window_sum -= window.pop(0)

        if i >= window_size - 1:
            filtered_data.append(window_sum / window_size)

    return filtered_data


# Constants
sampling_rate = 10000  # Sample rate in samples per second
duration = 1.0  # Duration of the acquisition in seconds
samples = int (sampling_rate * duration)  # Total number of samples

# Create an array of time values
time = np.linspace(0, duration, samples)

# Initialize the NI 6361 device and the analog input channel
with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0")  # Replace "Dev1/ai0" with your specific channel name
    task.timing.cfg_samp_clk_timing(sampling_rate, samps_per_chan=samples)

    # Read the voltage values from the photodiode
    data = task.read(samples, timeout=10.0)
    window_size = 3
    filtered_data = moving_average(data, window_size)
    
    peak_time = np.argmax(data)
    
    df = pd.DataFrame({"time": time, "data": data, "filtered_data": filtered_data, "peak_time": peak_time})

    # Define the CSV file path
    csv_file = "test.csv"

    df.to_csv(csv_file, index=False)

    # Write the data to the CSV file
    with open(csv_file, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(data)    

# Plot the waveform
plt.plot(time, filtered_data)
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.title('Interfacing of Two Laser Beams')
plt.grid(True)
plt.show()
