__author__ = 'isaac'

import sys
import os

from Classifier import Classifier

alias = "[OLC]>> "

def main():
    print "SISTEMA CLASIFICADOR EN LINEA"
    home = os.getenv("HOME")
    caffe_root = home + '/caffe/'
    sys.path.insert(0, caffe_root + 'python')
    import caffe
    classifier = Classifier()


if __name__ == "__main__":
    main()

