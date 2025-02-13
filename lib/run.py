#!/usr/bin/env python3
from __init__ import *  
from cli import start_cli



def run_start():
    accounts_table() 
    transactions_table()
    start_cli()

run_start()