import re
import json

import sys
sys.path.append("/home/jia/Dropbox/code/jpac")

def script_parser(fname):
    fmt = fname.split('.')[-1]

    if fmt == 'ipynb':
        return parse_ipynb(fname)
    if fmt == 'py':
        return parse_py(fname)

def parse_py(fname):
    code = ''
    with open(fname, 'r') as f:
        for line in f.readlines():
            code += line
    return {}, code

def parse_ipynb(fname):
    script_static = ''
    parameter_dict = {}
    script_code = ''
    plots_code = {}
    
    with open(fname, 'r') as f:
        cells = json.loads(f.read())['cells']
    
    for _cell in cells:
        _code = _cell['source']
        if len(_code) > 0:
            if _code[0] == "### Static ###\n":
                for line in _code:
                    script_static += line

            if _code[0] == "### Modifiable Parameters ###\n":
                for line in _cell['source'][1:]:
                    # m = re.match('(\w+)\s*=\s*([-]?[0-9\.]*[e]?[-]?[0-9]+)', line.strip())
                    m = re.match('(\w+)\s*=\s*([\']?\w+[\']?)', line.strip())
                    if m != None:
                        key = m.group(1)
                        val = m.group(2)
                        try:
                            parameter_dict[key] = float(val)
                        except:
                            parameter_dict[key] = val
                parameter_code = ''.join(_cell['source'])
            if _code[0] == "### Analysis Script ###\n":
                for line in _cell['source']:
                    script_code += line
            if _code[0] == "### Plots ###\n":
                plot_name = _cell['source'][1].replace('#', '').strip()
                plot_code = ''.join(_cell['source'])
                plots_code[plot_name] = plot_code
            
    return script_static, parameter_dict, script_code, plots_code

if __name__ == '__main__':
    fname = 'user/MOT_absorp_img.ipynb'
    # fname = 'user/simple_analysis.py'
    
    # def load(fname):
    
    global analysis_io
    parameters, code, plots = script_parser(fname)
    data_file = '/home/jia/Desktop/AnalysisCodeTest/RawData/2020-05-07-18;39;09.aia'
    analysis_io = {'data_file': data_file, 'result': {}, 'global_var': {}}
    
    local = {}
    exec(code, analysis_io)
    print(analysis_io['result'])

    print(locals())
