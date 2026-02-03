
function sbatch_gpu_big() {
    JOB_NAME=$1;
    JOB_WRAP=$2;
    mkdir -p logs

    sbatch \
        -J $JOB_NAME --output=logs/%x.out --error=logs/%x.err \
        --gpus=1 --gres=gpumem:40g \
	--mail-type END \
	--mail-user vilem.zouhar@gmail.com \
        --ntasks-per-node=1 \
        --cpus-per-task=6 \
        --mem-per-cpu=8G --time=1-0 \
        --wrap="$JOB_WRAP";
}


sbatch_gpu_big "translate_qwen3-1.7b" "python3 scripts/03-translate_wmt.py --model Qwen/Qwen3-1.7B"


function sbatch_gpu_big_short() {
    JOB_NAME=$1;
    JOB_WRAP=$2;
    mkdir -p logs

    sbatch \
        -J $JOB_NAME --output=logs/%x.out --error=logs/%x.err \
        --gpus=1 --gres=gpumem:40g \
	--mail-type END \
	--mail-user vilem.zouhar@gmail.com \
        --ntasks-per-node=1 \
        --cpus-per-task=6 \
        --mem-per-cpu=8G --time=0-4 \
        --wrap="$JOB_WRAP";
}


sbatch_gpu_big_short "translate_qwen3-1.7b" "python3 scripts/03-translate_wmt.py --model Qwen/Qwen3-1.7B"

function sbatch_gpu() {
    JOB_NAME=$1;
    JOB_WRAP=$2;
    mkdir -p logs

    sbatch \
        -J $JOB_NAME --output=logs/%x.out --error=logs/%x.err \
        --gres=gpumem:20g --gpus=rtx_4090:1 \
	--mail-type END \
	--mail-user vilem.zouhar@gmail.com \
        --ntasks-per-node=1 \
        --cpus-per-task=6 \
        --mem-per-cpu=8G --time=1-0 \
        --wrap="$JOB_WRAP";
}
sbatch_gpu "translate_apertus_8b_instruct_2509" "python3 scripts/03-translate_wmt.py --model swiss-ai/Apertus-8B-Instruct-2509"


sbatch_gpu "translate_qwen3-1.7b" "python3 scripts/03-translate_wmt.py --model Qwen/Qwen3-1.7B"