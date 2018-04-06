# -*- coding: utf-8 -*-


import os
from os.path import join, dirname
from dotenv import load_dotenv


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = False

load_dotenv(override=True)
