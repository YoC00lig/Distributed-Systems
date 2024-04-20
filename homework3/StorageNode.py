import ray
from Constants import RED
import logging

logging.basicConfig(level=logging.INFO)

@ray.remote
class StorageNode:
    def __init__(self) -> None:
        self.chunks = {}

    def store_chunk(self, name: str, chunk: str, chunk_id: int) -> None:
        if name not in self.chunks:
            self.chunks[name] = {}
        self.chunks[name][chunk_id] = chunk
    
    def update_chunk(self, name: str, new_chunk: str, chunk_id: int) -> None:
        if name not in self.chunks: print(f"{RED}Cannot update the artifact - artifact with the given name was not found in StorageNode.")
        elif chunk_id not in self.chunks[name]: print(f"{RED}Internal error: given StorageNode doesn't storage this chunk")
        self.chunks[name][chunk_id] = new_chunk

    def delete_chunk(self, name: str, chunk_id: int) -> None:
        if name in self.chunks: self.chunks[name].pop(chunk_id)
        else: print(f"{RED}Cannot delete the chunk from given artifact - artifact with the given name was not found in StorageNode.")

    def get_chunk(self, name, chunk_id):
        if name in self.chunks: return self.chunks[name][chunk_id]
        else:
          print(f"{RED} Cannot get given chunk - not found in StorageNode")
          return None
    
    def delete_artifact(self, name):
        if name not in self.chunks: print(f"{RED}Cannot delete given artifact - artifact with the given name was not found in StorageNode.")
        else: self.chunks.pop(name)
        