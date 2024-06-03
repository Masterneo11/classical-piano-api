import json

from fastapi import FastAPI, HTTPException
from models import Composer , Piece

app = FastAPI()

with open("composers.json", "r") as f:
    composers_list: list[dict] = json.load(f)

with open("pieces.json", "r") as f:
    piece_list: list[dict] = json.load(f)

composers: list[Composer] = []
for composer in composers_list:
    c = Composer(name=composer["name"],composer_id=composer["composer_id"], home_country=composer["home_country"])
    composers.append(c)

pieces: list[Piece] = []
for piece in piece_list:
    # if Piece is None:
    #     Piece.append(pieces)
    p = Piece(name=piece["name"], alt_name=piece["alt_name"], difficulty=piece["difficulty"], composer_id=piece["composer_id"])
    pieces.append(p)

@app.get("/composers")
async def get_composers() -> list[Composer]:
    return composers

@app.get("/pieces")
async def get_pieces(composer_id: int|None = None):
    piece = []
    if composer_id == None:
        print(pieces)
        return pieces
    
    for index , value in enumerate(pieces):
        if value.composer_id == composer_id:
            piece.append(pieces[index])
    return piece

@app.post("/composers")
async def create_composer(composer_name: str, home_country: str) -> None:
    try:
        new_composer_id = len(composers)
        new_composer_id += 1
    except :
        print("Duplicate ID detected")
    new_composer = Composer(name=composer_name,composer_id=new_composer_id, home_country=home_country)
    composers.append(new_composer)

@app.post("/pieces")
async def create_piece(piece: Piece) -> None:
    composer_id = []
    for index_id in pieces:
        composer_id.append(index_id.composer_id)
    if piece.composer_id not in composer_id:
        raise HTTPException(status_code=400, detail="try another id, the one you entered was not found")
    pieces.append(piece)
    

@app.put("/{composer_id}")
async def update_composer(composer_id: int, update_composer: Composer):
    for index, composer in enumerate(composers):
        if composer.composer_id == composer_id:
            composers[index] = update_composer
            return {"message": "Composer updated successfully"}
    composers.append(update_composer)    
    
@app.put("/pieces/{pieces_id}")
async def update_pieces(piece_name: str, update_piece: Piece) -> None:
    composer_list = []
    for composer_id in pieces:
        composer_list.append(composer_id.composer_id)
    if update_piece.composer_id not in composer_list:
        raise HTTPException(status_code=400, detail="Composer Id non existent")

    updated = False
    for i, piece in enumerate(pieces):
        if piece.name == piece_name:
            pieces[i] = update_piece
            updated = True

    if not updated:
        pieces.append(update_piece)


@app.delete("/composers/{composer_id}")
async def delete_composert(composer_id: int) -> None:
    for i, index in enumerate(composers):
        if composer_id == index.composer_id:
            composers.pop(i)


@app.delete("/pieces/{piece_name}")
async def delete_piece(piece_name: str) -> None:
    for i, index in enumerate(pieces):
        if index.name == piece_name:
            pieces.pop(i)
