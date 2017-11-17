import regex

EMAIL_REGEX = regex.compile(
    r'[\p{L}0-9]+[\p{L}0-9_.+-]*[\p{L}0-9_+-]+@[\p{L}0-9]+[\p{L}0-9.-]*\.\p{L}+'  # noqa
)
PUNCTUATION_SIGNS = set('.,;:¡!¿?…⋯&‹›«»\"“”[]()⟨⟩}{/|\\')


def clean_text(text, allowed_chars='- '):
    text = ' '.join(text.lower().split())
    text = ''.join(ch for ch in text if ch.isalnum() or ch in allowed_chars)

    return text


def contains_letters(word):
    return any(ch.isalpha() for ch in word)


def contains_numbers(word):
    return any(ch.isdigit() for ch in word)


def separate_punctuation(text):
    text_punctuation = set(text) & PUNCTUATION_SIGNS

    for ch in text_punctuation:
        text = text.replace(ch, ' ' + ch + ' ')

    return text


def tokenize(text, stopwords, keep_numbers=False, keep_emails=False):
    if not keep_emails:
        emails = set(EMAIL_REGEX.findall(text))

        for email in emails:
            text = text.replace(email, ' ')

    text = separate_punctuation(text)
    text = clean_text(text)

    if keep_numbers:
        tokens = [
            word for word in text.split()
            if (contains_letters(word) or contains_numbers(word)) and
            word not in stopwords
        ]

    else:
        tokens = [
            word for word in text.split()
            if contains_letters(word) and not contains_numbers(word) and
            word not in stopwords
        ]

    return tokens
