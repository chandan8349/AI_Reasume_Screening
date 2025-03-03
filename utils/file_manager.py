import os

def save_text_to_file(text, filepath):
    """
    Saves the provided text to the specified filepath.

    Parameters:
        text (str): The text content to be saved.
        filepath (str): The destination file path where text will be saved.
    """
    # Ensure that the directory exists; if not, create it
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(text)

def load_text_from_file(filepath):
    """
    Loads and returns text from the specified filepath.

    Parameters:
        filepath (str): The path of the file to load text from.

    Returns:
        str: The text content read from the file.

    Raises:
        FileNotFoundError: If the specified file does not exist.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"{filepath} does not exist.")
    
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()
