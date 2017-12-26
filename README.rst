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

In the following example we use
`BBC news dataset <http://mlg.ucd.ie/files/datasets/bbc-fulltext.zip>`_
as a corpus of documents.

.. code-block:: python

    from lexrank import STOPWORDS, LexRank
    from path import Path

    documents = []
    documents_dir = Path('bbc/politics')

    for file_path in documents_dir.files('*.txt'):
        with file_path.open(mode='rt', encoding='utf-8') as fp:
            documents.append(fp.readlines())

    lxr = LexRank(documents, stopwords=STOPWORDS['en'])

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

    # get summary with classical LexRank algorithm
    summary = lxr.get_summary(sentences, summary_size=2, threshold=.1)
    print(summary)

    # ['Mr Osborne said the coalition government was planning to change the tax '
    #  'system "to make it fairer for people on low and middle incomes", and '
    #  'undertake "long-term structural reform" of the banking sector, education and '
    #  'the welfare state.',
    #  'The BBC understands that as chancellor, Mr Osborne, along with the Treasury '
    #  'will retain responsibility for overseeing banks and financial regulation.']


    # get summary with continuous LexRank
    # default value for 'summary_size' is 1 and 'threshold' is not referenced
    summary_cont = lxr.get_summary(sentences, discretize=False)
    print(summary_cont)

    # ['The BBC understands that as chancellor, Mr Osborne, along with the Treasury '
    #  'will retain responsibility for overseeing banks and financial regulation.']

    # get LexRank scores for sentences
    # when 'normalize' is True, all the scores are divided by the maximal one
    # 'fast_power_method' speeds up the calculation, but requires more memory
    scores_cont = lxr.rank_sentences(
        sentences,
        discretize=False,
        normalize=True,
        fast_power_method=False,
    )
    print(scores_cont)

    # [0.9193576793242669,
    #  0.7602507729889821,
    #  0.939832498150748,
    #  0.6985590010158195,
    #  0.6844271578353363,
    #  1.0,
    #  0.9036049881647119]

Stop words for 22 languages are included into the package. To define your own mapping of stop words, prepare text files with utf-8 encoding where words are separated by newlines. Then use the command

.. code-block:: bash

    assemble_stopwords --source_dir directory_with_txt_files

that replaces the default mapping. Note that names of .txt files are used as keys in `STOPWORDS` dictionary.

Tests
-----

Tests are not supplied with the package, to run them you need to clone the repository and install additional dependencies.

.. code-block:: bash

    # ensure virtualenv is activated
    make install-dev

Run linter and tests

.. code-block:: bash

    make lint
    make test


References
----------

Güneş Erkan and Dragomir R. Radev:
`LexRank: Graph-based Lexical Centrality as Salience in Text Summarization
<http://www.jair.org/papers/paper1523.html>`_.
