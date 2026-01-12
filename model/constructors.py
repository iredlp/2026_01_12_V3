from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Set

@dataclass
class Constructors:
    constructorId: int
    constructorRef: str
    name: str
    nationality: str
    url: str

    oldest_driver_dob:Optional[int] = None  #valore opzionale

    list_piloti:  list = field(default_factory=list)
    #popolarita: set = field(default_factory=set)
   # popolarita: int = 0

    def __hash__(self):
        return hash(self.constructorId)

    def __eq__(self, other):
        if isinstance(other, Constructors):
            return self.constructorId == other. constructorId
        return False

    def __repr__(self):
        return (f"{self.name} ({self. constructorId}) ")
                # if self.year is not None else 'N/D'})")