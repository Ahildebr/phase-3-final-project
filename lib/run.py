#!/usr/bin/env python3
from __init__ import *  
from transactions import *
from accounts import *
from cli import *
from helpers import *



def run_start():
    accounts_table() 
    transactions_table()
    start_cli()

run_start()