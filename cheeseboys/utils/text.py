# -*- coding: utf-8 -

# Deprecated.
# All this stuff will be moved in the ktextsurfacewrited module someday

def _generateTextLengthException(text_too_long, max_length):
    return ValueError('Text "%s" is really too long for me to fit a max length of %s!' % (text_too_long, max_length))

def normalizeTextLength(text_too_long, font, max_length):
    """This function take a text too long and split it in a list of smaller text lines.
    The final text max length must be less/equals than max_length parameter, using the font passed.
    Return a list of text lines.
    """
    words = text_too_long.split(" ")
    words_removed = []
    tooLong = True
    txt1 = txt2 = ""
    while tooLong:
        try:
            words_removed.append(words.pop())
        except IndexError:
            raise _generateTextLengthException(text_too_long, max_length)
        txt1 = " ".join(words)
        if font.size(txt1)[0]<=max_length:
            tooLong = False
    words_removed.reverse()
    txt2 = " ".join(words_removed)
    if txt2==text_too_long:
        raise _generateTextLengthException(text_too_long, max_length)
    if font.size(txt2)[0]<=max_length:
        return [txt1, txt2]
    else:
        return [txt1] + normalizeTextLength(txt2, font, max_length)