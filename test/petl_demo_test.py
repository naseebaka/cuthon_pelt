from peltdemo import Pelt as CythonPelt
from ruptures import Pelt as Pelt

import ruptures as rpt
import time
import matplotlib.pylab as plt


n = 100000
model = "l2"
min_size = 3
jump = 5
n_bkps = 3
dim = 1
sigma = 1


signal, _ = rpt.pw_constant(n, dim, n_bkps, noise_std=sigma)


print("Testing Rupture")
start = time.time()
algo = Pelt(model=model, min_size=min_size, jump=jump)
my_bkps = algo.fit_predict(signal, pen=3)
end = time.time()

print("Start time:", start)
print("End time:", end)
print("Time taken:", end - start)

rpt.display(signal, range(len(my_bkps)), my_bkps, figsize=(10, 6))
plt.show()


print("Testing Cythonized")
start = time.time()
algo = CythonPelt(model=model, min_size=min_size, jump=jump)
my_cython_bkps = algo.fit_predict(signal, pen=3)
end = time.time()

print("Start time:", start)
print("End time:", end)
print("Time taken:", end - start)

rpt.display(signal, range(len(my_cython_bkps)), my_cython_bkps, figsize=(10, 6))
plt.show()

if my_bkps == my_cython_bkps:
    print("Outputs matching")
else:
    print("Outputs not matching")

input()