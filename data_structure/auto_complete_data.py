from dataclasses import dataclass


@dataclass
class AutoCompleteData:
    """Represents the data for an autocomplete suggestion.

    Attributes:
        completed_sentence (str): The suggested complete sentence.
        source_text (str): The source text from which the suggestion was derived.
        offset (int): The index offset in the source text where the suggestion starts.
        score (int): The score of the suggestion based on relevance.
    """
    completed_sentence: str
    source_text: str
    offset: int
    score: int