import pytest
import os
from unittest import mock
from data_structure.word_trie import WordTrie
from text_processor.text_processor import TextDatasetProcessor


@mock.patch('builtins.open', new_callable=mock.mock_open, read_data="how to learn python\nhow to sew\nlearn to cook\n")
def test_process_file(mock_open):
    word_trie = WordTrie()
    processor = TextDatasetProcessor(dataset_directory='Dataset')
    processor._process_file('Dataset/subfolder1/file1.txt', word_trie=word_trie)

    assert word_trie.search('how to') == [('Dataset/subfolder1/file1.txt', 1), ('Dataset/subfolder1/file1.txt', 2)]


@mock.patch('builtins.open', new_callable=mock.mock_open, read_data="test content\nnext line\nanother test\n")
@mock.patch('os.walk')
def test_process_files(mock_os_walk, mock_open):
    word_trie = WordTrie()
    processor = TextDatasetProcessor(dataset_directory='Dataset')

    mock_os_walk.return_value = [
        ('Dataset', ['subfolder1', 'subfolder2'], ['file5.txt', 'file6.txt']),
        ('Dataset/subfolder1', [], ['file1.txt']),
        ('Dataset/subfolder2', [], ['file2.txt', 'file3.txt'])
    ]

    processor.process_files(word_trie=word_trie)

    expected = {
        (os.path.normpath('Dataset/file5.txt'), 1),
        (os.path.normpath('Dataset/file6.txt'), 1),
        (os.path.normpath('Dataset/subfolder1/file1.txt'), 1),
        (os.path.normpath('Dataset/subfolder2/file2.txt'), 1),
        (os.path.normpath('Dataset/subfolder2/file3.txt'), 1),
    }

    result = word_trie.search('test content')
    result_normalized = set([(os.path.normpath(path), line) for path, line in result])

    assert result_normalized == expected


def test_empty_directory():
    word_trie = WordTrie()
    processor = TextDatasetProcessor(dataset_directory='Dataset')

    with mock.patch('os.walk') as mock_os_walk:
        mock_os_walk.return_value = []
        processor.process_files(word_trie=word_trie)

    assert word_trie.search('test') == []


@mock.patch('builtins.open', new_callable=mock.mock_open, read_data="line one\nline two\n")
def test_insert_multiple_sentences(mock_open):
    word_trie = WordTrie()
    processor = TextDatasetProcessor(dataset_directory='Dataset')

    processor._process_file('Dataset/subfolder/file1.txt', word_trie=word_trie)

    assert word_trie.search('line') == [
        ('Dataset/subfolder/file1.txt', 1),
        ('Dataset/subfolder/file1.txt', 2),
    ]
    assert word_trie.search('one') == [('Dataset/subfolder/file1.txt', 1)]
    assert word_trie.search('two') == [('Dataset/subfolder/file1.txt', 2)]
