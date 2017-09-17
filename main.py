import argparse, os
import subprocess
from preprocessor import preprocessor
from parser import airodump_parser

def main():
    print 'Welcome to WiFiRyu -->'

    # Prepare output directory in /tmp to for airodump-ng
    preprocessor().prepare_output_dir()

    #Create monitor mode interface.
    #Code to be added.

    #Start airodump-ng in subprocess.
    #Code to be added.

    #Read airodump-ng output csv file.
    header, entries = airodump_parser('/root/1-01.csv')
    print header
    print entries


def dump():
    print '--- Inside dump'


if __name__ == '__main__':
    main()
