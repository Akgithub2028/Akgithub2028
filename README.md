<p align="center">
  <picture>
    <source media="(max-width: 600px) and (prefers-color-scheme: light)" srcset="assets/identity/masthead-mobile-light.svg">
    <source media="(max-width: 600px)" srcset="assets/identity/masthead-mobile.svg">
    <source media="(prefers-color-scheme: light)" srcset="assets/identity/masthead-light.svg">
    <img src="assets/identity/masthead.svg" width="100%" alt="Aayaann Kausar — AI research and engineering · IIT Kharagpur">
  </picture>
</p>

<p align="center">
  <picture>
    <source media="(prefers-reduced-motion: reduce)" srcset="assets/coding-illustration.png">
    <img src="assets/coding-illustration.webp" width="190" height="190" alt="Animated blue and purple coding character working at a laptop">
  </picture>
</p>

<p align="center">
  <strong>Understanding models. Building the systems around them.</strong><br>
  I study how language models retain and adapt knowledge, and build AI systems<br>
  for speech, retrieval, and scientific reasoning.
</p>

<p align="center">
  <a href="https://linkedin.com/in/aayaann-kausar-8b2813344/"><strong>LinkedIn ↗</strong></a> &nbsp; · &nbsp;
  <a href="https://ak-portfolio-website-two.vercel.app/"><strong>Portfolio ↗</strong></a> &nbsp; · &nbsp;
  <a href="#selected-work"><strong>Explore the work ↓</strong></a>
</p>
<p align="center">
  <img src="https://komarev.com/ghpvc/?username=Akgithub2028&style=flat-square&color=7763ce&label=Profile+views" alt="Profile views">
</p>

<picture>
  <source media="(prefers-reduced-motion: reduce) and (max-width: 600px)" srcset="profile/signal-mobile.svg">
  <source media="(prefers-reduced-motion: reduce)" srcset="profile/signal.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Akgithub2028/Akgithub2028/output/pacman-contribution-graph.svg">
  <img src="https://raw.githubusercontent.com/Akgithub2028/Akgithub2028/output/pacman-contribution-graph-dark.svg" width="100%" alt="Pac-Man animation of my GitHub contribution history, updated daily">
</picture>

## Selected work

Research questions, working systems, and the evidence behind them.

<table width="100%">
<tr><td>
<p><img src="assets/labels/research.svg" alt="Continual learning" height="26"></p>
<h3><a href="https://github.com/Akgithub2028/SFP">Subspace Feature Preservation</a></h3>
<p>Investigating catastrophic forgetting through activation drift. SFP preserves an ablation-ranked PCA subspace during sequential language-model fine-tuning.</p>
<blockquote><strong>0.933 R²</strong> for drift prediction · <strong>0.699</strong> retention–plasticity harmonic score</blockquote>
<p>Results on Qwen2.5-1.5B with 32 directions; LwF scores 0.631. Includes a conditional forgetting bound verified in <strong>Lean 4</strong>. Findings vary with model scale.</p>
<p><code>PyTorch</code> <code>LoRA</code> <code>PCA</code> <code>Lean 4</code></p>
<p><a href="https://github.com/Akgithub2028/SFP/blob/main/paper/sfp.pdf"><strong>Read the paper ↗</strong></a> &nbsp; · &nbsp; <a href="https://github.com/Akgithub2028/SFP">Code</a> &nbsp; · &nbsp; <a href="https://github.com/Akgithub2028/SFP/tree/main/lean-sfp">Formal proofs</a></p>
</td></tr>
</table>

<table width="100%">
<tr><td>
<p><img src="assets/labels/speech.svg" alt="Speech systems" height="26"></p>
<h3><a href="https://github.com/Akgithub2028/Real-Time-AI-Voice-Translator">Real-Time Voice Translator</a></h3>
<p>Bidirectional translation across <strong>7 languages</strong>, with bilingual captions, streamed voice playback, and explicit speaker switching.</p>
<blockquote><strong>Whisper → GPT-OSS 20B → ElevenLabs</strong><br>Streaming audio, translation, and speech synthesis.</blockquote>
<p>AudioWorklet capture, stale-response filtering, and stage-level p50/p95 monitoring; <strong>27 backend tests</strong>. Deployed on Vercel and Render.</p>
<p><code>Next.js</code> <code>FastAPI</code> <code>WebSockets</code> <code>Web Audio</code></p>
<p><a href="https://real-time-ai-voice-translator.vercel.app"><strong>Try the translator ↗</strong></a> &nbsp; · &nbsp; <a href="https://real-time-ai-voice-translator.vercel.app/status">Latency dashboard</a> &nbsp; · &nbsp; <a href="https://github.com/Akgithub2028/Real-Time-AI-Voice-Translator">Code</a></p>
</td></tr>
</table>

<table width="100%">
<tr><td>
<p><img src="assets/labels/adaptation.svg" alt="Model adaptation" height="26"></p>
<h3><a href="https://github.com/Akgithub2028/qwen-domain-finetuning">Qwen2.5 · QLoRA Fine-Tuning</a></h3>
<p>Adapting Qwen2.5-1.5B on <strong>1,286 ML-systems examples</strong> with 4-bit NF4 and rank-16 adapters, evaluated across topics and difficulty levels.</p>
<blockquote><strong>+30.42% relative ROUGE-L</strong> on 161 held-out tasks<br>BERTScore F1: <strong>0.8187 → 0.8497</strong></blockquote>
<p>Error analysis spans 48 topics and reports the <strong>14.2% of tasks that regressed</strong>, alongside aggregate gains.</p>
<p><code>PyTorch</code> <code>PEFT</code> <code>TRL</code> <code>QLoRA</code></p>
<p><a href="https://github.com/Akgithub2028/qwen-domain-finetuning/tree/main/results"><strong>Explore the results ↗</strong></a> &nbsp; · &nbsp; <a href="https://github.com/Akgithub2028/qwen-domain-finetuning">Code and study</a></p>
</td></tr>
</table>

