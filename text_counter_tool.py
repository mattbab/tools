def count_characters(input_string: str) -> dict:
    """
    This function accepts a string and returns a dictionary with 
    the number of characters, words, sentences, and paragraphs.
    
    :param input_string: The string to be analyzed.
    :type input_string: str
    :return: A dictionary containing the count of characters, words, sentences, and paragraphs.
    :rtype: dict
    """
    # Initialize counters for each type of element in the string
    char_count = 0
    word_count = 0
    sentence_count = 0
    para_count = 0

    # Split the input string into paragraphs, sentences and words
    paragraphs = input_string.split("\n")
    for para in paragraphs:
        if para != "":
            sentences = para.split(". ")
            for sentence in sentences:
                if sentence != "":
                    words = sentence.split(" ")
                    word_count += len(words)
                    char_count += sum([len(word) for word in words])
                    sentence_count += 1
            para_count += 1

    return {
        "characters": char_count,
        "words": word_count,
        "sentences": sentence_count,
        "paragraphs": para_count
    }


def setup(ToolManager):
    """
    This function is used to add your function (count_characters) 
    into the ToolManager.
    
    :param ToolManager: The ToolManager object that will contain your function.
    :type ToolManager: class
    """
    ToolManager.add(count_characters)


def main():
    input_string = "This is a sample string.\nIt has multiple paragraphs, sentences and words."
    print(count_characters(input_string))


if __name__ == '__main__':
    main()
