lexrank
=======

LexRank algorithm for text summarization

.. image:: https://travis-ci.org/wikibusiness/lexrank.svg?branch=dev
    :target: https://travis-ci.org/wikibusiness/lexrank

.. image:: https://badge.fury.io/py/lexrank.svg
    :target: https://badge.fury.io/py/lexrank

Info
----

LexRank is an unsupervised approach to text summarization based on graph-based centrality scoring of sentences. The main idea is that sentences "recommend" other similar sentences to the reader. Thus, if one sentence is very similar to many others, it will likely be a sentence of great importance. The importance of this sentence also stems from the importance of the sentences "recommending" it. Thus, to get ranked highly and placed in a summary, a sentence must be similar to many sentences that are in turn also similar to many other sentences. This makes intuitive sense and allows the algorithms to be applied to any arbitrary new text.

Installation
------------

.. code-block:: shell

    pip install lexrank

Usage
-----

In the following example we use
`BBC news dataset <http://mlg.ucd.ie/files/datasets/bbc-fulltext.zip>`_
as a corpus of documents.

.. code-block:: python

    from lexrank import LexRank
    from lexrank.mappings.stopwords import STOPWORDS
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
    summary_cont = lxr.get_summary(sentences, threshold=None)
    print(summary_cont)

    # ['The BBC understands that as chancellor, Mr Osborne, along with the Treasury '
    #  'will retain responsibility for overseeing banks and financial regulation.']

    # get LexRank scores for sentences
    # 'fast_power_method' speeds up the calculation, but requires more RAM
    scores_cont = lxr.rank_sentences(
        sentences,
        threshold=None,
        fast_power_method=False,
    )
    print(scores_cont)

    #  [1.0896493024505858,
    #  0.9010711968859021,
    #  1.1139166497016315,
    #  0.8279523250808547,
    #  0.8112028559566362,
    #  1.185228912485382,
    #  1.0709787574388283]

Stop words for 22 languages are included into the package. To define your own mapping of stop words, prepare text files with utf-8 encoding where words are separated by newlines. Then use the command

.. code-block:: bash

    lexrank_assemble_stopwords --source_dir directory_with_txt_files

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
