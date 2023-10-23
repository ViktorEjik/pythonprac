from collections import Counter


def main():
    w = int(input())
    text = ''
    while line := input().lower():
        str = ''
        for char in line:
            if char.isalpha() or char == ' ':
                str += char
            else:
                str += ' '
        text += ' ' + str
    count = Counter(text.split())
    
    ans = list()
    for key, value in count.most_common():
        if len(key) == w:
            ans.append(key)
    print(*ans[::-1])
    


if __name__ == '__main__':
    main()
