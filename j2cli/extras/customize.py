
class CustomizationModule(object):
    """ The interface for customization functions, defined as module-level functions """

    def __init__(self, module=None):
        if module is not None:
            def howcall(*args):
                print(args)
                exit(1)

            # Import every module function as a method on ourselves
            for name in self._IMPORTED_METHOD_NAMES:
                try:
                    setattr(self, name, getattr(module, name))
                except AttributeError:
                    pass

    # stubs

    def j2_environment_params(self):
        return {}

    def j2_environment(self, env):
        return env

    def alter_context(self, context):
        return context

    def extra_filters(self):
        return {}

    def extra_tests(self):
        return {}

    _IMPORTED_METHOD_NAMES = [
        f.__name__
        for f in (j2_environment_params, j2_environment, alter_context, extra_filters, extra_tests)]
