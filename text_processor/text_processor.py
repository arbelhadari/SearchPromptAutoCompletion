import os
from data_structure.word_trie import WordTrie


class TextDatasetProcessor:
    """A class for processing text files in a dataset directory and inserting their content into a WordTrie.

    Handles traversing directories, reading files, and updating the WordTrie with the contents of each file.
    """
    def __init__(self, dataset_directory: str) -> None:
        """
        Initialize the TextDatasetProcessor with the path to the dataset directory.

        Args:
            dataset_directory (str): The path to the directory containing the text files to be processed.
        """
        self.dataset_directory = dataset_directory

    def process_files(self, word_trie: WordTrie) -> None:
        """
        Traverse the dataset directory and process each text file.

        This method walks through the directory tree, reads each file, and inserts its contents into the provided WordTrie.

        Args:
            word_trie (WordTrie): The WordTrie instance where the content of the files will be inserted.
        """
        for root, _, files in os.walk(self.dataset_directory):
            for file in files:
                self._process_file(os.path.join(root, file), word_trie)

    def _process_file(self, file_path: str, word_trie: WordTrie) -> None:
        """
        Read a single text file and insert its contents into the WordTrie.

        Args:
            file_path (str): The path to the text file to be processed.
            word_trie (WordTrie): The WordTrie instance where the content of the file will be inserted.
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, start=1):
                word_trie.insert_sentence(line.strip(), file_path, line_number)

