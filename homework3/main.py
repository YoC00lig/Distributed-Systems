import ray
from NameNode import NameNode
from Constants import PINK, BLUE, GREEN, ORANGE, DEFAULT
from typing import List

def handle_operation(command : str, args : List) -> None:
    number_of_args = len(args)

    if command == 'upload' and number_of_args  >= 3:
        name_node.upload_artifact.remote(args[1], " ".join(args[2:]))

    elif command == 'update' and number_of_args  >= 3:
        name_node.update_artifact.remote(args[1], " ".join(args[2:]))

    elif command == 'get' and number_of_args  >= 2:
        result = ray.get(name_node.get_artifact.remote(args[1]))
        if result != "": print(f"{PINK} NAME: {args[1]} CONTENT: {result}")

    elif command == 'delete' and number_of_args  >= 2:
        name_node.delete_artifact.remote(args[1])

    elif command == 'list' and number_of_args  == 1:
        result = ray.get(name_node.list_all.remote())
        print(f"{PINK}LIST:")
        for storage_node in result:
            print(f"{PINK}----------------------------------")
            print(f"{BLUE}Node PID: {storage_node[0]}")
            for artifact, chunks in storage_node[1].items():
                print (f"{GREEN}Artifact: {artifact}")
                for chunk_id, chunk_content in chunks.items():
                    print(f"{PINK}Chunk ID: {chunk_id} | Chunnk Content: {chunk_content}")
        print(f"{PINK}----------------------------------")

    else:
        print(f"{ORANGE}Unknown command.")

if __name__ == "__main__":
     ray.shutdown()
     ray.init()
     name_node = NameNode.options(max_concurrency=2).remote()
     while True:
        user_input = input(f'{PINK}CLIENT: {DEFAULT}')
        if len(user_input) < 1: continue
        args = user_input.split(' ')
        command = args[0]
        if command == 'quit':
            name_node.exit.remote()
            break
        else: 
            handle_operation(command, args)
