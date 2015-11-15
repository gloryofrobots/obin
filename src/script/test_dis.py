import dis

class C(object):
    def __init__(self, x):
        self.x = x

    def action(self, *args):
        print "ARGS", args


def f2(x, y):
    print x + y

def m1(self):
    print self.x


def f(*args):
    try:
        return 1/0
    except RuntimeError as e:
        print "RuntimeError"
    except BaseException as e:
        print "BaseException"
    finally:
        print "Finally"


dis.dis(f)


