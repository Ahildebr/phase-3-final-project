#!/usr/bin/env python3
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def line_break():
    print("-" * 10)

def enter_choice():
    input("Press Enter to continue... ")