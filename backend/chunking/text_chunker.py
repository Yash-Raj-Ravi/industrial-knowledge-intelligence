from backend.chunking.models import Chunk

# Use a class rather than a function since we will be reusing the same chunk size and overlap size values
class TextChunker:

    # Constructor
    def __init__(self,chunk_size : int , chunk_overlap : int ):
        if chunk_size <= 0:
            raise ValueError('chunk_size must be positive')

        if chunk_size <=chunk_overlap:
            raise ValueError('chunk_overlap must be smaller than chunk_size')

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    # The Algorithm
    def chunk_text(self,text:str) -> list[Chunk] :
        start=0
        chunks:list[Chunk] = []

        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            chunk_content = text[start:end] # Slicing

            if not chunk_content.strip():
                break

            chunk = Chunk (
                chunk_id = len(chunks) + 1,
                text = chunk_content,
                start_char=start,
                end_char=end,
                char_count=len(chunk_content),
                word_count=len(chunk_content.split())
            )
            chunks.append(chunk)
            start+= self.chunk_size - self.chunk_overlap

        return chunks


