# -*- coding: utf-8 -*-
from __future__ import absolute_import
from reportmaker import create_app
from conf import get_config
import os

# load config via env
env = os.environ.get('REPORTMAKER_ENV', 'dev')
config = get_config(env)
reportmaker = create_app(**config)
