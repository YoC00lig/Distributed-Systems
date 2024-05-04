#!/bin/bash

# I truly detest python import system
# https://github.com/protocolbuffers/protobuf/issues/1491#issuecomment-1463981985

mkdir -p ./generated
printf "import sys\nfrom pathlib import Path\nsys.path.append(str(Path(__file__).parent))" > ./generated/__init__.py
python3 -m grpc_tools.protoc \
          -I../protos \
          --python_out=./generated \
          --pyi_out=./generated \
          --grpc_python_out=./generated \
          ../protos/shopping.proto
