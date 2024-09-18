from data_structure.word_trie import WordTrie
from data_structure.auto_complete_data import AutoCompleteData
from text_processor.text_processor import TextDatasetProcessor
from utils.consts import MAX_SUGGESTIONS
from utils.functions import get_line_at_index, find_match_indices_by_words
from typing import List


class CompletionCoordinator:

    def __init__(self, dataset_dir: str, max_matches: int = MAX_SUGGESTIONS) -> None:
        self.trie = WordTrie(root=None, max_matches=max_matches)
        self.processor = TextDatasetProcessor(dataset_dir)
    
    def build_trie(self) -> None:
        self.processor.process_files(self.trie)
    
    def get_suggestions(self, prompt: str) -> List[AutoCompleteData]:
        suggestions = self.trie.search(prompt)
        results = []
        for suggestion in suggestions:
            line = get_line_at_index(*suggestion)
            line_range = find_match_indices_by_words(line, prompt)
            if line_range:
                data = AutoCompleteData(completed_sentence=line[line_range[0]:],
                                        source_text=suggestion[0],
                                        offset=suggestion[1],
                                        score=self.trie.matcher.calculate_score(prompt, line[line_range[0]:line_range[1]]))
                results.append(data)
        
        return results
    


