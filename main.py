#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 17:37:10 2026
BUAI 433 Project: Ice Cream Simulation
@author: Emi Hutter-DeMarco, Caroline Kilbane, Jerry Cai
"""
import numpy as np
import matplotlib.pyplot as plt

""" Expected Daily Demand Parameters """
lambda_m = 5.0   # Morning expected demand (rate * hour: 1 * 5 = 5)
lambda_a = 105.0 # Afternoon expected demand (rate * hour: 17.5 * 6 = 105)
lambda_e = 10.0  # Evening expected demand (rate * hour: 1 * 10 = 10)


"""
Generates demands using Poisson distribution for the three daily periods. 
This creates arrays (lists) of demands for each day.
"""
def demands(num_days):
    # Generates random demand values for the number of days where the average
    # demand is lambda (i.e. if there are 4 days, then a possible Dm = [12, 5, 11, 9])
    Dm = np.random.poisson(lambda_m, num_days) # Stores morning demands for each day
    Da = np.random.poisson(lambda_a, num_days) # Stores afternoon demands for each day
    De = np.random.poisson(lambda_e, num_days) # Stores evening demands for each day
    # Looked up numpy poission functions in documentation
    return Dm, Da, De


"""
Loops through the arrays of daily demands and applies method
to calculate the profit for each simulated day.
"""
def calculate_profits(Q, Dm_array, Da_array, De_array):
    # Make profits an array since we are calculating one profit value for every day
    profits = []
    # Chose Dm array, but realistically could choose any of the three as they all have the same length
    num_days = len(Dm_array)
    
    for i in range(num_days):
        # Extract the demand for day 'i' from our arrays
        Dm = Dm_array[i]
        Da = Da_array[i]
        De = De_array[i]
        
        # pi represents net profit
        if Dm >= Q: # Sell out before noon
            pi = (2.00 * Q) - (1.00 * Q)
        elif Q <= (Dm + Da): # Sell out in afternoon 
            pi = (2.00 * Dm) + 1.50 * (Q - Dm) - (1.00 * Q)
        elif Q <= (Dm + Da + De): # Sell out in evening
            pi = (2.00 * Dm) + (1.50 * Da) + 1.00 * (Q - Dm - Da) - (1.00 * Q)
        else: # Leftovers at end of day
            leftovers = Q - Dm - Da - De
            pi = (2.00 * Dm) + (1.50 * Da) + (1.00 * De) + (0.50 * leftovers) - (1.00 * Q)
            
        profits.append(pi) # Adds net profit to each day in the profits array 
        
    return np.array(profits)


""" \n ------- Question 1 -------"""
Dm1, Da1, De1 = demands(5000)
profits1 = calculate_profits(75, Dm1, Da1, De1)

print("------- Question 1 Statistics -------")
print("Mean Profit:", round(np.mean(profits1), 2))
print("Standard Deviation:", round(np.std(profits1, ddof=1), 2))
print("Minimum Profit:", round(np.min(profits1),2))
print("Maximum Profit:", round(np.max(profits1),2))

plt.figure(figsize=(8, 6))
plt.hist(profits1, bins=15,color='steelblue', edgecolor='black')
plt.xlabel('Profit ($)')
plt.ylabel('Frequency')
plt.title('Daily Profit Distribution (Q = 75)')
plt.show()



""" ------- Question 2 -------"""
periodmean = []

# Simulates 5000 91-day periods 
for i in range(5000):
    Dm2, Da2, De2 = demands(91)
    profits2 = calculate_profits(75, Dm2, Da2, De2)
    periodmean.append(np.mean(profits2))
    
periodmean = np.array(periodmean)

print("\n ------- Question 2 Statistics -------")
print("Mean of Period Means:", round(np.mean(periodmean), 2))
print("Standard Deviation of Period Means:", round(np.std(periodmean, ddof=1), 2))
print("Minimum Period Mean:", round(np.min(periodmean), 2))
print("Maximum Period Mean:", round(np.max(periodmean), 2))

plt.figure(figsize=(8, 6))
plt.hist(periodmean, bins=15,color='steelblue', edgecolor='black')
plt.xlabel('91-Day Mean Daily Profit ($)')
plt.ylabel('Frequency')
plt.title('Distribution of Mean Daily Profit for 5,000 91-Day Periods')
plt.show()


""" ------- Question 3 -------"""
# Draw a 91-day sample 
Dm_sample, Da_sample, De_sample = demands(91)
sample_profits = calculate_profits(75, Dm_sample, Da_sample, De_sample)

# Calculate the required sample stats
sample_mean = np.mean(sample_profits)
sample_std = np.std(sample_profits, ddof=1)
standard_error = sample_std / np.sqrt(91)

# Calculate 95% Confidence Interval boundaries
ci_lower = sample_mean - 1.96 * standard_error
ci_upper = sample_mean + 1.96 * standard_error

# Simulate a 10-Year period (3,650 days)
Dm3, Da3, De3 = demands(3650)
profits3 = calculate_profits(75, Dm3, Da3, De3)
mean3 = np.mean(profits3)

print("\n ------- Question 3 Statistics -------")
print("Single 91-Day Sample Mean Profit:", round(sample_mean, 2))
print("Sample Standard Deviation:", round(sample_std, 2))
print("Standard Error of the Mean:", round(standard_error, 2))
print("95% Confidence Interval Lower Boundary:", round(ci_lower, 2))
print("95% Confidence Interval Upper Boundary:", round(ci_upper, 2))
print("10-Year (3,650 Days) Mean Daily Profit:", round(mean3, 2))




""" ------- Question 4 ------- """
# Loop through all Q values from 50 to 150
q_values = np.arange(50, 151)
profits4 = []

# For each q from 50 to 150, estimate 3650 days from question 3
for q in q_values:
    q_profits = calculate_profits(q, Dm3, Da3, De3)
    profits4.append(np.mean(q_profits))

profits4 = np.array(profits4)

plt.figure(figsize=(8, 6))
plt.plot(q_values, profits4, color='steelblue', marker='o', markersize=3, linestyle='-')
plt.xlabel('Order Quantity (Q)')
plt.ylabel('Estimated Expected Daily Profit ($)')
plt.title('Expected Daily Profit vs. Order Quantity (Q)')
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()



""" ------- Question 5 ------- """
# Locate the maximum point using numpy's argmax
optimal_index = np.argmax(profits4)
recommended_Q = q_values[optimal_index]
max_expected_profit = profits4[optimal_index]

print("\n ------ Question 5 Statistics ---")
print("Recommended Daily Order Quantity (Q*):", recommended_Q)
print("Maximum Estimated Expected Daily Profit:", max_expected_profit)


