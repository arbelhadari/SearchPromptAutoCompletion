from typing import Dict, List
from collections import defaultdict


class Node:
    """Represents a node in a trie data structure.

    Attributes:
        word (str): The word associated with this node. `None` if this node does not represent a complete word.
        children (Dict[str, Node]): A dictionary mapping characters to child nodes.
        file_data (Dict[str, List[int]]): A dictionary mapping file names to lists of line indices where the word occurs.
    """
    def __init__(self, word: str = None) -> None:
        """Initialize a new node in the trie.

        Args:
            word (str, optional): The word associated with this node. Defaults to None.
        """
        self.word: str = word
        self.children: Dict[str, Node] = defaultdict(Node)
        self.file_data: Dict[str, List[int]] = defaultdict(list)