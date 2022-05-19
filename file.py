from functools import reduce
from collections import defaultdict
from types import MethodType


def greeter(func):
    def inner(*args):
        result = func(*args)
        names = result.split()
        return 'Aloha ' + ' '.join([name[0].upper() + name[1:].lower() for name in names])
    return inner


def calc_sum(number):
    times = 1
    if number[0] == '-':
        times = -1
        number = number[1:]

    return times * reduce(lambda x, ch: x + ord(ch) - ord('0'), number, 0)


def sums_of_str_elements_are_equal(func):
    def inner(*args):
        result = func(*args)
        (a, b) = result.split()
        (sum_a, sum_b) = (calc_sum(a), calc_sum(b))

        if sum_a == sum_b:
            return f"{sum_a} == {sum_b}"
        return f"{sum_a} != {sum_b}"
    return inner


def format_output(*required_keys):
    def decorator(func):
        def inner(*args):
            func_result = func(*args)
            result = defaultdict(str)

            aggregated_value = {}
            for required_key in required_keys:
                splitted_key = required_key.split('__')
                for (key, value) in func_result.items():
                    if key in splitted_key:
                        if value == '':
                            value = "Empty value"
                        aggregated_value[key] = value

                for key in splitted_key:
                    if key not in aggregated_value:
                        raise ValueError()
                    result[required_key] += aggregated_value[key] + " "
                result[required_key] = result[required_key][:-1]

            return dict(result)
        return inner
    return decorator


def add_method_to_instance(klass):
    def decorator(func):
        def class_func(self, *args):
            return func(*args)
        setattr(klass, func.__name__, MethodType(class_func, klass))

        def inner(*args):
            return func(*args)
        return inner
    return decorator

