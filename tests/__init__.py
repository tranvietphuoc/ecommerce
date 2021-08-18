from dataclasses import dataclass, field
from typing import List


def test():
    print("test")


@dataclass(frozen=True, order=True)
class Test:
    info: str = field(default='')
    subject: List[str] = field(default=list)

    def test(self):
        print(self)
        print(self)
        return
