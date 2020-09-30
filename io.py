''' Take our default path to save external data. '''
from os.path import join, dirname
data_dir = join(dirname(__file__), "data")
try:lib=__import__('.lib');from lib import *
except Exception as e:print(e)
