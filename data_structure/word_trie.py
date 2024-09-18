from data_structure.node import Node
from text_processor.string_matcher import StringMatcher
from utils.functions import normalize_text
from utils.consts import MAX_SUGGESTIONS, Typo
from typing import List, Tuple


class WordTrie:
    """Represents a trie data structure for storing and searching sentences.

    Attributes:
        root (Node): The root node of the trie.
        max_matches (int): The maximum number of matches to return.
        matcher (StringMatcher): An instance of StringMatcher for handling typos.
    """
    def __init__(self, root: Node = None, max_matches: int = MAX_SUGGESTIONS):
        """Initialize the WordTrie with a root node and maximum number of matches.

        Args:
            root (Node, optional): The root node of the trie. If not provided, a new root node is created.
            max_matches (int, optional): The maximum number of matches to return. Defaults to MAX_SUGGESTIONS.
        """
        self.root: Node = root or Node()
        self.max_matches: int = max_matches
        self.matcher: StringMatcher = StringMatcher()

    def insert_sentence(self, sentence: str, file_name: str, line_number: int) -> None:
        """Insert a sentence into the trie, associating it with a file name and line number.

        Args:
            sentence (str): The sentence to insert.
            file_name (str): The name of the file where the sentence is located.
            line_number (int): The line number where the sentence is located in the file.
        """
        words = normalize_text(sentence).split()
        for i in range(len(words)):
            self._insert_suffix(words[i:], file_name, line_number)

    def search(self, sentence: str) -> List[Tuple[str, int]]:
        """Search for a sentence in the trie, allowing for one character typo.

        Args:
            sentence (str): The sentence to search for.

        Returns:
            List[Tuple[str, int]]: A list of tuples where each tuple contains the file name and line number of matching sentences.
        """
        words = normalize_text(sentence).split()
        node = self.root
        substring = []
        file_data_intersection = None

        for i, word in enumerate(words):
            if word in node.children:
                node = node.children[word]
                substring.append(word)
                file_data = self._get_file_data(node)
            else:
                close_match = None
                for child_word, child_node in node.children.items():
                    typo, _ = self.matcher.check_typo(word, child_word)
                    if typo.value > Typo.MATCH.value:
                        if (i + 1 < len(words) and words[i + 1] in child_node.children) or (i == len(words) - 1):
                            close_match = child_node
                            substring.append(child_word)
                            break
                
                if close_match:
                    node = close_match
                    file_data = self._get_file_data(node)
                else:
                    return []
            
            if file_data_intersection is None:
                file_data_intersection = file_data
            else:
                file_data_intersection = self._intersect_file_data(file_data_intersection, file_data)
            
            if not file_data_intersection:
                return []
            
        return list(file_data_intersection)[:self.max_matches]
    
    def _get_file_data(self, node: Node) -> List[Tuple[str, int]]:
        """Retrieve file data from a given node.

        Args:
            node (Node): The node from which to retrieve file data.

        Returns:
            List[Tuple[str, int]]: A list of tuples containing file names and line numbers associated with the node.
        """
        file_data = []
        for file_name, lines in node.file_data.items():
            for line_number in lines:
                file_data.append((file_name, line_number))
        return file_data
    
    def _intersect_file_data(self, current_data: List[Tuple[str, int]], new_data: List[Tuple[str, int]]) -> List[Tuple[str, int]]:
        """Find the intersection between two lists of file data.

        Args:
            current_data (List[Tuple[str, int]]): The current list of file data.
            new_data (List[Tuple[str, int]]): The new list of file data to intersect with the current data.

        Returns:
            List[Tuple[str, int]]: A list of tuples representing the intersection of the two file data lists.
        """
        return list(set(current_data) & set(new_data))

    def _insert_suffix(self, words: List[str], file_name: str, line_number: int) -> None:
        """Insert a suffix of words into the trie, associating it with a file name and line number.

        Args:
            words (List[str]): The list of words to insert into the trie.
            file_name (str): The name of the file where the words are located.
            line_number (int): The line number where the words are located in the file.
        """
        node = self.root
        for word in words:
            if word not in node.children:
                node.children[word] = Node(word)
            
            node = node.children[word]
            if file_name not in node.file_data:
                node.file_data[file_name] = []
            node.file_data[file_name].append(line_number)