<table width="100%">
<tr><td>
<p><img src="assets/labels/agents.svg" alt="Agent infrastructure" height="26"></p>
<h3><a href="https://github.com/Akgithub2028/NexusAgent-Enterprise-Autonomous-Multi-Agent-Decision-Intelligence-Platform">NexusAgent</a></h3>
<p>Evidence-grounded decision support across documents and relational data. LangGraph coordinates hybrid retrieval, MCP text-to-SQL, and answer review.</p>
<blockquote><strong>96.25% retrieval Hit@1</strong> on 160 answerable synthetic queries<br><strong>1,941 unit tests</strong> · <strong>323 offline integration tests</strong></blockquote>
<p>Milvus, BM25, rank fusion, and BGE reranking support retrieval. SQLGlot AST validation, read-only scopes, and query timeouts control SQL execution.</p>
<p><code>LangGraph</code> <code>Milvus</code> <code>MCP</code> <code>SQLGlot</code></p>
<p><a href="https://github.com/Akgithub2028/NexusAgent-Enterprise-Autonomous-Multi-Agent-Decision-Intelligence-Platform/blob/main/docs/ARCHITECTURE.md"><strong>Explore the architecture ↗</strong></a> &nbsp; · &nbsp; <a href="https://github.com/Akgithub2028/NexusAgent-Enterprise-Autonomous-Multi-Agent-Decision-Intelligence-Platform/tree/main/artifacts/public-evaluation">Evidence</a> &nbsp; · &nbsp; <a href="https://github.com/Akgithub2028/NexusAgent-Enterprise-Autonomous-Multi-Agent-Decision-Intelligence-Platform">Code</a></p>
</td></tr>
</table>

<table width="100%">
<tr><td>
<p><img src="assets/labels/science.svg" alt="AI for science" height="26"></p>
<h3><a href="https://github.com/Akgithub2028/Autonomous-AI-Co-Scientist">Autonomous AI Co-Scientist</a></h3>
<p>Developing research hypotheses from literature through coordinated agents, iterative critique, and evidence retrieval.</p>
<blockquote><strong>Review → Generate → Critique → Rank → Refine</strong><br>Literature-grounded hypotheses with Elo-based ranking.</blockquote>
<p>LangGraph coordinates asynchronous workers; corrective RAG and persistent vector memory support evidence retrieval and final-report synthesis.</p>
<p><code>Python</code> <code>LangGraph</code> <code>ChromaDB</code> <code>Docker</code></p>
<p><a href="https://github.com/Akgithub2028/Autonomous-AI-Co-Scientist"><strong>Explore the research workflow ↗</strong></a></p>
</td></tr>
</table>

## From models to infrastructure

My work connects model behaviour, application engineering, and the systems that run them.

| Focus | Tools & direction |
| :--- | :--- |
| **🟣 Model research** | Continual learning, PyTorch, Transformers, LoRA / QLoRA, PEFT, TRL, Lean 4 |
| **🔵 AI applications** | LangGraph, RAG, MCP, FastAPI, WebSockets, Next.js |
| **🟢 Software & cloud** | Python, C++, TypeScript, Linux, Docker, Kubernetes, Terraform, CI/CD, AWS, GCP |
| **🟠 Studying now** | CUDA, Triton, GPU kernels, profiling, efficient inference, and LLM serving |

## Competition & academics

<table width="100%">
<tr><td>
<p><sub>WUNDER FUND / HFT MARKET STATE FORECASTING</sub></p>
<h3>9th of 5,000+ competitors</h3>
<p><strong>Final R²: 0.3920</strong> · Forecasting over 1,000-step streaming sequences.</p>
<p>A four-layer, eight-head Transformer with masked autoencoding and temporal positional encodings. Optimized CPU inference with <code>torch.compile</code>, Numba kernels, and preallocated buffers.</p>
</td></tr>
</table>

<details>
<summary><strong>Academic achievements</strong> · Engineering entrance examinations, 2024</summary>

| Examination | Standing |
| :--- | :--- |
| JEE Main | Top **0.29%** |
| JEE Advanced | Top **3.2%** |
| WBJEE | Top **0.20%** |

</details>

## GitHub activity

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: light)" srcset="profile/stats-light.svg">
    <img src="profile/stats.svg" width="600" alt="GitHub stats: contributions over the last year, stars on public original repositories, public original repository count, and followers. Updated daily.">
  </picture>
</p>
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: light)" srcset="profile/top-langs-light.svg">
    <img src="profile/top-langs.svg" width="600" alt="Most-used languages by code bytes across public original repositories. Updated daily.">
  </picture>
</p>

---

<p align="center">
  <strong>Interested in model research or building AI systems?</strong><br>
  <a href="https://linkedin.com/in/aayaann-kausar-8b2813344/">Connect on LinkedIn ↗</a> &nbsp; · &nbsp; <a href="https://ak-portfolio-website-two.vercel.app/">Visit my portfolio ↗</a>
</p>
