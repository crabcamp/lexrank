from lexrank.utils.text import tokenize


def test_tokenize():
    text = 'Shipping & Delivery\nContact Information\nWe\'re here to help!'
    result = tokenize(text, {})
    extected = [
        'shipping', 'delivery', 'contact', 'information',
        'were', 'here', 'to', 'help',
    ]

    assert result == extected

    text = 'www.6pm.com\nCall us: 1.888.676.2660 24/7\nEmail us: cs@6pm.com\n'
    result = tokenize(
        text, {}, keep_numbers=True, keep_emails=True, keep_urls=True,
    )
    expected = [
        'www.6pm.com', 'call', 'us', '1', '888', '676', '2660', '24', '7',
        'email', 'us', 'cs@6pm.com',
    ]

    assert result == expected

    text = 'www.6pm.com\nCall us: 1.888.676.2660 24/7\nEmail us: cs@6pm.com\n'
    result = tokenize(
        text, {}, keep_numbers=False, keep_emails=False, keep_urls=False,
    )
    expected = [
        'call', 'us', 'email', 'us',
    ]

    assert result == expected

    text = 'Please, help!'
    result = tokenize(text, {'please'})
    expected = ['help']

    assert result == expected
