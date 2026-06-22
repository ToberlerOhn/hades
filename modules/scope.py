# ---------------------------------------------------------------------------- #
#                                    Imports                                   #
# ---------------------------------------------------------------------------- #

from typing import Any as any

# ---------------------------------------------------------------------------- #
#                              Environment / Scope                             #
# ---------------------------------------------------------------------------- #

class Scope:
    
    def __init__(self, parent: Scope | None = None):
        self.variables: dict[str, any] = {}
        self.parent = parent

    def get(self, name: str) -> any:
        if name in self.variables:
            return self.variables[name]
        if self.parent is not None:
            return self.parent.get(name)
        raise KeyError(name)
    
    def set(self, name: str, value: any) -> None:
        if name in self.variables:
            self.variables[name] = value
            return
        if self.parent is not None:
            self.parent.set(name, value)
            return
        raise KeyError(name)

    def declare(self, name: str, value: any) -> None:
        self.variables[name] = value

    def has(self, name: str) -> bool:
        return name in self.variables