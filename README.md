# llama-cpp-binaries

llama.cpp server in a Python wheel.

## Installation

```
git clone --recurse-submodules https://github.com/oobabooga/llama-cpp-binaries
cd llama-cpp-binaries
CMAKE_ARGS="-DGGML_CUDA=ON -DGGML_NATIVE=off -DGGML_CUDA_FORCE_MMQ=ON -DCMAKE_CUDA_ARCHITECTURES=all" pip install -v .
```
