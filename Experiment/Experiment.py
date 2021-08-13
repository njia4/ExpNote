#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import glob, os, shutil, datetime, time
import pickle
from .script_parser import script_parser
from config import * # Check if this is necessary
from utilities import *

import sys
sys.path.append(JPAC_DIR)

class Figure:
	def __init__(self, name, plot_code, experiment):
		self.exp = experiment
		self.name = name
		self.plot_code = plot_code
		self.fig = plt.figure(constrained_layout=True, dpi=100)
		self.ax = self.fig.add_subplot(111)
		self.lines = {}
		self.id = 0
		
	def update_plot(self):
		self.id += 1
		self.ax.cla()
		namespace = {}
		namespace.update(self.exp.analysis_namespace) # TODO
		namespace.update(self.exp.analysis_parameters)
		namespace.update({'df': self.exp.df})
		try: 
			exec(self.plot_code, {'fig': self.fig, 'ax': self.ax}, namespace)
			# self.fig.canvas.draw()
		except Exception as e:
			console_print('Analysis', 'Failed to run the plotting script.', method='error')
			if hasattr(e, 'message'):
				print(e.massage)
			else:
				print(e)
			return 0
		return 1

DF_INIT_DATA = {'Run Name': [np.nan], 'Valid': [1], 'Data Note': ''}
DF_INIT_COLUMNS = ['Run Name', 'Valid', 'Data Note']
EXP_DEFAULT_NAME = 'Archive'
EXP_DEFAULT_DF = pd.DataFrame(columns=DF_INIT_DATA)

