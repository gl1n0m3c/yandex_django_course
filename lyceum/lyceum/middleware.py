import re

from django.conf import settings


__all__ = []


RUSSIAN_WORDS_REGULAR = re.compile(r"\b[а-яА-ЯёЁ]+\b")


class MiddlewareReverse:
    REQUEST_COUNTER = 0

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if self.check_need_reverse():
            response.content = self.reverse_russian_words(
                response.content.decode("utf-8"),
            )
        return response

    @classmethod
    def reverse_russian_words(cls, content):
        def reverse_word(match):
            word = match.group()
            return word[::-1]

        content = RUSSIAN_WORDS_REGULAR.sub(reverse_word, content)
        return content.encode("utf-8")

    @classmethod
    def check_need_reverse(cls):
        if not settings.ALLOW_REVERSE:
            return False

        MiddlewareReverse.REQUEST_COUNTER += 1
        if MiddlewareReverse.REQUEST_COUNTER != 10:
            return False
        MiddlewareReverse.REQUEST_COUNTER = 0
        return True
