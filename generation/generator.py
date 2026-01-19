import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig
)
from generation.prompts import BASE_PROMPT


class Generator:
    def __init__(self, model_name="mistralai/Mistral-7B-Instruct-v0.2"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # 🔹 Quantization config (CRITICAL)
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
        )

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            quantization_config=bnb_config,   # ✅ ADD THIS
            device_map="auto",                # ✅ keep auto
            max_memory={
                0: "6GB",     # GPU (leave headroom)
                "cpu": "10GB"
            }
        )

        # Optional but good
        self.model.eval()

    def generate(self, question, retrieved_chunks, max_new_tokens=256):
        context = "\n\n".join(c.text for c in retrieved_chunks)

        prompt = BASE_PROMPT.format(
            context=context,
            question=question
        )

        inputs = self.tokenizer(
        prompt,
        return_tensors="pt"
        )

        inputs = {k: v.to(self.model.device) for k, v in inputs.items()}

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            use_cache=True
        )

        return self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )
