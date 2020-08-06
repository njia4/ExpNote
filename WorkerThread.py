#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import glob, os, shutil, datetime, time
from script_parser import script_parser
from config import *
from utilities import *

import sys
sys.path.append(JPAC_DIR)


DF_INIT_DATA = {'Run Name': [np.nan], 'Tag': np.nan, 'Valid': [1], 'Data Note': ''}
DF_INIT_COLUMNS = ['Run Name', 'Tag', 'Valid', 'Data Note']
EXP_DEFAULT_NAME = 'Archive'
EXP_DEFAULT_DF = pd.DataFrame(columns=DF_INIT_DATA)



##########################
### File Lookup Thread ###
##########################
# TODO: PUT IS SOMEWHERE REASONABLE. 
global_parameters = {
	'settings':{
		'save_flg': True,
	},
	
	'exp': None,
}

def worker(experiment):
	console_print('File Thread', 'Start!')
	counter = 0;
	while True:
		time.sleep(FILECHECK_FREQUENCY)
		print("Checked file!", counter)
		
		# data_input_dir = generate_dir(DATA_INPUT_FOLDER_NAME)
		# if not os.path.exists(data_input_dir):
		# 	console_print('Worker', '"{}" does not exist!'.format(DATA_INPUT_FOLDER_NAME), 'error')
		# 	continue

		# file_format = os.path.join(data_input_dir, "*."+FMT_DATAFILE)
		# files = glob.glob(file_format)
		# # files = sorted(files, key=lambda x: os.path.split) # TODO: SORT

		# if len(files) > 0:
		# 	for f in files:
		# 		# Move file
		# 		file_name = os.path.split(f)[-1]
		# 		src = f
		# 		dst_dir = generate_dir(global_parameters['exp'].name)
		# 		dst = os.path.join(dst_dir, file_name)
		# 		if not os.path.exists(dst_dir):
		# 			os.mkdir(dst_dir)
		# 		shutil.move(src, dst)

		# 		r = global_parameters['exp'].do_analyze(dst)

		# 		if not global_parameters['settings']['save_flg']:
		# 			os.remove(dst)

		# 		counter += 1

		counter += 1

		if counter >= 10:
			break

	console_print('File Thread', 'Abort!')
