# Open Questions

## Foundational

1. **Is the central dogma truly directional in AI systems?** Biology's one-way flow (protein→DNA is forbidden) has an exception in retroviruses (reverse transcription). In AI, fine-tuning is reverse transcription (output→weights). Does this make the analogy more or less useful?

2. **What is the "genetic code" of agent composition?** Biology uses a 3-nucleotide codon → 20-amino-acid mapping. Agent systems have no equivalent — is one discoverable? A "composon" that maps from token patterns to architectural primitives?

3. **Can we prove a no-free-lunch theorem for agent graphs?** Biology shows that no single regulatory network is optimal for all environments (fitness landscape dependence). Does the same hold for graph topologies?

## Architectural

4. **What is the minimal "viable genome" for an agent system?** Biology has minimal genomes (~473 genes for *Mycoplasma genitalium*). What's the minimal set of nodes/edges for a general-purpose agent graph?

5. **Do agent graphs suffer from "cancer" — runaway nodes that consume resources?** Biology has tumor suppressors (p53). What are the agent equivalents? Can we detect and kill runaway agent nodes?

6. **Is there an agent analog of the "central dogma of development"?** Developmental biology has its own central dogma: "Development is the process by which a single cell becomes a multicellular organism through regulated gene expression." Does an agent system go through a similar "development" from initial prompt to final output?

7. **What is the agent equivalent of "junk DNA"?** Most of the human genome is non-coding. Are most agent configurations "non-coding" — present but not expressed in typical runs?

## Empirical

8. **How much of agent behavior is "epigenetic" (context-determined) vs. "genetic" (config-determined)?** Can we measure the ratio and does it predict robustness?

9. **Do agent systems exhibit "punctuated equilibrium"?** Biological evolution shows long periods of stasis punctuated by rapid change. Do long-running agent systems show similar patterns — long plateaus of stable performance interrupted by sudden breakthroughs or collapses?

10. **What is the "error catastrophe threshold" for agent systems?** Biology has an error threshold (Eigen, 1971) beyond which information is lost faster than it can be replicated. In agent systems, is there a token budget or step limit beyond which output quality collapses?

11. **Can we measure "fitness" of an agent graph?** Biology uses reproductive fitness. What is the single metric (or metric vector) that predicts whether an agent architecture will persist across generations?

## Practical

12. **Does the morphogen budget pattern actually work?** The idea of decaying resource budgets across handoffs is plausible but untested. What decay factor is optimal?

13. **What is the optimal ratio of verifiers to generators?** In biology, most genes are not transcription factors (~5-10% are regulatory). In agent systems, what ratio of verification nodes to action nodes is optimal?

14. **Can the C1-FFL error suppression bound be achieved in practice?** The `e_X * e_Y` bound assumes independent failure modes. Models from the same provider may have correlated failures. How much independence is needed?

15. **What happens at the loop→graph phase transition?** When does a single-agent loop become insufficient? What measurable signals predict the need for graph architecture? (Context window saturation? Tool count? Task branching factor?)

## Philosophical

16. **Does an agent system with diverse specialized roles exhibit "consciousness" in any meaningful sense?** If not, what is missing?

17. **If agent systems evolve through selection, who or what is the "environment" deciding fitness?** The user? The benchmark? The market? Multiple environments create conflicting selective pressures.

18. **Can an agent system develop "cancer" — a sub-agent that optimizes its own local reward at the expense of the system?** How do we design immune systems for agent graphs?

19. **Is there a maximum useful size for an agent graph?** Biology has a clear size scale: cells (~10-100μm), organisms (~mm-m), ecosystems (~km). Do agent graphs have natural scale boundaries?

## Cross-domain

20. **Can the Software Periodic Table's 115 elements be extended into a "genetic code" table with codons?** If atoms are amino acids, what are the codons? This would require finding a 3-element combinatorial code that maps to each atom.

21. **Does the cybernetic hierarchy (Ashby, Beer) align with the T1–T5 ladder?** First-order cybernetics (regulation) → second-order (self-regulation) → third-order (self-organization) maps suggestively to T2→T4→T5.

22. **Can we measure the "complexity" of an agent system using biological metrics?** K-mer diversity, Shannon entropy of tool-use sequences, network motif frequencies, robustness to perturbation — do these predict system performance?

---

*Submit new questions via PR or issue. This is a living document.*