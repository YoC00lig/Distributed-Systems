from Constants import NUMBER_OF_STORAGE_NODES, CHUNK_SIZE, NUMBER_OF_COPIES, BLUE, RED, ORANGE
from StorageNode import StorageNode
import random
import logging
import ray

logging.basicConfig(level=logging.INFO)

@ray.remote
class NameNode():
    def __init__(self) -> None:
        self.artifacts = {}  
        self.storage_nodes = {storage_node_id : StorageNode.remote() for storage_node_id in range(NUMBER_OF_STORAGE_NODES)} 

    def store_artifact_chunk(self, name : str, chunk : str, chunk_id : int) -> None:
        if name not in self.artifacts:
            self.artifacts[name] = {}
        random_storage_nodes = random.sample(list(self.storage_nodes.keys()), NUMBER_OF_COPIES)
        [self.storage_nodes[storage_node_id].store_chunk.remote(name, chunk, chunk_id) for storage_node_id in random_storage_nodes]
        if chunk_id not in self.artifacts[name]:
                self.artifacts[name][chunk_id] = [] 
        [self.artifacts[name][chunk_id].append(storage_node_id) for storage_node_id in random_storage_nodes]

    def upload_artifact(self, name : str, content : str) -> None:
        if name in self.artifacts:
            print(f"{ORANGE}Given artifact already exists")
            return
        self.artifacts[name] = {}
        artifact_chunks = [content[i:i+CHUNK_SIZE] for i in range(0, len(content), CHUNK_SIZE)]
        print(f"{BLUE}Your artifact is divided into chunks")
        for chunk_id, chunk in enumerate(artifact_chunks):
            self.store_artifact_chunk(name=name, chunk=chunk, chunk_id=chunk_id)
        print(f"{BLUE}Your artifact's chunks are distributed into storage nodes")

    def update_artifact(self, name : str, new_content : str) -> None:
        if name not in self.artifacts:
            print(f"{ORANGE}Cannot update the artifact - artifact with the given name was not found.")
            return
          
        artifact_chunks = [new_content[i:i+CHUNK_SIZE] for i in range(0, len(new_content), CHUNK_SIZE)]
        print(f"{BLUE}Your new artifact is divided into chunks")

        for chunk_id, chunk in enumerate(artifact_chunks):
            if chunk_id not in self.artifacts[name]: self.store_artifact_chunk(name=name, chunk=chunk, chunk_id=chunk_id) 
            else:
                for storage_node_id in self.artifacts[name][chunk_id]:
                    self.storage_nodes[storage_node_id].update_chunk.remote(name=name, new_chunk=chunk, chunk_id=chunk_id) 

        chunks_to_remove = [chunk_id for chunk_id in self.artifacts[name] if chunk_id >= len(artifact_chunks)]

        for chunk_id in chunks_to_remove:
            for storage_node_id in self.artifacts[name][chunk_id]:
                self.storage_nodes[storage_node_id].delete_chunk.remote(name, chunk_id)

        for chunk_id in chunks_to_remove:
            self.artifacts[name].pop(chunk_id)
        print(f"{BLUE}Artifact successfully updated")

    def get_artifact(self, name : str) -> str:
        if name not in self.artifacts: 
            print(f"{ORANGE}Cannot get the artifact - artifact with the given name was not found.")
            return 
        content = ""
        for chunk_id, storages in self.artifacts[name].items():
            content += ray.get(self.storage_nodes[storages[0]].get_chunk.remote(name, chunk_id))
        return content