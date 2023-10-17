from collections import Counter
import timeit

def f_dict(s: str):
    d = dict()
    for word in s.split():
        try:
            d[word] += 1
        except:
            d[word] = 1
    return d


def f_count(s: str):
    return Counter(s.split())


if __name__ == '__main__':
    s = ',knkdmv wnlkcn bwkwj j j j kfklan jdkjfjojamsdjlm kjkldm  lwlf, endwlldk jad,lma sndmkv ajkm vjjk;lm ldsm '
    print(timeit.Timer('f_dict(s)', globals=globals()).autorange())
    print(timeit.Timer('f_count(s)', globals=globals()).autorange())
    print(f_dict(s))
    print(f_count(s))
