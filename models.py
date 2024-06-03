from pydantic import BaseModel

class Composer(BaseModel):
    name: str
    composer_id: int
    home_country: str

class Piece(BaseModel):
    
    name: str
    alt_name: str | None
    difficulty: int
    composer_id: int

class Composer_id(BaseModel):
    "Sergei Rachmaninof" == 1
    "Franz Liszt" == 2
    "Ludwig van Beethoven" == 3
    "Frédéric Chopin" == 4