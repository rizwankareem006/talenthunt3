from collections.abc import Iterator
from django.contrib.auth.models import User
from Details.models import Teams

class UserIterator(Iterator):

    def __init__(self, collection, reverse: bool = False) -> None:
        self._collection = collection
        self._reverse = reverse
        self._position = -1 if reverse else 0

    def __next__(self):
        """
        The __next__() method must return the next item in the sequence. On
        reaching the end, and in subsequent calls, it must raise StopIteration.
        """
        try:
            value = self._collection[self._position].get_full_name()
            self._position += -1 if self._reverse else 1
        except IndexError:
            raise StopIteration()

        return value

class TeamIterator(Iterator):

    def __init__(self, collection, reverse: bool = False) -> None:
        self._collection = collection
        self._reverse = reverse
        self._position = -1 if reverse else 0

    def __next__(self):
        """
        The __next__() method must return the next item in the sequence. On
        reaching the end, and in subsequent calls, it must raise StopIteration.
        """
        try:
            value = self._collection[self._position].teamname
            self._position += -1 if self._reverse else 1
        except IndexError:
            raise StopIteration()

        return value

# if __name__ == "__main__":
#     users = User.objects.all()
#     user_iterator = UserIterator(users)
#     for i in user_iterator:
#         print(i)