from utils.consts import Typo
from typing import Tuple


class StringMatcher:
    """A class for matching strings with typographical error handling.

    Provides methods to check for typos and calculate scores based on mismatches, extra characters, or missing characters.
    """
    @staticmethod
    def penalty_for_mismatch(index: int) -> int:
        """Calculate the penalty for a mismatch based on its position.

        Args:
            index (int): The position of the mismatch in the string.

        Returns:
            int: The penalty score for the mismatch.
        """
        if index == 0:
            return 5
        elif index == 1:
            return 4
        elif index == 2:
            return 3
        elif index == 3:
            return 2
        else:
            return 1
        
    @staticmethod
    def penalty_for_extra_or_missing(index: int) -> int:
        """Calculate the penalty for an extra or missing character based on its position.

        Args:
            index (int): The position of the extra or missing character.

        Returns:
            int: The penalty score for the extra or missing character.
        """
        if index == 0:
            return 10
        elif index == 1:
            return 8
        elif index == 2:
            return 6
        elif index == 3:
            return 4
        else:
            return 2

    def check_typo(self, str_before: str, str_after: str) -> Tuple[Typo, int | None]:
        """Check for typographical errors between two strings and determine the type of error.

        Args:
            str_before (str): The original string.
            str_after (str): The string to compare against the original.

        Returns:
            Tuple[Typo, int | None]: A tuple containing the type of typo and the index where the typo occurred, or None if there's no typo.
        """
        if str_before == str_after:
            return Typo.MATCH, None
        
        # Case 1: One different character (substitution)
        if len(str_before) == len(str_after):
            idx = 0
            found_one = False
            for i in range(len(str_before)):
                if str_before[i] != str_after[i]:
                    if not found_one:
                        found_one = True
                        idx = i
                    else:
                        return Typo.INVALID, None
            return Typo.SWITCH, idx

        # Case 2: One extra character (str_before has one more char)
        if len(str_before) == len(str_after) + 1:
            for i in range(len(str_before)):
                if str_before[:i] + str_before[i+1:] == str_after:
                    return Typo.ADD, i
            return Typo.INVALID, None
        
        # Case 3: One missing character (str_before has one less char)
        if len(str_before) + 1 == len(str_after):
            for i in range(len(str_after)):
                if str_after[:i] + str_after[i+1:] == str_before:
                    return Typo.MISS, i
            return Typo.INVALID, None
        
        # Otherwise, they don't differ by just one character
        return Typo.INVALID, None

    def calculate_score(self, str_before: str, str_after: str) -> int:
        """Calculate the score based on the typographical error between two strings.

        Args:
            str_before (str): The original string.
            str_after (str): The string with a typo to compare against the original.

        Returns:
            int: The calculated score, considering exact matches, typographical errors, and penalties.
        """
        typo, idx = self.check_typo(str_before, str_after)
        
        if typo == Typo.MATCH:
            return 2 * len(str_before)
        elif typo == Typo.SWITCH:
            return 2 * (len(str_before) - 1) - self.penalty_for_mismatch(idx)
        elif typo == Typo.ADD or typo == Typo.MISS:
            return 2 * (len(str_before) - 1) - self.penalty_for_extra_or_missing(idx)
        else:
            return -100