class Experiment:
	def __init__(self, name=EXP_DEFAULT_NAME, df=EXP_DEFAULT_DF, script=None):
		self.name = name
		self.description = ''
		self.dt = datetime.datetime.now()

		self.df = df.copy() # Have to use copy() to get the namespace correct
		self.columns = []
		self.data_id = len(df['Run Name'].dropna())
		self.figs = {}
		
		self.script_dir = ''
		self.script_filename = ''
		self.static = ''
		self.analysis_parameters = {}
		self.analysis_script = ''
		self.analysis_namespace = {}

		exp_dir = generate_dir(self.name, self.dt)
		if not os.path.exists(exp_dir):
			os.makedirs(exp_dir)

		if script != None:
			self.set_analysis_script(script)

	def get_exp_info(self):
		console_print('Experiment', 'Send experiment ("{}") info.'.format(self.name))
		exp_info = {'name': self.name, 'description': self.description, 'script_dir': self.script_dir, 'script': self.script_filename}
		return exp_info
	def get_row(self, row_ind):
		if row_ind in self.df.index: # Check if row exist, otherwise return None
			return self.df.loc[row_ind]
		else:
			return pd.Series() # Return empty series if the row is not in the DataFrame
	def get_df(self):
		console_print('Experiment', 'Sending data table!')
		_df = self.df.sort_index() # Sort according to index
		_df = _df.fillna('null') # For working with Javascript. 
		payload = _df.to_dict('index') # Sending a dictionary so it will be compatible for JSON in the future
		return payload, len(self.df)
	def get_parameters(self):
		console_print('Experiment', 'Send script parameters. ({} items)'.format(len(self.analysis_parameters)))
		return self.analysis_parameters
	def get_figures(self):
		console_print('Experiment', 'Send figures. ({} figures detected)'.format(len(self.figs)))
		return self.figs

	def add_col(self, col_index, name):
		# Add an empty column for new a variable
		self.df.insert(col_index, name, pd.Series())

	def set_exp_info(self, msg):
		self.name = msg['name'] # TODO: DEAL WITH SAVING DIRECTORY
		self.description = msg['description']
	def set_cell(self, row, col, val):
		console_print('Experiment', 'Update cell (row: {}, col: {}, val: {})'.format(row, col, val))
		
		# Panda is using indexing instead of rwo number. If some variable is set before the data come in, 
		# it will mess up the order. So append some empty rows before assigning
		# TODO: MAYBE MAKE BETTER USE OF THE PANDA INDEXING SYSTEM. 
		# FOR EXAMPLE DIRECTLY CALL AND SET USING THE INDEX AND SORT BEFORE SAVING?
		# if row >= len(self.df):
		# 	_counter = row-len(self.df)
		# 	for ii in range(_counter):
		# 		self.df = self.df.append(pd.Series(), ignore_index=True)

		try:
			_v = float(val) # Try to convert the value to float when possible
		except:
			_v = val
		self.df.at[row, col] = _v

		# Update figures is costy since it is replotting everything. 
		# Will manually update plots from the GUI and use a different thread. 
		# self.update_figure()
	def set_parameters(self, data):
		for key in data.keys():
			try:
				self.analysis_parameters[key] = eval(data[key])
			except:
				self.analysis_parameters[key] = data[key]
			console_print('Experiment', 'Parameter update: ({} = {})'.format(key, data[key]))
	def set_settings(self, msg):
		pass
	def set_analysis_script(self, file):
		# Update script file name and path
		self.script_dir, self.script_filename = os.path.split(file)
		# Copy the script to local folder
		_src = file
		_dst = os.path.join(generate_dir(self.name, self.dt), self.script_filename)
		if _src != _dst:
			shutil.copy(_src, _dst)
		# Load and parse the analysis script
		console_print('Experiment', 'Loading script: {}'.format(self.script_filename))
		self.analysis_static, self.analysis_parameters, self.analysis_script, plots_code = script_parser(file)
		
		# Run static cell and reset analysis namespace
		self.analysis_namespace = {}
		exec(self.analysis_static, self.analysis_namespace)

		if "column_names" in self.analysis_namespace:
			_cols = self.analysis_namespace['column_names']
			
		self.figs = {} # Clear old figures
		for name, code in plots_code.items():
			self.add_figure(name, code)
	def set_figures(self):
		# for name, code in plots_code.items():
		# 	self.add_figure(name, code)
		pass

	def save_info(self):
		console_print('Experiment', 'Saving experiment info!')
		info_txt  = ''
		info_txt += 'Experiment Name: {}\n'.format(self.name)
		info_txt += 'Analysis script: {}\n'.format(self.script_filename)
		info_txt += 'Description: \n'
		info_txt += self.description
		info_filename = os.path.join(generate_dir(self.name, self.dt), 'info.txt')
		with open(info_filename, 'w') as file:
			file.write(info_txt)
	def save_df(self):
		console_print('Experiment', 'Saving data table!')
		df_file = os.path.join(generate_dir(self.name, self.dt), self.name+'.csv')
		self.df.sort_index().to_csv(df_file, index=False)
		return
	def save(self):
		self.save_info()
		self.save_df()

	def add_figure(self, name, data_sets):
		self.figs[name] = Figure(name, data_sets, self)

	def add_run(self, data_dict):
		# TODO: MAYBE NOT USING APPEND BUT RATHER CALL THE INDEX TO MAKE THINGS CONSISTENT
		# if self.data_id == len(self.df):
		# 	_df_header = self.df.columns.tolist()
		# 	_col_header = [_key for _key in data_dict.keys() if _key not in _df_header]
		# 	# if 'id' in data_dict.keys(): _col_header.remove('id')
		# 	self.df = self.df.append(data_dict, ignore_index=True)
		# 	if len(_col_header) > 0:
		# 		self.df = self.df[_df_header+_col_header]
		# else:
		# 	for key in data_dict.keys():
		# 		self.df.loc[self.data_id, key] = data_dict[key]

		# Cannot assign row with a pd.Series since it will remove user set values not in the data_dict
		for key in data_dict.keys():
			self.df.loc[self.data_id, key] = data_dict[key]
		data_dict = {key: render_numeric_value(val) for key, val in data_dict.items()}
		self.data_id += 1

		return self.data_id-1, data_dict

	def update_figure(self): # TODO: SEND AT ONCE
		for key in self.figs.keys():
			self.figs[key].update_plot()

	def do_analyze(self, fname):
		# Setup the analysis namespace
		self.analysis_namespace['data_file'] = fname
		self.analysis_namespace['result'] = pd.Series({'Run Name': os.path.split(fname)[-1]})
		self.analysis_namespace['data_dir'] = os.path.join(generate_dir(self.name, self.dt), 'Data')
		self.analysis_namespace.update(self.analysis_parameters)
		
		# Execute the analysis script
		try:
			exec(self.analysis_script, self.analysis_namespace)
			console_print('Analysis', 'Finished running the analysis script.')
		except Exception as e:
			console_print('Analysis', 'Failed to run the analysis script.', method='error')
			if hasattr(e, 'message'):
				print(e.massage)
			else:
				print(e)

		# Complete analysis result with more meta-data
		self.add_run(self.analysis_namespace['result']) # Add result to the DataFrame
		self.update_figure() # Update plots. This is probably ok since it is in the WorkerThread already. 

		return int(self.data_id-1) # The add_run function will increment the run index, so the current one is data_id-1

def load_exp(filename):
	exp_dir = os.path.split(filename)[0]
	print(exp_dir)
	with open(filename, 'r') as info_file:
		exp_name   = info_file.readline().split(':')[-1].strip()
		exp_script = info_file.readline().split(':')[-1].strip()
		printYellow(exp_script)
		exp_info   = ''.join(info_file.readlines()[1:])
		print(exp_info)
		try:
			exp_df = pd.read_csv(os.path.join(exp_dir, exp_name+'.csv'))
		except:
			exp_df = EXP_DEFAULT_DF

		exp = Experiment(name=exp_name, df=exp_df, script=os.path.join(exp_dir, exp_script))
	return exp





