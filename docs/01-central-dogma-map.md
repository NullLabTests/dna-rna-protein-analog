# The Central Dogma Map

## Information flow in biology vs. AI

### DNA → RNA → Protein

The central dogma (Crick, 1958/1970) states that once information has passed into protein, it cannot get out again. More precisely:

- **DNA** replicates to DNA (replication)
- **DNA** transcribes to RNA (transcription)
- **RNA** translates to protein (translation)
- RNA can reverse-transcribe to DNA (retroviruses — an exception)
- Proteins do not flow back to nucleic acids

This is a **one-way information flow** from stable storage to ephemeral message to functional machinery.

### The isomorphic claim

AI agent systems exhibit the same directional constraint:

- **Weights / config / tools** (DNA-level) → define capability boundaries
- **Context window / activations** (RNA-level) → transient expression of capability
- **Output / tool calls / actions** (Protein-level) → real-world effect

Once context is consumed and output produced, you cannot "un-output." The information has crossed a phase boundary.

### Why this matters for agent architecture

| Biological principle | Agent architecture consequence |
|--------------------|-------------------------------|
| Most DNA is non-coding | Most config/tools are never used in one session |
| Transcription is regulated | Prompting is regulation; system prompt = promoter |
| RNA is ephemeral | Context windows must be managed, compacted, spliced |
| Proteins fold to function | Output formatting determines usability |
| Error rates are ~1e-9 | Agent error rates must approach biological fidelity for production |
| Epigenetics > genome mutation | In-context learning > retraining for adaptation |
| Evolution requires generations | Benchmark-loops > single-session improvement |

### Phase transitions of information

In biology, the critical transitions are:

1. **Replication** (DNA→DNA): copying with fidelity
2. **Transcription initiation**: regulated by promoters, enhancers, repressors
3. **RNA splicing**: one gene → multiple transcripts
4. **Translation initiation**: ribosome binding, start codon
5. **Protein folding**: primary sequence → 3D structure → function
6. **Feedback regulation**: protein affects transcription of its own gene

In AI agents, the parallel transitions are:

1. **Distillation** (model→model): compressed replication
2. **Inference start**: regulated by system prompt, temperature, priming
3. **Context splicing**: RAG retrieval, memory compaction, window sliding
4. **Output parsing**: raw tokens → structured action (JSON, code, tool call)
5. **Action execution**: parsed intent → side effect in the world
6. **Result verification**: output feeds back into context for next iteration

### The no-free-lunch of information flow

In biology, the one-way flow prevents acquired characteristics from rewriting the genome (Weismann barrier). In AI, the same barrier prevents a single bad output from corrupting the base model weights — but fine-tuning (analogous to retroviral integration) can introduce lasting changes. This is why:

- **LoRA adapters** are epigenetic: they modify expression without changing the genome
- **RLHF** is artificial selection: rewarding desired expression patterns
- **Prompt injection** is a regulatory hijack: an external signal that overrides normal transcription control