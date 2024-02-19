def count_elements(text):
    """
    This function accepts a string and returns the number of characters, words, sentences, 
    and paragraphs in the string.

    :param text: str - The input string.
    :return: tuple - A tuple containing the number of characters, words, sentences, and paragraphs.
    """
    # Initialize counters for each element
    num_chars = 0
    num_words = 0
    num_sentences = 0
    num_paragraphs = 0

    # Split the text into paragraphs
    paragraphs = text.split('\n')

    # Iterate over each paragraph
    for para in paragraphs:
        # Count characters, words and sentences in this paragraph
        num_chars += len(para)
        num_words += len(para.split())
        num_sentences += len(para.split('. '))

    # Return the counts as a tuple
    return num_chars, num_words, num_sentences, num_paragraphs


def setup(ToolManager):
    """
    This function is part of the ToolManager and includes calls to the primary function in the code.
    
    :param ToolManager: ToolManager - An instance of the ToolManager class.
    """
    # Add your function to the ToolManager
    ToolManager.add(count_elements)


def main():
    """
    This is a test for the count_elements function.
    """
    print(count_elements("Hello, world! This is a test.\nAnother paragraph."))


if __name__ == "__main__":
    main()
