import sys
from math import *

fun_param_dict = dict()
ans = list()
global count_fun
count_fun = 0


def parser(s: str):

    def pars_fun(s_list: list):
        fun_param_dict[s_list[0][1:]] = (s_list[-1], s_list[1:-1])

    def pars_param(s_list: list):
        try:
            fun = fun_param_dict[s_list[0]]
        except:
            print('Функция не определена')
            sys.exit()
        args = list()
        for arg in s_list[1:]:
            if arg.isnumeric():
                args.append(float(arg))
            else:
                args.append(arg)
        global count_fun
        count_fun += 1
        print(eval(fun[0], globals(), dict(zip(fun[1], args))))

    s_list = s.split()
    if s_list[0][0] == ':':
        pars_fun(s_list)
    else:
        pars_param(s_list)


def main():
    x = input()
    count = 1
    while x[:4] != 'quit':
        parser(x)
        x = input()
        count += 1
    else:
        print(x[4:].format(count_fun, count))


if __name__ == '__main__':
    main()
