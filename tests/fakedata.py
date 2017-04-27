import random
import string
from faker import Faker
from faker.providers import BaseProvider


fake = Faker()


class RandomLengthStringProvider(BaseProvider):
    MIN_CHAR_DEFAULT = 3
    MAX_CHAR_DEFAULT = 100

    def __init__(self, min_chars=None, max_chars=None):
        self._min_chars = min_chars if min_chars else self.MIN_CHAR_DEFAULT
        self._max_chars = max_chars if max_chars else self.MAX_CHAR_DEFAULT

    def __call__(self):
        length = random.randint(self._min_chars, self._max_chars)
        random_string = [random.choice(string.ascii_letters) for i in xrange(length)]
        return ''.join(random_string)


class RandomIntegerProvider(BaseProvider):
    def __init__(self, minimum, maximum):
        self._minimum = minimum
        self._maximum = maximum

    def __call__(self):
        return random.randint(self._minimum, self._maximum)


class RandomSelectionProvider(BaseProvider):
    def __init__(self, sequence):
        self._sequence = sequence

    def __call__(self):
        return random.choice(self._sequence)


randstr = RandomLengthStringProvider()
randint = RandomIntegerProvider(1, 1000)
randprovider = RandomSelectionProvider(['google', 'twitter', 'facebook'])
