lexrank
=======

:info: LexRank algorithm for text summarization

.. image:: https://travis-ci.org/wikibusiness/lexrank.svg?branch=dev
    :target: https://travis-ci.org/wikibusiness/lexrank

Installation
------------

.. code-block:: shell

    # not implemented

Usage
-----

Simple example
~~~~~~~~~~~~~~

In the following example we use
`BBC news dataset <http://mlg.ucd.ie/files/datasets/bbc-fulltext.zip>`_
as a corpus of documents:

.. code-block:: python

    from lexrank import LexRank
    from lexrank.mappings import STOPWORDS
    from path import Path

    documents = []
    documents_dir = Path('bbc/politics')

    for file in documents_dir.files('*.txt'):
        with file.open(mode='rt', encoding='utf-8') as fp:
            documents.append(fp.readlines())

    lexrank = LexRank(documents, stopwords=STOPWORDS['en'])

    sentences = [
        'One of David Cameron\'s closest friends and Conservative allies, '
        'George Osborne rose rapidly after becoming MP for Tatton in 2001.',

        'Michael Howard promoted him from shadow chief secretary to the '
        'Treasury to shadow chancellor in May 2005, at the age of 34.',

        'Mr Osborne took a key role in the election campaign and has been at '
        'the forefront of the debate on how to deal with the recession and '
        'the UK\'s spending deficit.',

        'Even before Mr Cameron became leader the two were being likened to '
        'Labour\'s Blair/Brown duo. The two have emulated them by becoming '
        'prime minister and chancellor, but will want to avoid the spats.',

        'Before entering Parliament, he was a special adviser in the '
        'agriculture department when the Tories were in government and later '
        'served as political secretary to William Hague.',

        'The BBC understands that as chancellor, Mr Osborne, along with the '
        'Treasury will retain responsibility for overseeing banks and '
        'financial regulation.',

        'Mr Osborne said the coalition government was planning to change the '
        'tax system \"to make it fairer for people on low and middle '
        'incomes\", and undertake \"long-term structural reform\" of the '
        'banking sector, education and the welfare state.',
    ]

    summary = lexrank.get_summary(sentences, discretize=False)
    print(summary)

Module contents
~~~~~~~~~~~~~~~

lexrank.\ **LexRank**\ (*documents, stopwords=None, keep_numbers=False,
keep_emails=False, include_new_words=True,*)
:Returns an object for ranking sentences using given 'documents' (a sequence of lists of sentences).

References
----------

Güneş Erkan and Dragomir R. Radev:
`LexRank: Graph-based Lexical Centrality as Salience in Text Summarization
<http://www.jair.org/papers/paper1523.html>`_.
