import fileinput
from numpy.random import choice,rand


def translateSliceLength(s, sliceLength, dict):
    str = ''
    i = 0
    while i < len(s) - sliceLength:
        slice = s[i:i+sliceLength]

        if slice.lower() in dict:
            if rand(1)[0] <= dict[slice.lower()][0]:
                ch = choice(dict[slice.lower()][1], 1, p=dict[slice.lower()][2])
                str += ch[0]
                i += sliceLength - 1
            else:
                str += s[i]
        else:
            str += s[i]
        i += 1
    str += s[-sliceLength:]

    return str


def translate(s, dict, lengths):
    for i in range(len(lengths)):
        length = lengths[i]
        s = translateSliceLength(s, length, dict)
    return s


def toFloatIfPossible(str):
    try:
        return float(str)
    except ValueError:
        return str


if __name__ == '__main__':
    prob = 0.3
    file = open('dict.txt', 'r')
    lines = file.readlines()
    # dict = {line.split(':')[0]: list(zip(*[tuple([toFloatIfPossible(val) for val in repl.split('-')]) for repl in line.split(':')[1].rstrip('\n').split(',')])) for line in lines if len(line.split(':')) == 2}

    dict = {}
    lengths = []
    for line in lines:
        linesplit = line.split(':')
        if len(linesplit) == 2:
            keysplit = linesplit[0].split('-')

            curProb = prob
            if len(keysplit) == 2:
                curProb = float(keysplit[1])

            dict[keysplit[0]] = [curProb] + list(zip(*[tuple([toFloatIfPossible(val) for val in repl.split('-')]) for repl in linesplit[1].rstrip('\n').split(',')]))

            if len(keysplit[0]) not in lengths:
                lengths.append(len(keysplit[0]))

    print(dict)

    for line in fileinput.input():
        print(''.join(translate(line.rstrip(), dict, sorted(lengths, reverse=True))))
