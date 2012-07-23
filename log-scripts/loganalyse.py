import os
from numpy import arange
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime

dictionary = {}

def addtodict(key, value):
	global dictionary
	:

def letsanalyse():
	pathtolog = input("Enter the path to the root directory containing the logs: #")
	pathtopdf = input("Enter the path where plots will be saved in a pdf file: #")
	print '****Now choosing tags and keywords from log****'
	tag = input("Enter I ---> info, D---> debug, E ---> exception: #")
	
