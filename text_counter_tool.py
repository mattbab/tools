def count_elements(text):
    """
    This function accepts a string and returns the number of characters, words, sentences 
    and paragraphs in the string.

    :param text: str - The input string to be analyzed.
    :return: tuple - A tuple containing the number of characters, words, sentences, and paragraphs.
    """
    # Initialize counters
    num_chars = 0
    num_words = 0
    num_sentences = 0
    num_paragraphs = 0

    # Split text into paragraphs
    paragraphs = text.split('\n')
    for p in paragraphs:
        if p != '':  # Ignore empty lines
            num_paragraphs += 1

            # Count words and sentences in each paragraph
            words = p.split()
            num_words += len(words)
            num_sentences += len(
                p.split('.')) - 1  # Assuming a sentence ends with '.'

    num_chars = sum([len(w) for w in text.split('\n')])

    return (num_chars, num_words, num_sentences, num_paragraphs)


def setup(ToolManager):
    """
    This function is used to set up the tool by adding your function to the ToolManager.

    :param ToolManager: ToolManager - The ToolManager object that this function will be added to.
    """
    ToolManager.add(count_elements)
