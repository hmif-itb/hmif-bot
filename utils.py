def text_contains(text, keywords):
    for keyword in keywords:
        if (text.find(keyword) == -1):
            return False
    return True
