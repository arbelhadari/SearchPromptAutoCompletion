import pytest
from collections import defaultdict
from typing import List, Tuple
from data_structure.word_trie import WordTrie


@pytest.fixture
def sample_trie() -> WordTrie:
    trie = WordTrie()
    
    # Inserting some sample sentences into the trie
    trie.insert_sentence("this is a test", "file1.txt", 1)
    trie.insert_sentence("this is another example", "file1.txt", 2)
    trie.insert_sentence("learning python is fun", "file2.txt", 1)
    trie.insert_sentence("how to cook pasta", "file3.txt", 3)
    trie.insert_sentence("how to learn python", "file3.txt", 4)
    
    return trie


def test_insert_and_search_exact_match(sample_trie):
    """
    Test inserting and searching for an exact match.
    """
    results = sample_trie.search("how to learn")
    expected = [("file3.txt", 4)]
    
    assert results == expected, f"Expected {expected}, got {results}"


def test_search_partial_match(sample_trie):
    """
    Test searching for a partial match of a sentence.
    """
    results = sample_trie.search("learning python")
    expected = [("file2.txt", 1)]
    
    assert results == expected, f"Expected {expected}, got {results}"


def test_search_multiple_results(sample_trie):
    """
    Test searching where multiple results match the query.
    """
    results = sample_trie.search("this is")
    expected = [("file1.txt", 1), ("file1.txt", 2)]
    
    assert results == expected, f"Expected {expected}, got {results}"


def test_search_nonexistent_word(sample_trie):
    """
    Test searching for a word that doesn't exist.
    """
    results = sample_trie.search("nonexistent")
    expected = []
    
    assert results == expected, "Expected an empty list for nonexistent word"


def test_search_limit_results():
    """
    Test limiting search results to 5 entries.
    """
    trie = WordTrie()
    
    # Inserting more than 5 sentences with the same prefix
    trie.insert_sentence("how to code in python", "file1.txt", 1)
    trie.insert_sentence("how to write tests", "file2.txt", 2)
    trie.insert_sentence("how to cook", "file3.txt", 3)
    trie.insert_sentence("how to dance", "file4.txt", 4)
    trie.insert_sentence("how to paint", "file5.txt", 5)
    trie.insert_sentence("how to swim", "file6.txt", 6)
    
    results = trie.search("how to")
    
    # The result should be limited to 5
    assert len(results) == 5, f"Expected 5 results, got {len(results)}"


def test_insert_and_search_different_files(sample_trie):
    """
    Test inserting sentences from different files and retrieving correct file names.
    """
    results = sample_trie.search("how to cook")
    expected = [("file3.txt", 3)]
    
    assert results == expected, f"Expected {expected}, got {results}"


def test_empty_trie_search():
    """
    Test searching in an empty trie should return no results.
    """
    trie = WordTrie()
    results = trie.search("any query")
    assert results == [], "Expected empty list when searching in an empty trie"