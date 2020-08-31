
import re

if __name__ == '__main__':
	m = re.match('(\w+)\s*=\s*([\W\w]*)', "run_tag = 'asdf'".strip())
	print(m.group(1))