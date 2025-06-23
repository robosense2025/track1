GPU_NUM=$1

vllm serve "Qwen/Qwen2.5-VL-7B-Instruct" \
    --allowed-local-media-path / \
    --tensor-parallel-size $GPU_NUM