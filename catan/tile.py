class Tile:
    def __init__(self, id: int, type: str, value: int, neighbours_id: list, is_inland: bool = False):
        self.type = type
        self.value = value
        self.neighbours_id = neighbours_id
        self.id = id
        self.is_inland = is_inland
    
    def __repr__(self):
        return f"Typ: {self.type}, hodnota: {self.value}, sousedi: {self.neighbours_id}, id: {self.id}"

