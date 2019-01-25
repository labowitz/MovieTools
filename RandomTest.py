import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from io import StringIO
from matplotlib import colors
from scipy import stats

from scipy.optimize import curve_fit
from matplotlib.ticker import FormatStrFormatter

# sns.set_style("whitegrid")

hillFunc = lambda x, a, b, c: a*x**b/(c+x**b)+1

x = np.array([float(a) for a in ('0.0092 0.0097 0.8468 0.7887 1.7868 1.9587 3.0925 3.0989 6.6149 7.3477 14.1792 13.438'.split(' '))])
yr = np.array([float(a) for a in ('1.3810e+05 1.4011e+05 7.4226e+04 5.7742e+04 3.7518e+04 4.4779e+04 1.8557e+04 2.0599e+04 1.0007e+04 9.4158e+03 6.1240e+03 5.6919e+03'.split(' '))])
ys = np.array([float(a) for a in ('8.7138e+03 8.8298e+03 9.6564e+03 7.1695e+03 8.5073e+03 6.5928e+03 7651 8.4249e+03 7.7293e+03 7.6454e+03'.split(' '))])

x=x*100
yrNorm = (yr[0]+yr[1])/2
ys=yrNorm/ys
yr=yrNorm/yr

perc = np.linspace(0, 1500, 1500)
poptr, pcovr = curve_fit(hillFunc, x, yr, maxfev=10000)
percYr = hillFunc(perc, *poptr)
popts, pcovs = curve_fit(hillFunc, x[2:], ys, maxfev=10000)
percYs = hillFunc(perc, *popts)


fig, ax = plt.subplots(figsize=(4,3), facecolor='w')
fig.dpi = 100
# ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
# ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

ax.plot(x, yrNorm/yr/1e4, '.c', label='Receiver response')
ax.plot(perc, yrNorm/percYr/1e4, '-c')
ax.plot(x[2:], yrNorm/ys/1e4, '.m', label='Sender-receiver response')
# ax.plot(perc, yrNorm/percYs/1e4, '-m')
# ax.set_xlim([-50, 1500])
ax.set_ylim([0, 15])
ax.set_ylabel('mCherry (A.U.)')
ax.set_xlabel('Sender-receiver population size')
legend = ax.legend(loc='upper right')
# legend.get_frame().set_facecolor('C0')
# ax.legend()
# ax.set_yscale('log')
plt.show()