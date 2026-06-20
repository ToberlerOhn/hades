# ---------------------------------------------------------------------------- #
#                                    Imports                                   #
# ---------------------------------------------------------------------------- #

from typing import Any as any

# ---------------------------------------------------------------------------- #
#                              Environment / Scope                             #
# ---------------------------------------------------------------------------- #

class Scope:
    
    def __init__(self):
        self.variables: dict[str, any] = {}

    def get(self, name: str) -> any:
        if name not in self.variables:
            raise KeyError(name)
        return self.variables[name]
    
    def set(self, name: str, value: any) -> None:
        if name not in self.variables:
            raise KeyError(name)
        self.variables[name] = value

    def declare(self, name: str, value: any) -> None:
        self.variables[name] = value

    def has(self, name: str) -> bool:
        return name in self.variables