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

def wer(r, h):
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

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print(wer("who is there".split(), "is there a cat".split()))
    print(wer("who is there".split(), "who is cat".split()))
    print(wer("blue had range of okay".split(), "blue hydrangea bouquet".split()))
    print(wer("blue hydrangea bouquet".split(), "blue had range of okay".split()))


