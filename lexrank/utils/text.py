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


def filter_words(words, stopwords, keep_numbers=False):
    if keep_numbers:
        words = [
            word for word in words
            if (contains_letters(word) or contains_numbers(word)) and
            word not in stopwords
        ]

    else:
        words = [
            word for word in words
            if contains_letters(word) and not contains_numbers(word) and
            word not in stopwords
        ]

    return words


def separate_punctuation(text):
    text_punctuation = set(text) & PUNCTUATION_SIGNS

    for ch in text_punctuation:
        text = text.replace(ch, ' ' + ch + ' ')

    return text


def tokenize(text, stopwords, keep_numbers=False, keep_emails=False):
    tokens = []
    ix = 0

    for found in EMAIL_REGEX.finditer(text):
        part = text[ix: found.start()]
        words = clean_text(separate_punctuation(part)).split()
        words = filter_words(words, stopwords, keep_numbers=keep_numbers)

        email = found.group()
        ix = found.end()

        tokens.extend(words)

        if keep_emails:
            tokens.append(email)

    words = clean_text(separate_punctuation(text[ix:])).split()
    words = filter_words(words, stopwords, keep_numbers=keep_numbers)
    tokens.extend(words)

    return tokens
