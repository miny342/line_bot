from .base import *
from .secret import *

DEBUG = False

ALLOWED_HOSTS = ["miny-ki.f5.si"]+[f"192.168.2.{i}" for i in range(100,200)]