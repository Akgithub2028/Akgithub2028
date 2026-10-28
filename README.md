# Aayaann Kausar

**AI research and engineering · Software and cloud systems · IIT Kharagpur**

I work on continual learning, language-model adaptation, and AI applications. My current interests include efficient inference, GPU programming with CUDA and Triton, and infrastructure for AI systems.

[LinkedIn](https://linkedin.com/in/aayaann-kausar-8b2813344/) · [Portfolio](https://ak-portfolio-website-two.vercel.app/) &nbsp; <img src="https://komarev.com/ghpvc/?username=Akgithub2028&style=flat-square&color=526c8c&label=Profile+views" alt="Profile views">

<picture>
  <source media="(prefers-reduced-motion: reduce) and (max-width: 600px)" srcset="profile/signal-mobile.svg">
  <source media="(prefers-reduced-motion: reduce)" srcset="profile/signal.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Akgithub2028/Akgithub2028/output/pacman-contribution-graph.svg">
  <img src="https://raw.githubusercontent.com/Akgithub2028/Akgithub2028/output/pacman-contribution-graph-dark.svg" width="100%" alt="Pac-Man animation of my GitHub contribution history, updated daily">
</picture>

## Research

### [Subspace Feature Preservation](https://github.com/Akgithub2028/SFP)

Investigating how drift in task-critical activation directions predicts catastrophic forgetting, and whether preserving those directions improves sequential fine-tuning.

- **R² = 0.933** for drift along 32 ablation-ranked PCA directions in Qwen2.5-1.5B; **0.699** retention–plasticity harmonic score versus 0.631 for LwF.
- Selective feature regularization and a **conditional forgetting bound verified in Lean 4**, with scale-dependent empirical findings.

`PyTorch` `LoRA` `PCA` `Lean 4`

[Paper](https://github.com/Akgithub2028/SFP/blob/main/paper/sfp.pdf) · [Code](https://github.com/Akgithub2028/SFP) · [Formal verification](https://github.com/Akgithub2028/SFP/tree/main/lean-sfp)

## Selected projects

### [Real-Time Voice Translator](https://github.com/Akgithub2028/Real-Time-AI-Voice-Translator)

Bidirectional speech translation across **seven languages**, with streaming voice output, bilingual captions, and latency monitoring. Uses 20 ms audio frames; backend validation includes 27 tests.

`Python` `FastAPI` `WebSockets` `Next.js` `TypeScript` `Whisper` `GPT-OSS 20B` `ElevenLabs`

[Live demo](https://real-time-ai-voice-translator.vercel.app) · [Latency dashboard](https://real-time-ai-voice-translator.vercel.app/status) · [Code](https://github.com/Akgithub2028/Real-Time-AI-Voice-Translator)

### [Qwen2.5 QLoRA Fine-Tuning](https://github.com/Akgithub2028/qwen-domain-finetuning)

Adapted Qwen2.5-1.5B on 1,286 ML-systems tasks using 4-bit NF4 and rank-16 adapters. Paired evaluation found a **30.42% relative ROUGE-L improvement** across 161 held-out tasks, with topic-level analysis and **14.2% of examples regressing**.

`PyTorch` `QLoRA` `PEFT` `TRL` `ROUGE-L` `BERTScore`

[Code and study](https://github.com/Akgithub2028/qwen-domain-finetuning) · [Evaluation results](https://github.com/Akgithub2028/qwen-domain-finetuning/tree/main/results)

### [NexusAgent](https://github.com/Akgithub2028/NexusAgent-Enterprise-Autonomous-Multi-Agent-Decision-Intelligence-Platform)

Decision-support platform combining hybrid retrieval, guarded MCP NL2SQL, and evidence review. Achieved **96.25% retrieval Hit@1** on 160 answerable synthetic queries; recorded validation includes **1,941 unit tests and 323 offline integration tests**.

`Python` `LangGraph` `Milvus` `BM25` `BGE` `MCP` `SQLGlot` `FastAPI`

[Architecture](https://github.com/Akgithub2028/NexusAgent-Enterprise-Autonomous-Multi-Agent-Decision-Intelligence-Platform/blob/main/docs/ARCHITECTURE.md) · [Benchmark evidence](https://github.com/Akgithub2028/NexusAgent-Enterprise-Autonomous-Multi-Agent-Decision-Intelligence-Platform/tree/main/artifacts/public-evaluation) · [Code](https://github.com/Akgithub2028/NexusAgent-Enterprise-Autonomous-Multi-Agent-Decision-Intelligence-Platform)

### [Autonomous AI Co-Scientist](https://github.com/Akgithub2028/Autonomous-AI-Co-Scientist)

Multi-agent research workflow for literature review, hypothesis generation, critique, and iterative refinement. Combines **Elo-ranked hypotheses**, corrective RAG, persistent vector memory, and asynchronous workers.

`Python` `LangGraph` `ChromaDB` `Docker`

[Code and research workflow](https://github.com/Akgithub2028/Autonomous-AI-Co-Scientist)

## Technical focus

| Area | Tools and topics |
| :--- | :--- |
| Model research and adaptation | PyTorch, Transformers, LoRA / QLoRA, PEFT, TRL, Lean 4 |
| AI applications | LangGraph, retrieval-augmented generation, MCP, FastAPI, WebSockets, Next.js |
| Software and cloud systems | Python, C++, TypeScript, Linux, Docker, Kubernetes, Terraform, CI/CD, AWS, GCP |
| Current study | CUDA, Triton, GPU kernels, profiling, and LLM serving |

## Competition

**Wunder Fund — HFT Market State Forecasting Challenge**

**9th of 5,000+ competitors** · Final R² **0.3920**

Trained a four-layer, eight-head Transformer and optimized CPU inference with `torch.compile`, Numba, and preallocated buffers.

<details>
<summary>Academic achievements</summary>

- **JEE Main 2024:** top 0.29%.
- **JEE Advanced 2024:** top 3.2%.
- **WBJEE 2024:** top 0.20%.

</details>
