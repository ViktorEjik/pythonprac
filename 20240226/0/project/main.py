import sys
import cowsay


if __name__ == '__main__':
    arg = sys.argv
    if arg[1] in cowsay.list_cows():
        print(cowsay.cowsay(arg[2], arg[1]))
    else:
        with open(arg[1], 'r') as f:
            s = cowsay.read_dot_cow(f)
        print(cowsay.cowsay(arg[2], cowfile=s))

