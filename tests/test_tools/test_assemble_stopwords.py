from lexrank.tools.assemble_stopwords import assemble_stopwords


def test_assemble_stopwords():
    try:
        assemble_stopwords()
        raise AssertionError

    except OSError:
        pass
