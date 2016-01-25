from root import W_Callable
from obin.runtime import error
from obin.types import api, space
from rpython.rlib import jit


class W_Fiber(W_Callable):
    def __init__(self, fiber):
        self.fiber = fiber

    def _tostring_(self):
        return "<fiber>"

    def _tobool_(self):
        return True

    def _behavior_(self, process):
        return process.std.behaviors.Fiber

    def _call_(self, process, args):

        if not self.fiber.is_waiting():
            error.throw_1(error.Errors.FIBER_FLOW, space.newstring(u"Can't resume active fiber"))

        if api.n_length(args) == 0:
            value = space.newundefined()
        elif api.n_length(args) == 1:
            value = api.at_index(args, 0)
        else:
            value = args
        process.switch_to_fiber(self.fiber, value)


def newfiber(process):
    fiber1 = process.fiber
    w_fiber1 = W_Fiber(fiber1)
    fiber2 = process.create_fiber()
    w_fiber2 = W_Fiber(fiber2)
    return w_fiber1, w_fiber2


def activate_fiber(process, fiber_wrap, function, args):
    process.activate_fiber(fiber_wrap.fiber, function, args)