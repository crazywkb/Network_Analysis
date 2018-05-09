import time


def printer(switch=True):
    """
    decoration of function
    :param switch: print the result of func or not
    :return: func()
    """

    def deco(func):
        def __deco(*args, **kwargs):
            result = func(*args, **kwargs)

            if switch:
                print("==========================================================================")
                print("Function \033[1;34m %s \033[0m called." % func.__name__)
                print("Output result: \033[1;32m %s \033[0m" % str(result))
                print()

            return result

        return __deco

    return deco


def timer(switch=True):
    def deco(func):
        def __deco(*args, **kwargs):
            if switch:
                start_time = time.time()
                result = func(*args, **kwargs)
                end_time = time.time()
                print("==========================================================================")
                print("Function \033[1;34m %s \033[0m called." % func.__name__)
                print("Time cost: \033[1;35m %f \033[0m" % (end_time - start_time))
                print()

            else:
                result = func(*args, **kwargs)

            return result

        return __deco

    return deco


def watcher(switch=True):
    def deco(func):
        def __deco(*args, **kwargs):
            if switch:
                start_time = time.time()
                result = func(*args, **kwargs)
                end_time = time.time()
                print("==========================================================================")
                print("Function \033[1;34m %s \033[0m called." % func.__name__)
                print("Output result: \033[1;32m %s \033[0m" % str(result))
                print("Time cost: \033[1;35m %f \033[0m" % (end_time - start_time))
                print("")

            else:
                result = func(*args, **kwargs)

            return result

        return __deco

    return deco
