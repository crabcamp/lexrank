from lexrank.utils.text import tokenize


def test_tokenize():
    raw_text = 'Contact Information\n' \
        'We\'re here to help!\n' \
        'Call us: 1.888.676.2660 24/7\n' \
        'Email us: cs@6pm.com\n' \
        '(When sending us an email, please do so from the email address ' \
        'on your 6pm account or it may result in a delay of assistance.)\n' \
        'Questions? Select a topic to learn more!\n' \
        'Frequently Asked Questions\n' \
        'Shipping & Delivery\n' \
        'Returns\n'

    tokens_all = [
        'contact', 'information', 'were', 'here', 'to', 'help', 'call', 'us',
        '1', '888', '676', '2660', '24', '7', 'email', 'us', 'cs@6pm.com',
        'when', 'sending', 'us', 'an', 'email', 'please', 'do', 'so', 'from',
        'the', 'email', 'address', 'on', 'your', '6pm', 'account', 'or', 'it',
        'may', 'result', 'in', 'a', 'delay', 'of', 'assistance', 'questions',
        'select', 'a', 'topic', 'to', 'learn', 'more', 'frequently', 'asked',
        'questions', 'shipping', 'delivery', 'returns',
    ]
    tokens_nonum = [
        token for token in tokens_all
        if token not in {'1', '888', '676', '2660', '24', '7', '6pm'}
    ]
    tokens_nonum_noemail = [
        token for token in tokens_nonum if token not in {'cs@6pm.com'}
    ]
    tokens_rude = [
        token for token in tokens_nonum if token not in {'please', 'help'}
    ]

    actual_tokens_all = tokenize(
        raw_text, {}, keep_emails=True, keep_numbers=True,
    )
    actual_tokens_nonum = tokenize(
        raw_text, {}, keep_emails=True, keep_numbers=False,
    )
    actual_tokens_nonum_noemail = tokenize(
        raw_text, {}, keep_emails=False, keep_numbers=False,
    )
    actual_tokens_rude = tokenize(
        raw_text, {'please', 'help'}, keep_emails=True, keep_numbers=False,
    )

    assert actual_tokens_all == tokens_all
    assert actual_tokens_nonum == tokens_nonum
    assert actual_tokens_nonum_noemail == tokens_nonum_noemail
    assert actual_tokens_rude == tokens_rude
