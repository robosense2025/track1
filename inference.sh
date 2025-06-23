MODEL_PATH="Qwen/Qwen2.5-VL-7B-Instruct"
INPUT_DATA="robosense_track1_release_convert.json"
OUTPUT_DIR="outputs"
MAX_MODEL_LEN=8192
NUM_IMAGES_PER_PROMPT=6
TEMPERATURE=0.2
TOP_P=0.2
MAX_TOKENS=512
PORT=8000

mkdir -p ${OUTPUT_DIR}

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_FILE="${OUTPUT_DIR}/inference_results_${TIMESTAMP}.json"

echo "Running inference..."
python toolkits/inference.py \
    --model ${MODEL_PATH} \
    --data ${INPUT_DATA} \
    --output ${OUTPUT_FILE} \
    --max_model_len ${MAX_MODEL_LEN} \
    --num_images_per_prompt ${NUM_IMAGES_PER_PROMPT} \
    --temperature ${TEMPERATURE} \
    --top_p ${TOP_P} \
    --max_tokens ${MAX_TOKENS} \
    --api_base "http://localhost:${PORT}/v1"