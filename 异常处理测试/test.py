import sys
import traceback
def divison(a, b):
    try:
        print 'res = %s' %(a / b)
    except (ZeroDivisionError, ArithmeticError) as e:
        return str(e)
    else:
        print '%s / %s = %s' %(a, b, a / b)
    finally:
        print 'finally clause'
print 'return value:%s' %divison(2, 2)

class SelfException(ZeroDivisionError):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self)
    def __repr__(self):
        return self.value
try:
    raise SelfException('OK')
except SelfException as err:
    print 'LAILE'
    print 'exception:%s' %err

def get_trace_str(tp, val, tb):
    trace_info_list = traceback.format_exception(tp, val, tb)
    trace_str = ' '.join(trace_info_list)
    print 'sys.excepthook'
    print trace_str
sys.excepthook = get_trace_str
try:
    1 / 0
except TypeError as e:
    res = traceback.format_exc()
    print str(e.message)
    print res