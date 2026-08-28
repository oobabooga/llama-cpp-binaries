# llama-cpp-binaries

llama.cpp server in a Python wheel.

## Installation

```
git clone --recurse-submodules https://github.com/oobabooga/llama-cpp-binaries
cd llama-cpp-binaries
CMAKE_ARGS="-DGGML_CUDA=ON" pip install -v .
```

Replace `-DGGML_CUDA=ON` with the appropriate flag for your GPU, or remove it if you don't have a GPU.

## Usage

```python
import subprocess
import llama_cpp_binaries

server_path = llama_cpp_binaries.get_binary_path()
process = subprocess.Popen([server_path, "--help"])
```

For a more detailed example, consult: https://github.com/oobabooga/textgen/blob/main/modules/llama_cpp_server.py
