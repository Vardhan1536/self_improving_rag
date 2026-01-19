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

* Explicit distinction between **answer intent** (answer vs refusal) and **confidence**
* Refusal triggered by **semantic insufficiency**, not just low confidence
* Confidence measures trust in the chosen response (including refusal)
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
* System determines the question is **unanswerable from the corpus**
* Answer type is classified as **refusal**
* Retry improves retrieval quality but does not introduce new information
* Confidence increases, indicating higher trust in the refusal
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

# 🔍 Evaluation Metrics

## 1️⃣ Retrieval Similarity (Auxiliary Signal)

### What it measures

The **semantic closeness** between the query and each retrieved chunk in embedding space.

### What it means

* **High similarity ≠ answerable**
* Similarity only tells us *“this text looks related”*, not *“this text is sufficient”*

---

## 2️⃣ Coverage Score (Retrieval Completeness)

### What it measures

How much of the **query’s intent** is actually covered by the retrieved context.

### How it’s computed

* Tokenize the query into key terms
* Tokenize retrieved chunks
* Compute the fraction of query terms appearing in retrieved text

### What it means

| Coverage         | Interpretation                               |
| ---------------- | -------------------------------------------- |
| High (≥ 0.6)     | Retrieval likely contains enough information |
| Medium (0.4–0.6) | Partial answer possible                      |
| Low (< 0.4)      | High hallucination risk                      |

### Why it exists

Coverage detects **silent failures** where:

* similarity is high
* but key aspects of the question are missing

---

## 3️⃣ Redundancy Score (Context Waste)

### What it measures

How repetitive the retrieved chunks are.

### How it’s computed

* Count unique chunk texts
* Compare against total retrieved chunks


### What it means

| Redundancy | Interpretation        |
| ---------- | --------------------- |
| Low        | Diverse evidence      |
| High       | Wasted context window |

### Why it exists

High redundancy:

* wastes token budget
* reduces answer quality
* hides missing information

---

## 4️⃣ Faithfulness Score (Answer ↔ Context Alignment)

### What it measures

How much of the **generated answer is actually supported** by the retrieved context.

### How it’s computed

* Tokenize the generated answer
* Tokenize the retrieved context
* Measure fraction of answer tokens appearing in context

### What it means

| Faithfulness | Interpretation              |
| ------------ | --------------------------- |
| High         | Answer grounded in evidence |
| Medium       | Partial grounding           |
| Low          | Hallucination risk          |

### Why it exists

Faithfulness directly detects **hallucination**, even when:

* the answer *sounds correct*
* the retriever returned something relevant

---

## 5️⃣ Grounding Score (Evidence Availability)

### What it measures

Whether the retrieval step provided **usable, non-trivial evidence**.

### How it’s computed

* Count retrieved chunks with meaningful length/content
* Normalize by total retrieved chunks

### What it means

| Grounding | Interpretation                        |
| --------- | ------------------------------------- |
| High      | Context is usable                     |
| Low       | Retrieval returned noise or fragments |

### Why it exists

Grounding separates:

* *retrieval failure* from *generation failure*

---

## 6️⃣ Confidence Score (System Trust Estimate)

### What it measures

An aggregate estimate of **how safe it is to answer**.

### How it’s computed

A weighted combination of:

* Coverage (retrieval completeness)
* Faithfulness (answer support)
* Grounding (evidence quality)

### What it means

| Confidence | Interpretation                                     |
| ---------- | -------------------------------------------------- |
| High       | High trust in the chosen response (answer/refusal) |
| Medium     | Retry may improve certainty                        |
| Low        | System is unsure of its own decision               |


### Why it exists

Production systems must:

* **calibrate trust**
* not answer everything
* prefer refusal over hallucination

---

## 7️⃣ Answer Type (Answer vs Refusal)

### What it measures

Whether the system’s response is an **answer** or an explicit **refusal**.

### How it’s computed

* Semantic analysis of the generated response
* Detection of insufficiency indicators (e.g., “not enough information in context”)
* Independent of numeric confidence score

### What it means

A **refusal** indicates that the system has determined the question
cannot be answered from the retrieved context.

Refusal is **not a failure**.

It is a **correct and safe outcome** when:
* the corpus lacks required information
* the question is out of scope
* answering would require hallucination


## 🧠 How These Metrics Work Together

Each metric captures a **different failure mode**:

| Metric       | Detects           |
| ------------ | ----------------- |
| Similarity   | Surface relevance |
| Coverage     | Missing intent    |
| Redundancy   | Context waste     |
| Faithfulness | Hallucination     |
| Grounding    | Evidence quality  |
| Confidence   | Overall trust     |

No single metric is trusted alone.
Decisions are made **systemically**, not heuristically.

---

# Answer Type vs Confidence (Important Distinction)

In this system, **answer intent** and **confidence** are treated as separate concepts.

* **Answer Type** determines *what* the system decided to do:
  * answer
  * refuse

* **Confidence** determines *how sure* the system is about that decision.

During retry, it is possible for:
- confidence to increase
- while the correct response remains a refusal

This occurs when:
- retrieval quality improves
- faithfulness increases
- grounding improves
- but the corpus still lacks the required information

In such cases, the system becomes **more confident that refusal is the correct outcome**.

This separation avoids policy ambiguity and reflects how
production LLM systems handle uncertainty safely.


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



