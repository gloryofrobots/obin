class ObinException(Exception):
    message = u'Exception'

    def __init__(self, message=None):
        if message is not None:
            assert isinstance(message, unicode)
            self.message = message

    def _msg(self):
        return self.message

    def msg(self):
        from obin.objects.object_space import _w
        return _w(self._msg())

    def __str__(self):
        return self._msg()

    def __repr__(self):
        return self.__str__()

class ObinRuntimeError(ObinException):
    pass

class ObinTypeError(ObinException):
    def __init__(self, value):
        super(ObinTypeError, self).__init__()
        from obin.utils import tb
        tb()
        # assert isinstance(value, unicode)
        self.value = value

    def _msg(self):
        return u'TypeError : ' + self.value  # % (self.value, )


class ObinReferenceError(ObinException):
    def __init__(self, identifier):
        super(ObinReferenceError, self).__init__()
        self.identifier = identifier.value()

    def _msg(self):
        return u'ReferenceError: ' + self.identifier + u' is not defined'


class ObinRangeError(ObinException):
    def __init__(self, value=None):
        super(ObinRangeError, self).__init__()
        self.value = value

    def _msg(self):
        return u'RangeError: %s' % (self.value,)


class ObinKeyError(ObinRangeError):
    def __init__(self, value=None):
        super(ObinKeyError, self).__init__()
        self.value = value

    def _msg(self):
        return u'KeyError: %s' % (self.value,)

class ObinInvokeError(ObinRangeError):
    def __init__(self, value=None):
        super(ObinInvokeError, self).__init__()
        self.value = value

    def _msg(self):
        return u'InvokeError: expected argument with number %s' % (str(self.value),)


class ObinMethodInvokeError(ObinRangeError):
    def __init__(self, name, args):
        super(ObinMethodInvokeError, self).__init__()
        self.arguments = args
        self.name = name

    def _msg(self):
        return u'Method Invoke Error:  Can\'t find method  %s for arguments %s' % (str(self.name), str(self.arguments),)

class ObinSyntaxError(ObinException):
    def __init__(self, msg=u'', src=u'', line=0, column=0):
        super(ObinSyntaxError, self).__init__()
        self.error_msg = msg
        self.src = src
        self.line = line
        self.column = column

    def _msg(self):
        # error_src = self.src #self.src.encode('unicode_escape')
        if self.error_msg:
            return u'SyntaxError: "%s" in "%s" at line:%d, column:%d'  # %(self.error_msg, error_src, self.line, self.column)
        else:
            return u'SyntaxError: in "%s" at line:%d, column:%d'  # %(error_src, self.line, self.column)
