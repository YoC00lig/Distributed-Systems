import ray
from NameNode import NameNode
from Constants import PINK
import os

if __name__ == "__main__":
     ray.shutdown()
     ray.init()
     
     name_node = NameNode.remote()
     
     while True:
        input_text = input('> ')
        if len(input_text) < 1: continue
          
        parsed_input = input_text.split(' ')
        command = parsed_input[0]

        if command == 'exit': break
        elif command == 'upload':
            if len(parsed_input) >= 3: name_node.upload_artifact.remote(parsed_input[1], " ".join(parsed_input[2:]))
        elif command == 'update':
            if len(parsed_input) >= 3: name_node.update_artifact.remote(parsed_input[1], " ".join(parsed_input[2:]))
        elif command == 'get':
            if len(parsed_input) >= 2:
                result = ray.get(name_node.get_artifact.remote(parsed_input[1]))
                print(f"{PINK} NAME: {parsed_input[1]} CONTENT: {result}")