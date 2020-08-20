from Experiment.Experiment import Experiment

data_file = '/home/jia/dev/Test/ExpNote/2020/08/20/Archive/Data/12-07-2018_15_22_33.fits'
script_file = '/home/jia/Desktop/SingleSiteDeconvolution_v0.ipynb'

exp = Experiment(script=script_file)

if __name__ == '__main__':
	data_id = exp.do_analyze(data_file)
	r = exp.get_row(data_id)

	for _key in r.keys():
		print(_key, r[_key])

	print(exp.df)