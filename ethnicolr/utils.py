# -*- coding: utf-8 -*-

import sys

def isstring(s):
    # if we use Python 3
    if (sys.version_info[0] >= 3):
        return isinstance(s, str)
    # we use Python 2
    return isinstance(s, basestring)


def column_exists(df, col):
    """Check the column name exists in the DataFrame.

    Args:
        df (:obj:`DataFrame`): Pandas DataFrame.
        col (str): Column name.

    Returns:
        bool: True if exists, False if not exists.

    """
    if col and (col not in df.columns):
        print("The specify column `{0!s}` not found in the input file"
              .format(col))
        return False
    else:
        return True


def fixup_columns(cols):
    """Replace index location column to name with `col` prefix

    Args:
        cols (list): List of original columns

    Returns:
        list: List of column names

    """
    out_cols = []
    for col in cols:
        if type(col) == int:
            out_cols.append('col{:d}'.format(col))
        else:
            out_cols.append(col)
    return out_cols


def find_ngrams(vocab, text, n):
    """Find and return list of the index of n-grams in the vocabulary list.

    Generate the n-grams of the specific text, find them in the vocabulary list
    and return the list of index have been found.

    Args:
        vocab (:obj:`list`): Vocabulary list.
        text (str): Input text
        n (int): N-grams

    Returns:
        list: List of the index of n-grams in the vocabulary list.

    """

    wi = []

    if not isstring(text):
        return wi

    a = zip(*[text[i:] for i in range(n)])
    for i in a:
        w = ''.join(i)
        try:
            idx = vocab.index(w)
        except Exception as e:
            idx = 0
        wi.append(idx)
    return wi

def transform_and_pred(df = df, namecol = '__last_name', cls, maxlen=FEATURE_LEN):

    # build X from index of n-gram sequence
    X = np.array(df[nn][namecol].apply(lambda c:
                                                 find_ngrams(cls.vocab,
                                                             c, NGRAMS)))
    X = sequence.pad_sequences(X, maxlen=maxlen)

    proba = cls.model.predict(X, verbose=2)

    df.loc[nn, '__pred'] = np.argmax(proba, axis=-1)

    df.loc[nn, 'race'] = df[nn]['__pred'].apply(lambda c:
                                                    cls.race[int(c)])

    # take out temporary working columns
    del df['__pred']
    del df[namecol]

    pdf = pd.DataFrame(proba, columns=cls.race)
    pdf.set_index(df[nn].index, inplace=True)

    rdf = pd.concat([df, pdf], axis=1)

    return rdf
