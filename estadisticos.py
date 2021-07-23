import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

x = np.array([2, 7,9,12,15])
y = np.array([5, 15,3,4,18])
slope, intercept, r_value, p_value, std_err = linregress(x, y)
print("slope: %f, intercept: %f" % (slope, intercept))
print("R-squared: %f" % r_value**2)
  
plt.figure(figsize=(15, 5))
plt.plot(x, y, 'o', label='original data')
plt.plot(x, intercept + slope*x, 'r', label='fitted line')
plt.legend()
plt.grid()
plt.show()