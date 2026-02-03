LANG_TO_NAME = {
    "en": "English",
    "cs": "Czech",
    "ja": "Japanese",
    "cs_CZ": "Czech",
    "de_DE": "German",
    "uk_UA": "Ukrainian",
    "ar_EG": "Arabic",
    "bho_IN": "Bhojpuri",
    "et_EE": "Estonian",
    "is_IS": "Icelandic",
    "it_IT": "Italian",
    "ja_JP": "Japanese",
    "ko_KR": "Korean",
    "mas_KE": "Maasai",
    "ru_RU": "Russian",
    "sr_Cyrl_RS": "Serbian (Cyrillic)",
    "zh_CN": "Chinese",
}

MODEL_VLLM_PARAMS = {
    "Qwen/Qwen3-1.7B": {
        "gpu-memory-utilization": 0.85,
        "max-num-seqs": 1,
        "max-model-len": 4096,
    },
    "swiss-ai/Apertus-8B-Instruct-2509": {
        "gpu-memory-utilization": 0.85,
        "max-num-seqs": 1,
        "max-model-len": 4096,
    },
    "HuggingFaceTB/SmolLM3-3B": {
        "gpu-memory-utilization": 0.85,
        "max-num-seqs": 1,
        "max-model-len": 4096,
    },
}
