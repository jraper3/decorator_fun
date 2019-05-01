# Standard Library Imports
import sys
from functools import wraps
import logging
import traceback
import datetime

# Third Party Library Imports

# Custom Package Imports


# Code Start
def debug(orig_func=None, *, throw_err=False, print_dbg=False, logfile=None):
	def _decorate(func):
		if not logfile:
			today = datetime.date.today()
			logfile = f'{today}.log'
		logging.basicConfig(filename=logfile, level=logging.DEBUG)

		@wraps(func)
		def wrapper(*args, **kwargs):
			name = func.__name__
			arg_list = [str(x) for x in args]
			kwarg_list = [f'{k}={v}' for k, v in kwargs.items()]
			arg_str = ', '.join([*arg_list, *kwarg_list])
			dt = datetime.datetime.now()
			try:
				ret = func(*args, **kwargs)
				log_str = f'{dt}\n{name}({arg_str}) = {ret}\n'
				logging.debug(log_str)
				return ret
			except:
				if throw_err:
					raise
				trace_str = traceback.format_exc()
				log_str = f'{dt} -- args: {arg_str}\n{trace_str}'
				if print_dbg:
					print(log_str)
				else:
					logging.error(log_str)
		return wrapper
	if orig_func:
		return _decorate(orig_func)
	else:
		return _decorate


@debug(throw_err=True)
def raise_error(*args, **kwargs):
	raise Exception('OhNoes!!! An Errooooooor!!!!!!')


@debug
def log_error(*args, **kwargs):
	raise Exception('OhNoes!!! An Errooooooor!!!!!!')


@debug(print_dbg=True)
def print_error(*args, **kwargs):
	raise Exception('OhNoes!!! An Errooooooor!!!!!!')


if __name__ == '__main__':
	print('logging...')
	log_error()
	print('printing...')
	print_error()
	print('raising...')
	raise_error()
