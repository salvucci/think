import re


def text_to_words(text):
    text = str(text)
    text = re.sub(r"[']", "", text)
    text = re.sub(r"[^A-Za-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip().split()


def count_syllables(text):
    text = text.strip().lower()
    count = 0
    for word in text_to_words(text):
        word = re.sub(r"^([^aeiouy]*)e$", "$1 ee", word)
        word = re.sub(r"([^aeiouy])le$", "$1 ul", word)
        word = re.sub(r"be$", " bee", word)
        word = re.sub(r"es?$", "", word)
        word = re.sub(r"ing$", " ing", word)
        word = re.sub(r"([aeiouy][^aeiouy])ed$", "$1d", word)
        word = re.sub(r"([^cs])ia", "$1i a", word)
        word = re.sub(r"([^s])ea$", "$1e a", word)
        word = re.sub(r"qu", "q", word)
        word = re.sub(r"ienc", "i enc", word)
        word = re.sub(r"ue", "u e", word)
        word = re.sub(r"ual", "u al", word)
        count += len(re.findall(r"[aeiouy]+", word))
    return count
