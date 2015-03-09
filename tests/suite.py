#!../python
import os
import sys
here = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(1, here)


os.environ["MOSEKLM_LICENSE_FILE"]="27000@quantsrv"

if __name__ == '__main__':
    print "Environment used:"
    print sys.prefix

    print "Path:"
    for x in sys.path:
        print x

    import nose
    nose.main()