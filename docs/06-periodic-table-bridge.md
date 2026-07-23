# Bridge: Software Periodic Table × polymer

The Software Periodic Table identifies ~115 recurring atoms of software:
- Objects (1-35): nouns/entities
- Properties (36-60): attributes/fields
- Actions (61-85): verbs/operations
- Interfaces (86-100): views/presentation
- Intelligence (101-108): AI primitives
- Rules (109-115): automation/governance

The central dogma tells you **how information flows BETWEEN these atoms**. The periodic table gives you the atoms; polymer gives you the reaction.

## Mapping

| Periodic table family | DNA role | RNA role | Protein role |
|---------------------|----------|----------|-------------|
| Objects (1-35) | Stored entity definitions | Transient entity instances | Rendered/returned objects |
| Properties (36-60) | Config constants | Context fields | Output parameters |
| Actions (61-85) | Capability descriptions | Selected action intent | Executed tool calls |
| Interfaces (86-100) | Template definitions | Rendered views | User-facing output |
| Intelligence (101-108) | Model capability | Activated skill | Generated response |
| Rules (109-115) | Invariant policies | Active constraints | Enforced gates |

## How a polymer-aware agent uses the periodic table

Instead of generating atoms from scratch each time, an agent:

1. **DNA phase (planning)**: Retrieves relevant atoms from the periodic table — entities, actions, rules. These form the "genome" of the current task.

2. **RNA phase (context assembly)**: Selects which atoms to express based on the specific task. This is regulated transcription — not every retrieved atom gets used.

3. **Protein phase (execution)**: Composes selected atoms into runnable code. The composition IS the folded protein — structure determines function.

4. **Feedback phase (regulation)**: The result checks against rules. If the check fails, the composition is re-attempted (retry with different atom selection).

## Composition vs. generation

The periodic table's central claim: selecting and wiring curated atoms is superior to regenerating equivalent patterns. This is **composition** (analogous to protein folding from a finite set of amino acids) rather than **generation** (analogous to random peptide synthesis).

| Approach | Biology analog | Token cost | Reliability |
|----------|---------------|------------|-------------|
| Generate from scratch | Random peptide synthesis | High | Low |
| Retrieve + compose | Protein folding from genes | Medium | Medium |
| Reuse proven assembly | Conserved protein domain | Low | High |

## Practical workflow

1. Load periodic table atoms into vector store or context
2. Use the polymer SKILL prompt to reason about information flow
3. Select atoms that fit the task's "genetic program"
4. Compose along the DNA→RNA→Protein pipeline
5. Verify output against rules (the "immune system")
6. Register successful compositions as new conserved patterns

This is the skill that makes an agent **grow** software rather than **generate** it.