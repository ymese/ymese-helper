#!/usr/bin/env python

from optparse import OptionParser
from sendowls import make_zip_sites
import sys

def hello():
    return 'hello word'

def get_args(name):
    swicher={
        'deploy-sendowl': hello()
    }
    return swicher.get(name, False)

def main():
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-c", "--config", dest="config_url",
                      help="Config site urls")
    parser.add_option("-p", "--plugin", dest="plugin_detail",
                      help="read data from FILENAME")
    parser.add_option("-d", "--directory", dest="project_dir",
                      help="Project directory")
    parser.add_option("-n", "--name", dest="plugin_name",
                      help="Plugin name")

    (options, args) = parser.parse_args()
    make_zip_sites( 
        options.config_url,
        options.plugin_detail,
        options.project_dir,
        options.plugin_name
    )
    

if __name__ == "__main__":
    main()