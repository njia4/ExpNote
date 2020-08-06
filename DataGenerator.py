import numpy as np
import time, datetime

def Gaussian2D(xx, yy):
    return 1.*np.exp(-(xx**2+yy**2))
xx, yy = np.meshgrid(np.linspace(-1, 1, 128), np.linspace(-1, 1, 128))

ii = 0
while 1:
	zz = Gaussian2D(xx, yy)+.05*np.random.rand(128, 128)
	np.savetxt('Test/DataIn/IMG_{}.txt'.format(ii), zz)
	print(ii)
	ii += 1
	time.sleep(1.)