def nth_char(words):
    result = ""
    for i, word in enumerate(words):
        if i < len(word):
            result += word[i]
    return result
