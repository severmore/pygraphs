import matplotlib as mpl
import matplotlib.pyplot as plt
import math

dpi = 80
fig = plt.figure(dpi = dpi, figsize = (512 / dpi, 384 / dpi) )
mpl.rcParams.update({'font.size': 10})

plt.axis([0, 100, 0, 100])

plt.title('Algorithm execution time')
plt.xlabel('st number')
plt.ylabel('time')

xs = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
vals = [0.33, 2.64, 4.43, 9.81, 16.72, 25.37, 41.22, 54.52, 60.2, 87.20]

x_third = []

for x in xs:
    x_third += [x**3 // 10000]

plt.plot(xs, vals, 'ro', color = 'blue',
         label = 'O(n)')
plt.plot(xs, x_third, color = 'red', linestyle = 'dashed',
         label = 'n^3')

plt.grid()

plt.legend(loc = 'upper right')
fig.savefig('O_n.png')