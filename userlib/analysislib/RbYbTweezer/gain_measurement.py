import lyse
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize

df = lyse.data()
# df_grouped = df.groupby('cooling_aom_ttl_dur').agg('mean')

means = df['basic_image_reader']['mean'].values
variances = df['basic_image_reader']['variance'].values

def model(x,a,b):
    return a*x + b

popt, pcov = scipy.optimize.curve_fit(model,means,variances)

plt.figure(0)
plt.plot(means,variances,'kx')

mesh = np.linspace(0,np.amax(means),100)
plt.title('Andor_iXon_ultra system gain')
plt.plot(mesh,model(mesh,*popt),'r',label='K = '+str(np.round(popt[0],4)))
plt.xlabel('mean counts (DN)')
plt.ylabel(r'variance (DN$^2$)')
plt.legend()
plt.grid()
