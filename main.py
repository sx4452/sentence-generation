__author__ = 'ben'

import time
import os
import jieba
import itertools

CORPUSPATH = 'Reduced'

def Train(inputFile, filecnt):
    CountSingle = {}
    CountDouble = {}
    for i in xrange(0, filecnt):
        inputRead = inputFile[i].read()
        seg_list = jieba.cut(inputRead)
        curseg = next(seg_list)
        for seg in seg_list:
            nextseg = seg
            doubleseg = curseg + nextseg
            if curseg in CountSingle:
                CountSingle[curseg] += 1
            else:
                CountSingle[curseg] = 1
            if doubleseg in CountDouble:
                CountDouble[doubleseg] +=1
            else:
                CountDouble[doubleseg] = 1
            curseg = nextseg
        if curseg in CountSingle:
            CountSingle[curseg] += 1
        else:
            CountSingle[curseg] = 1
    return CountSingle, CountDouble

def main():
    print 'main'
    inputFile = {}
    filecnt = 0;
    paths = os.walk(CORPUSPATH)
    for path in paths:
        for i in xrange(0,len(path[2])):
            if(cmp(path[2][i][-4:], '.txt') == 0):
                inputFile[filecnt] = open(path[0] + '\\' + path[2][i], 'r+')
                filecnt += 1
    [CountSingle, CountDouble] = Train(inputFile, filecnt)
    for i in xrange(0, filecnt):
        inputFile[i].close()

    cmd = 'Y'
    word = ''
    wordseg = ''
    while(cmp(cmd, 'Y') == 0):
        wordcnt = 0
        while(cmp(word, '#') != 0):
            word = raw_input('Please input a word\n')
            if(cmp(word, '#') == 0):
                break
            wordseg = wordseg + ' '+ unicode(word, 'gb2312')
            wordcnt += 1
            if wordcnt > 8:
                print 'WARNING! Too much words, it may cost infinity time'
        sentencelist = itertools.permutations(wordseg.split(' ')[1:])
        Pdouble = {}
        result = ''
        maxP = 0.0
        for sentence in sentencelist:
            Pall = 1.0
            sent = ''
            for i in xrange(0, len(sentence)-1):
                sent = sent + sentence[i]
                doubleword = sentence[i]+sentence[i+1]
                if doubleword not in Pdouble:
                    if (doubleword in CountDouble) and (sentence[i] in CountSingle):
                        Pdouble[doubleword] = float(CountDouble[doubleword])/float(CountSingle[sentence[i]])
                    else:
                        if (sentence[i] in CountSingle):
                            Pdouble[doubleword] = (1.0/float(len(CountDouble)))/float(CountSingle[sentence[i]])
                        else:
                            Pdouble[doubleword] = (1.0/float(len(CountDouble)))/float(len(CountSingle))
                Pall = Pall * Pdouble[sentence[i]+sentence[i+1]]
            if(Pall > maxP):
                maxP = Pall
                sent = sent + sentence[len(sentence)-1]
                result = sent
        print 'result is'
        print result
        word = ''
        wordseg = ''
        cmd = raw_input('Do you want to generate one more sentence?(Y/N)\n')

if __name__ == '__main__':
    strat = time.clock()
    main()
    end = time.clock()
    print 'running time is'
    print end

