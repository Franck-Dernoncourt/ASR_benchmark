import numpy
import string


def format_text(text, lower_case=False, remove_punctuation=False,write_numbers_in_letters=True):
    '''

    '''
    if lower_case: text = text.lower()

    # https://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string-in-python
    table = str.maketrans({key: None for key in string.punctuation})
    if remove_punctuation: text = text.translate(table)

    if write_numbers_in_letters:
        text = text.replace('0',' zero ')
        text = text.replace('1',' one ')
        text = text.replace('2',' two ')
        text = text.replace('3',' three ')
        text = text.replace('4',' four ')
        text = text.replace('5',' five ')
        text = text.replace('6',' six ')
        text = text.replace('7',' seven ')
        text = text.replace('8',' eight ')
        text = text.replace('9',' nine ')
        # https://stackoverflow.com/questions/1546226/simple-way-to-remove-multiple-spaces-in-a-string
        text = ' '.join(text.split())
    return text

def wer2(r, h):
    '''
    This function was originally written by Martin Thoma
    https://martin-thoma.com/word-error-rate-calculation/

    Calculation of WER with Levenshtein distance.

    Works only for iterables up to 254 elements (uint8).
    O(nm) time ans space complexity.

    Parameters
    ----------
    r : list
    h : list

    Returns
    -------
    int

    Examples
    --------
    >>> wer("who is there".split(), "is there".split())
    1
    >>> wer("who is there".split(), "".split())
    3
    >>> wer("".split(), "who is there".split())
    3
    '''
    # Initialization
    d = numpy.zeros((len(r)+1)*(len(h)+1), dtype=numpy.uint8)
    d = d.reshape((len(r)+1, len(h)+1))
    for i in range(len(r)+1):
        for j in range(len(h)+1):
            if i == 0:
                d[0][j] = j
            elif j == 0:
                d[i][0] = i

    # Computation
    for i in range(1, len(r)+1):
        for j in range(1, len(h)+1):
            if r[i-1] == h[j-1]:
                d[i][j] = d[i-1][j-1]
            else:
                substitution = d[i-1][j-1] + 1
                insertion    = d[i][j-1] + 1
                deletion     = d[i-1][j] + 1
                d[i][j] = min(substitution, insertion, deletion)

    return d[len(r)][len(h)]


def wer(ref, hyp ,debug=False):
    '''
    This function was originally written by SpacePineapple
    http://progfruits.blogspot.com/2014/02/word-error-rate-wer-and-word.html
    '''
    DEL_PENALTY = 1
    SUB_PENALTY = 1
    INS_PENALTY = 1
    #r = ref.split()
    #h = hyp.split()
    r= ref
    h = hyp
    #costs will holds the costs, like in the Levenshtein distance algorithm
    costs = [[0 for inner in range(len(h)+1)] for outer in range(len(r)+1)]
    # backtrace will hold the operations we've done.
    # so we could later backtrace, like the WER algorithm requires us to.
    backtrace = [[0 for inner in range(len(h)+1)] for outer in range(len(r)+1)]

    OP_OK = 0
    OP_SUB = 1
    OP_INS = 2
    OP_DEL = 3

    # First column represents the case where we achieve zero
    # hypothesis words by deleting all reference words.
    for i in range(1, len(r)+1):
        costs[i][0] = DEL_PENALTY*i
        backtrace[i][0] = OP_DEL

    # First row represents the case where we achieve the hypothesis
    # by inserting all hypothesis words into a zero-length reference.
    for j in range(1, len(h) + 1):
        costs[0][j] = INS_PENALTY * j
        backtrace[0][j] = OP_INS

    # computation
    for i in range(1, len(r)+1):
        for j in range(1, len(h)+1):
            if r[i-1] == h[j-1]:
                costs[i][j] = costs[i-1][j-1]
                backtrace[i][j] = OP_OK
            else:
                substitutionCost = costs[i-1][j-1] + SUB_PENALTY # penalty is always 1
                insertionCost    = costs[i][j-1] + INS_PENALTY   # penalty is always 1
                deletionCost     = costs[i-1][j] + DEL_PENALTY   # penalty is always 1

                costs[i][j] = min(substitutionCost, insertionCost, deletionCost)
                if costs[i][j] == substitutionCost:
                    backtrace[i][j] = OP_SUB
                elif costs[i][j] == insertionCost:
                    backtrace[i][j] = OP_INS
                else:
                    backtrace[i][j] = OP_DEL

    # back trace though the best route:
    i = len(r)
    j = len(h)
    numSub = 0
    numDel = 0
    numIns = 0
    numCor = 0
    if debug:
        print("OP\tREF\tHYP")
        lines = []
    while i > 0 or j > 0:
        if backtrace[i][j] == OP_OK:
            numCor += 1
            i-=1
            j-=1
            if debug:
                lines.append("OK\t" + r[i]+"\t"+h[j])
        elif backtrace[i][j] == OP_SUB:
            numSub +=1
            i-=1
            j-=1
            if debug:
                lines.append("SUB\t" + r[i]+"\t"+h[j])
        elif backtrace[i][j] == OP_INS:
            numIns += 1
            j-=1
            if debug:
                lines.append("INS\t" + "****" + "\t" + h[j])
        elif backtrace[i][j] == OP_DEL:
            numDel += 1
            i-=1
            if debug:
                lines.append("DEL\t" + r[i]+"\t"+"****")
    if debug:
        lines = reversed(lines)
        for line in lines:
            print(line)
        #print("#cor " + str(numCor))
        #print("#sub " + str(numSub))
        #print("#del " + str(numDel))
        #print("#ins " + str(numIns))
    #return (numSub + numDel + numIns) / (float) (len(r))
    wer_result = round( (numSub + numDel + numIns) / (float) (len(r)), 3)
    #return {'WER':wer_result, 'Cor':numCor, 'Sub':numSub, 'Ins':numIns, 'Del':numDel}
    return {'changes': numSub + numDel + numIns, 'corrects':numCor, 'substitutions':numSub, 'insertions':numIns, 'deletions':numDel}


if __name__ == "__main__":
    import doctest
    #doctest.testmod()
    print(wer("who is there".split(), "is there a cat".split()))
    print(wer("who is there".split(), "who is cat".split()))
    print(wer("blue had range of okay".split(), "blue hydrangea bouquet".split()))
    print(wer("blue hydrangea bouquet".split(), "blue had range of okay".split()))
