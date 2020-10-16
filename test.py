import pandas as pd
from Experiment.Experiment import Experiment

dat1 = Experiment()
dat2 = Experiment()

dat1.set_cell(0, 'a', 1)

if __name__ == '__main__':
	print(dat1.df)
	print(dat2.df)
