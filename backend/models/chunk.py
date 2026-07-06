from pydantic import BaseModel

class Chunk(BaseModel):
    chunk_id:int
    start_char:int
    end_char:int
    char_count:int
    word_count:int
    text: str

