# 🧠 Self-Improving Retrieval-Augmented Generation (RAG) System

> A production-oriented RAG system that **detects its own failures**, **adapts retrieval and prompting strategies**, and **learns from past mistakes** to improve reliability over time.

---

## 🔍 Why This Project Exists

Most RAG systems stop at:

> *“Upload documents → retrieve top-k → generate answer”*

This approach fails silently in production due to:

* poor chunking
* partial retrieval coverage
* hallucinations
* overconfident answers on insufficient context

**This project addresses those failures directly.**

Instead of optimizing for “accuracy”, it optimizes for:

* **faithfulness**
* **grounding**
* **confidence calibration**
* **system-level learning**

---

## ✨ Key Capabilities

### ✅ Multi-Strategy Ingestion & Chunking

* Fixed / sliding window chunking
* Section-aware chunking
* Semantic (sentence-based) chunking
* Strategy metadata preserved per chunk

### ✅ Retrieval with Quality Introspection

* Dense vector retrieval (FAISS + sentence-transformers)
* Retrieval diagnostics:

  * semantic similarity
  * query coverage
  * redundancy

### ✅ GPU-Accelerated Generation

* HuggingFace causal LLMs
* Automatic GPU/CPU offloading
* 4-bit NF4 quantization (BitsAndBytes)
* Memory-aware inference

### ✅ LLM Evaluation (Not Accuracy-Based)

* **Faithfulness**: Is the answer supported by retrieved context?
* **Grounding**: Did retrieval provide usable evidence?
* **Confidence estimation**: Combined signal from retrieval + evaluation

### ✅ Refusal & Safety Logic

* Explicit refusal when confidence is low
* Avoids hallucination instead of masking it

### 🚀 Self-Improving Feedback Loop

* Automatic failure attribution:

  * weak retrieval
  * hallucination risk
  * low confidence
* Strategy retry (chunking / retrieval / prompt)
* Persistent memory of what worked

---

## 🧠 System Architecture

```
User Query
   ↓
Retriever (FAISS)
   ↓
Generator (GPU-backed LLM)
   ↓
Evaluation (Faithfulness, Grounding, Confidence)
   ↓
Failure Attribution
   ↓
Retry Policy (Strategy Switch)
   ↓
Memory Store (Learning)
```

This design mirrors **production LLM reliability pipelines**, not demos.

---

## 🧪 Example Failure Handling

### Query

```
How does bad chunking affect gradient flow in transformer attention layers?
```

### System Behavior

* Retrieval finds chunking-related context
* Coverage is low (no mention of gradients or attention math)
* Faithfulness drops
* Confidence falls below threshold
* **System refuses instead of hallucinating**
* Retry attempts improve retrieval but still refuse if unsupported
* Failure and retry outcome are stored in memory

> Refusal is treated as a **successful outcome**, not a failure.

---

## 📁 Project Structure

```text
self_improving_rag/
├── ingestion/        # document loading & chunking
├── retrieval/        # vector store & quality scoring
├── generation/       # GPU-accelerated LLM inference
├── evaluation/       # faithfulness, grounding, confidence
├── feedback/         # failure attribution & retry logic
├── memory/           # persistent learning store
├── configs/          # YAML-based configuration
├── docs/             # system & design documentation
├── logs/             # ingestion & retrieval logs
└── main_self_improving.py
```

---

## 📊 Evaluation Philosophy

### Why Accuracy Is Not Used

Accuracy requires ground-truth answers, which do not exist for:

* enterprise documents
* evolving policies
* ambiguous queries

### Metrics Used Instead

* **Faithfulness** → answer tokens supported by context
* **Grounding** → retrieval usefulness
* **Coverage** → query intent captured
* **Confidence** → weighted system trust score

This reflects how **real RAG systems are validated in production**.

---

## ⚙️ Performance & Deployment Notes

* 7B-parameter LLMs run locally using:

  * GPU + CPU offloading
  * 4-bit quantization
* HuggingFace Accelerate handles layer placement
* Some parameters may appear on the `meta` device — **expected behavior**
* System is designed to degrade safely under memory pressure

---

## 📌 Known Trade-Offs

* Confidence thresholds are heuristic-based (policy, not training)
* Retry may marginally increase confidence without new information
* Future improvement: stricter refusal gating after retry

These are **documented design decisions**, not bugs.

---

## 🔮 Future Extensions

* Hybrid dense + sparse retrieval
* Clarifying question generation instead of refusal
* Automated evaluation dashboards
* Offline analysis of memory store for policy tuning

---

## 🧑‍💼 Intended Audience

This project is designed for:

* Applied GenAI Engineers
* LLM / RAG Reliability Engineers
* ML Engineers working on production LLM systems

It prioritizes **correctness, transparency, and safety** over flashy demos.

---

## 🏁 Final Note

> This system does not try to be clever.
> It tries to be **trustworthy**.



