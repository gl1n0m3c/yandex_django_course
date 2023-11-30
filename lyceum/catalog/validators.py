from re import findall

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


__all__ = []


@deconstructible
class ValidateMustContain:
    def __init__(self, *needed_words):
        self.needed_words_arr = {word.lower() for word in needed_words}
        self.joined_words = ", ".join(self.needed_words_arr)

    def __call__(self, value):
        words = set(findall(r"\w+|\W+", value.lower()))
        if not (self.needed_words_arr & words):
            raise ValidationError(
                f"В тексте `{value}` нет слов: {self.joined_words}",
            )
