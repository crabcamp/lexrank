import regex

EMAIL_REGEX = regex.compile(
    r'[\p{L}0-9]+[\p{L}0-9_.+-]*[\p{L}0-9_+-]+@[\p{L}0-9]+[\p{L}0-9.-]*\.\p{L}+'  # noqa
)
PUNCTUATION_SIGNS = set('.,;:¡!¿?…⋯&‹›«»\"“”[]()⟨⟩}{/|\\')


def clean_text(text, allowed_chars='- ', lowercase=True):
    text = ' '.join(text.split())

    if lowercase:
        text = text.lower()

    text = ''.join(
        ch for ch in text
        if ch in allowed_chars or ch.isalnum()
    )

    return ' '.join(text.split())


def contains_numbers(word):
    return any(ch.isdigit() for ch in word)


def separate_punctuation(text):
    text_punctuation = set(text) & PUNCTUATION_SIGNS

    for ch in text_punctuation:
        text = text.replace(ch, ' ' + ch + ' ')

    return text
