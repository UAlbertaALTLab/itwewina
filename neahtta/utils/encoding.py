def encodeOrFail(S):
    try:
        return S.encode('utf-8')
    except:
        return S

def decodeOrFail(S):
    try:
        return S.decode('utf-8')
    except:
        return S


def ensure_unicode(text):
    """
    Returns a unicode object, regardless if text is a str or unicode object.
    Decodes str objects as UTF-8.

    :param text:
    :return:
    """
    if isinstance(text, str):
        return text.decode('UTF-8')
    else:
        return text