import re
from text_processor.string_matcher import StringMatcher
from typing import Optional, Tuple
from utils.consts import Typo


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # punctuation
    text = re.sub(r'\s+', ' ', text)     # extra spaces
    return text.strip()


def get_line_at_index(file_path, n):
    with open(file_path, 'r', encoding='utf-8') as file:
        for current_index, line in enumerate(file, start=1):
            if current_index == n:
                return line.strip()
            

def find_match_indices_by_words(line: str, prompt: str) -> Optional[Tuple[int, int]]:
    matcher = StringMatcher()
    line_words = line.split()
    prompt_words = prompt.split()
    
    for i in range(len(line_words) - len(prompt_words) + 1):
        match_found = True
        typo_used = False

        for j in range(len(prompt_words)):
            word_in_line = line_words[i + j]
            word_in_prompt = prompt_words[j]

            typo_type, _ = matcher.check_typo(word_in_line, word_in_prompt)

            if typo_type == Typo.INVALID:
                match_found = False
                break
            elif typo_type != Typo.MATCH:
                if typo_used:
                    match_found = False
                    break
                typo_used = True
        
        if match_found:
            start_word_index = i
            end_word_index = i + len(prompt_words) - 1

            start_char_index = line.index(line_words[start_word_index])
            end_char_index = line.index(line_words[end_word_index]) + len(line_words[end_word_index]) - 1

            return start_char_index, end_char_index

    return None
