# RPO Research Sweep — 2026-02-17

Purpose: gather recent (2023–2026) academic and engineering evidence that supports, validates, or stress-tests specific RPO design decisions. Complements the original [annotated bibliography (2026-02-10)](./rpo-academic-research-2026-02-10.md) with targeted research across six dimensions.

---

## Executive Summary

Six parallel research tracks investigated the empirical basis for RPO's core design choices. Findings across **80+ sources** converge on three conclusions:

1. **Input-side schema enforcement avoids the reasoning penalty of output-side constraints.** Constraining output tokens during decoding degrades reasoning quality (Park et al., NeurIPS 2024; Tam et al., EMNLP 2024; Banerjee et al., 2025). RPO's architecture — strict input validation, flexible output — gets structural guarantees without semantic cost.

2. **Prompt format dramatically affects output quality, and deterministic rendering eliminates format variance.** Performance varies up to 76 accuracy points from formatting alone (Sclar et al., ICLR 2024), up to 40% from template format choice (He et al., 2024). RPO eliminates this by enforcing a single canonical format per target.

3. **Prompts are software artifacts that require versioning, testing, and CI/CD.** 58.8% of prompt+model combinations regress on API updates (Ma et al., CAIN 2024). Only 21.9% of prompt changes are documented in commits (Tafreshipour et al., MSR 2025). RPO's schema validation, changelog enforcement, and snapshot testing directly address these failures.

**RPO's unique position:** No existing system applies strict JSON Schema validation (Draft 2020-12, `additionalProperties: false`) to the *prompt itself* as a first-class IR. The literature validates each design choice independently; RPO is the first to combine them.

---

## Track 1: Token Efficiency and Cost Savings

### Key Findings

| Source | Token Savings | Mechanism | RPO Relevance |
|--------|--------------|-----------|---------------|
| Schmidt et al., Frontiers AI 2025 | ~30-50% via format choice | Prompt format selection | Validates per-provider rendering |
| Hsieh et al., 2025 | Diminishing returns documented | Token-cost framework (Big-O_tok) | Enables per-section ROI analysis |
| LLMLingua, EMNLP 2023 (Microsoft) | Up to 20x compression | Token pruning via small LM | Complementary: RPO + compression = multiplicative |
| LongLLMLingua, ACL 2024 | Up to 94% cost reduction | Positional-aware compression | Informs RPO section ordering |
| CompactPrompt, 2025 | Up to 60% reduction | N-gram + self-information | Validates redundancy elimination |
| Prompt Cache, MLSys 2024 (Yale/Google) | 8x–60x latency reduction | Modular attention reuse via schema | Architectural sibling to RPO |
| Anthropic Prompt Caching, 2024 | Up to 90% cost, 85% latency | Exact prefix caching | RPO sections = natural cache units |
| OpenAI Prompt Caching, 2024 | 50% cost reduction | Automatic prefix matching | RPO structure triggers auto-cache |
| FrugalGPT, Stanford, TMLR 2024 | Up to 98% cost reduction | LLM cascade | RPO enables per-cascade-tier rendering |
| TokenOps, 2025 | 40-46% reduction | Template matching + hierarchical reduction | RPO provides the hierarchy |
| Dynamic Template Selection, 2025 | ~33% output token reduction | Template routing | RPO systematizes template selection |
| EPiC, 2024 | 2-10x more cost-effective | Evolutionary prompt refinement | RPO enables section-level mutation |

### Critical Finding: Prompt Cache (Gim et al., MLSys 2024)

Prompt Cache defines reusable "prompt modules" via a schema and caches attention states across prompts sharing those modules. **RPO's section-based architecture (mode/rules, warm_state, hot_task) maps directly to Prompt Cache's module concept.** RPO sections are natural cache boundaries:

- `mode` + `warm_state` → stable prefix, cacheable across turns
- `hot_task` → dynamic per-request, varies each call

**Anthropic's production caching** requires exact prefix matching — even whitespace differences break the cache. RPO's deterministic rendering guarantees byte-identical prefixes, maximizing cache hit rates.

### References

- Schmidt et al. (2025). "Enhancing Structured Data Generation with GPT-4o." *Frontiers in AI* 8:1558938. https://doi.org/10.3389/frai.2025.1558938
- Hsieh et al. (2025). "Incorporating Token Usage into Prompting Strategy Evaluation." arXiv:2505.14880
- Jiang et al. (2023). "LLMLingua." *EMNLP 2023*, pp. 13358-13376. https://aclanthology.org/2023.emnlp-main.825/
- Jiang et al. (2024). "LongLLMLingua." *ACL 2024*, pp. 1658-1677. https://aclanthology.org/2024.acl-long.91/
- CompactPrompt (2025). arXiv:2510.18043
- Gim et al. (2024). "Prompt Cache: Modular Attention Reuse." *MLSys 2024*. https://arxiv.org/abs/2311.04934
- Anthropic. "Prompt Caching." https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching
- OpenAI. "Prompt Caching." https://platform.openai.com/docs/guides/prompt-caching
- Chen et al. (2023). "FrugalGPT." arXiv:2305.05176. *TMLR 2024*
- Lodha (2025). "TokenOps." https://www.chitrangana.com/wp-content/uploads/2025/04/Research-Paper-TokenOps.pdf
- Taherkhani & Sepindband (2024). "EPiC." arXiv:2408.11198
- Shimizu et al. (2024). "Optimizing Token Usage via DSM." *DSM 2024*. arXiv:2410.00749

---

## Track 2: Determinism and Reproducibility

### Key Findings

**Hardware non-determinism is real:** Even with temperature=0, GPU floating-point non-associativity causes up to 15% accuracy variance (Atil et al., 2024). Small models (2-8B) answer consistently only 50-80% of the time (Pinhanez et al., 2025).

**Prompt formatting is the largest controllable variance source:**
- Up to 76 accuracy points from formatting-only changes (Sclar et al., ICLR 2024)
- Up to 40% from template format choice in code translation (He et al., 2024)
- Reasoning tasks are 37% more sensitive to format than classification (Ngweta et al., NAACL 2025)

**Section ordering matters:** Input reordering changes outputs even when semantics are preserved (McIlroy-Young et al., 2024; Guan et al., 2025). RPO's fixed section schema eliminates ordering variance by design.

**Structured prompting improves evaluation reliability:** Without structured prompting, HELM underestimates LM performance by ~4% and variance increases by ~2% SD (Aali et al., 2025). Modular Prompt Optimization (MPO) — treating prompts as structured objects with independently optimizable sections — outperforms monolithic optimization (Sharma & Henley, 2026).

### Derived Hypotheses

- **H6 (Formatting determinism):** Byte-identical prompt rendering eliminates the 40-76 point accuracy variance from formatting differences.
- **H7 (Section ordering):** RPO's fixed schema eliminates order-dependency variance that degrades output quality.
- **H8 (Section-level optimization):** RPO's architecture enables per-section optimization that outperforms monolithic prompt optimization.

### References

- Atil et al. (2024). "Non-Determinism of 'Deterministic' LLM Settings." arXiv:2408.04667
- Pinhanez et al. (2025). "The Non-Determinism of Small LLMs." arXiv:2509.09705
- Peeperkorn et al. (2024). "Is Temperature the Creativity Parameter?" *ICCC'24*. arXiv:2405.00492
- Sclar et al. (2024). "Quantifying Sensitivity to Spurious Features." *ICLR 2024*. https://openreview.net/forum?id=RIu5lyNXjT
- Zhuo et al. (2024). "ProSA: Assessing Prompt Sensitivity." *EMNLP 2024 Findings*. arXiv:2410.12405
- Zhu et al. (2023). "PromptBench." arXiv:2306.04528
- He et al. (2024). "Does Prompt Formatting Have Any Impact?" arXiv:2411.10541
- Liu et al. (2025). "Content-Format Integrated Prompt Optimization (CFPO)." arXiv:2502.04295
- Ngweta et al. (2025). "Towards Robustness to Prompt Format Styles." *NAACL 2025 SRW*. arXiv:2504.06969
- McIlroy-Young et al. (2024). "Order-Independence Without Fine Tuning." arXiv:2406.06581
- Guan et al. (2025). "The Order Effect." arXiv:2502.04134
- Aali et al. (2025). "Structured Prompting Enables More Robust Evaluation." arXiv:2511.20836
- Sharma & Henley (2026). "Modular Prompt Optimization (MPO)." arXiv:2601.04055
- Commey (2026). "When 'Better' Prompts Hurt." arXiv:2601.22025
- Seleznyov et al. (2025). "When Punctuation Matters." arXiv:2508.11383

---

## Track 3: Microsoft Ecosystem Alignment

### Key Finding: Azure Documentation Uses "Output Contract"

Azure's official system message design guide uses the exact term "output contract" to describe structured output specifications — the same term RPO uses for its `output_contract` field. This is the strongest terminological alignment found.

### Microsoft Ecosystem Map

| Initiative | Layer | RPO Relationship |
|---|---|---|
| **Semantic Kernel** | Runtime SDK | RPO renders messages SK consumes; SK's factory pattern (ADR-0016) supports RPO as a template format |
| **POML** (arXiv:2508.13948) | Authoring markup | RPO is the IR; POML could compile to RPO; `warm_state` is RPO's unique contribution POML lacks |
| **Prompty** | File format / asset packaging | Prompty packages execution config + template; RPO provides structured content; they compose |
| **Guidance** | Inference enforcement | RPO's `output_contract` could reference Guidance grammars for enforced constrained decoding |
| **PromptWizard** (arXiv:2405.18369) | Optimization | RPO's structured fields enable targeted per-section optimization |
| **SAMMO** | Structural optimization | RPO's schema provides stable anchor points for SAMMO's optimizer |
| **LMOps** | Research umbrella | RPO aligns with LMOps' thesis of prompts as optimizable software artifacts |
| **Azure System Messages** | Enterprise guidance | Azure uses "output contract"; RPO is the machine-readable implementation |
| **Dynamic Prompt Middleware** | UX research | RPO's fields could serve as the data model middleware UIs generate |

### Strategic Observations

1. **No single Microsoft tool covers RPO's niche.** POML is closest but lacks `warm_state`. Prompty lacks semantic decomposition. SK lacks prompt-level structure.
2. **RPO's `warm_state` concept** (goal, constraints, facts, decisions, next_actions) has no equivalent in any Microsoft tool surveyed. This is RPO's unique contribution.
3. **SK's ADR-0016** (factory pattern for custom prompt template formats) was designed for pluggable formats — RPO's natural integration point.
4. **Microsoft has 3+ prompt optimization frameworks** (PromptWizard, SAMMO, LMOps), all of which benefit from structured prompt representations.

### References

- Microsoft. "Semantic Kernel Prompt Engineering." https://learn.microsoft.com/en-us/semantic-kernel/concepts/prompts/
- Microsoft. "SK ADR-0016: Custom Prompt Template Formats." https://github.com/microsoft/semantic-kernel/blob/main/docs/decisions/0016-custom-prompt-template-formats.md
- Zhang et al. (2025). "POML." arXiv:2508.13948. https://github.com/microsoft/poml
- Agarwal et al. (2024). "PromptWizard." arXiv:2405.18369. https://github.com/microsoft/PromptWizard
- Schnabel & Neville (2024). "SAMMO." https://www.microsoft.com/en-us/research/blog/sammo-a-general-purpose-framework-for-prompt-optimization/
- Drosos et al. (2025). "Dynamic Prompt Middleware." *CHIWORK '25*
- Microsoft. "LMOps." https://github.com/microsoft/LMOps
- Microsoft. "Safety System Messages." https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/system-message
- Microsoft. "Guidance." https://github.com/guidance-ai/guidance
- Microsoft. "Prompty." https://github.com/microsoft/prompty

---

## Track 4: Schema Validation and Constraint Satisfaction

### Key Findings

**Input-side constraints avoid reasoning penalties:**
- Grammar-Aligned Decoding (Park et al., NeurIPS 2024): constrained decoding distorts LLM probability distributions, degrading semantic quality
- CRANE (Banerjee et al., 2025): adaptive constrained decoding gains up to 10pp accuracy over pure constrained baselines
- "Let Me Speak Freely?" (Tam et al., EMNLP 2024): significant reasoning decline under output format restrictions, but classification tasks *improve*
- RPO's design: constrain the *input* (prompt object) strictly, leave the *output* format flexible

**The `additionalProperties: false` pattern is the industry standard:**
- OpenAI's strict mode requires it on every object with all fields in `required`
- Anthropic compiles schemas into grammar artifacts and caches them for 24 hours
- Both independently converged on closed-schema design
- RPO already satisfies this standard across all object definitions

**JSONSchemaBench (Geng et al., 2025):** 10,000 real-world JSON schemas benchmarked against six constrained decoding frameworks. RPO's schema features (`additionalProperties: false`, `required`, `oneOf`, `minLength`, `minimum`) all fall within the well-supported complexity class.

**Prompt specificity matters:** DETAIL (arXiv:2512.02246) finds specificity improves accuracy, especially for smaller models. RPO's required fields (`goal`, `constraints`, `success_criteria`) are a specificity enforcement mechanism.

### Derived Hypothesis

- **H9 (Input-side enforcement):** RPO-structured prompts with unconstrained output will produce higher reasoning scores than equivalent content with constrained output decoding, while matching schema conformance via post-hoc validation.

### References

- Willard & Louf (2023). "Efficient Guided Generation (Outlines)." arXiv:2307.09702
- Park et al. (2024). "Grammar-Aligned Decoding." *NeurIPS 2024*. arXiv:2405.21047
- Dong et al. (2025). "XGrammar." *MLSys 2025*. arXiv:2411.15100
- Banerjee et al. (2025). "CRANE." arXiv:2502.09061
- Geng et al. (2025). "JSONSchemaBench." arXiv:2501.10868
- Tam et al. (2024). "Let Me Speak Freely?" *EMNLP 2024*. arXiv:2408.02442
- Raspanti et al. (2025). "GCD for Logical Parsing." *ACL 2025 Industry*
- Zheng et al. (2024). "SGLang." *NeurIPS 2024*. arXiv:2312.07104
- OpenAI. "Structured Outputs." https://openai.com/index/introducing-structured-outputs-in-the-api/
- Anthropic. "Structured Outputs." https://docs.claude.com/en/docs/build-with-claude/structured-outputs
- "5C Prompt Contracts." arXiv:2507.07045
- "FASTRIC." arXiv:2512.18940

---

## Track 5: Prompt Versioning, Drift, and CI/CD

### Key Findings

**Prompt drift is real and severe:**
- GPT-4 accuracy on prime identification: 97.6% → 2.4% across two versions, same prompt (Chen et al., 2023)
- 58.8% of prompt+model combinations regress on API updates (Ma et al., CAIN 2024)
- GPT-4o reduced output tokens by ~1/3 in a silent update (OpenAI community, 2024)
- Azure safety policy changes blocked previously-working prompts (Microsoft Tech Community, 2024)

**Current practices are inadequate:**
- Only 21.9% of prompt changes documented in commits (Tafreshipour et al., MSR 2025)
- Widespread format inconsistency across 24,800 prompts in 92 repos (Li et al., IEEE Software 2025)
- 74 professionals confirm ad-hoc practices (Villamizar et al., PROFES 2025)
- "Promptware crisis" identified, analogous to 1960s software crisis (Chen et al., TOSEM 2025)

**CI/CD for prompts is emerging:**
- Promptfoo: open-source CLI with GitHub Actions, before/after PR views
- DeepEval: pytest-native LLM evaluation framework
- Traceloop: LLM-as-a-Judge in CI with cost/latency gating

**"Better" prompts can hurt:** Adding rules to Llama 3 8B degraded extraction accuracy by 10% while improving instruction-following (Commey, 2026). Snapshot testing catches these trade-offs.

### RPO's Direct Address

| Problem | Evidence | RPO Solution |
|---------|----------|-------------|
| Undocumented prompt changes | 21.9% documentation rate | Changelog enforcement via CI gate |
| Format inconsistency | 24,800 inconsistent prompts | Schema validation (`additionalProperties: false`) |
| Silent model regressions | 97.6% → 2.4% accuracy drop | Snapshot testing with deterministic rendering |
| "Better prompts hurt" | 10% extraction accuracy loss | Regression gates reject degrading changes |
| Ad-hoc practices | 74 professionals confirm | Structured schema + SKILL.md workflow |

### References

- Chen et al. (2023). "How Is ChatGPT's Behavior Changing?" arXiv:2307.09009. *HDSR* 6.2, 2024
- Ma et al. (2024). "(Why) Is My Prompt Getting Worse?" *CAIN 2024*. arXiv:2311.11123
- Tafreshipour et al. (2024). "Prompting in the Wild." *MSR 2025*. arXiv:2412.17298
- Li et al. (2025). "Understanding Prompt Management in GitHub." *IEEE Software*. arXiv:2509.12421
- Villamizar et al. (2025). "Prompts as SE Artifacts." *PROFES 2025*. arXiv:2509.17548
- Chen et al. (2025). "Promptware Engineering." *TOSEM*. arXiv:2503.02400
- Li et al. (2025). "Prompt-with-Me." *ASE 2025*. arXiv:2509.17096
- Commey (2026). "When 'Better' Prompts Hurt." arXiv:2601.22025
- Promptfoo. https://github.com/promptfoo/promptfoo
- DeepEval. https://github.com/confident-ai/deepeval

---

## Track 6: Separation of Concerns in Prompt Engineering

### Key Findings

**System/user separation is fragile:**
- Instruction hierarchy fails: models struggle with consistent prioritization even for simple formatting conflicts (Geng et al., AAAI 2026)
- Societal hierarchy framings (authority, expertise) influence behavior more than system/user roles
- System prompt drift within 8 conversation rounds (Li et al., COLM 2024)
- System prompt robustness requires fine-tuning on realistic data (Mu et al., 2025)

**Architectural separation helps:**
- ASIDE (Zverev et al., ICLR 2026): orthogonal rotation of data token embeddings achieves instruction-data separation without parameters, improving prompt injection robustness
- Wallace et al. (2024): instruction hierarchy training drastically increases robustness, even for unseen attacks

**Context management matters:**
- Context Rot (Chroma, 2025): models perform worse on logically structured haystacks than shuffled ones; focused prompts outperform full prompts at ~113K tokens
- Found-in-the-Middle (Hsieh et al., ACL 2024): U-shaped attention bias; up to 15pp gains from calibrating positional attention
- Implication: RPO's section ordering should place high-priority content at boundaries (start/end), not middle

**Format and content must be co-optimized:**
- CFPO (Liu et al., 2025): jointly optimizing content and format outperforms content-only optimization
- RPO's schema/renderer separation enables exactly this

### References

- Geng et al. (2026). "Control Illusion: Instruction Hierarchy Failure." *AAAI 2026*. arXiv:2502.15851
- Wallace et al. (2024). "The Instruction Hierarchy." arXiv:2404.13208
- Zverev et al. (2026). "ASIDE." *ICLR 2026*. arXiv:2503.10566
- Li et al. (2024). "Instruction Stability in LM Dialogs." *COLM 2024*. arXiv:2402.10962
- Mu et al. (2025). "System Prompt Robustness." arXiv:2502.12197
- Hong et al. (2025). "Context Rot." Chroma Research. https://research.trychroma.com/context-rot
- Hsieh et al. (2024). "Found in the Middle." *ACL Findings 2024*. arXiv:2406.16008

---

## Updated Hypotheses (H1–H12)

Building on the original 5 hypotheses from the Feb 10 bibliography:

| # | Hypothesis | Evidence Base |
|---|-----------|--------------|
| H1 | Explicit output contract increases parseable output rate | Original + OpenAI strict mode, JSONSchemaBench |
| H2 | Dedicated rules section reduces instruction-following errors | Original + Geng et al. AAAI 2026, Wallace et al. 2024 |
| H3 | Checklist/verify step improves factuality | Original + Commey 2026 |
| H4 | Constrained decoding yields higher validity | Original + XGrammar, CRANE, Tam et al. |
| H5 | DSPy-optimized RPO beats static RPO | Original + MPO, PromptWizard |
| H6 | Byte-identical rendering eliminates 40-76pp format variance | Sclar ICLR 2024, He et al. 2024 |
| H7 | Fixed section ordering eliminates order-dependency variance | McIlroy-Young 2024, Guan et al. 2025 |
| H8 | Section-level optimization beats monolithic optimization | Sharma & Henley 2026 (MPO) |
| H9 | Input-side enforcement avoids reasoning penalty of output constraints | Park NeurIPS 2024, Tam EMNLP 2024, CRANE |
| H10 | RPO caching alignment reduces per-turn cost by 70%+ | Prompt Cache MLSys 2024, Anthropic/OpenAI caching |
| H11 | Snapshot testing catches 50%+ of silent model regressions | Ma CAIN 2024, Chen 2023 |
| H12 | RPO achieves >90% prompt change documentation rate (vs. 21.9% baseline) | Tafreshipour MSR 2025 |

---

## Gaps Identified

1. **No head-to-head "structured prompt IR vs. freeform" study.** No paper compares a structured prompt *architecture* (RPO-style sections) against an equivalent monolithic prompt measuring both quality and cost. This is the study RPO should commission.

2. **No cross-provider rendering study.** No study tests whether rendering the same semantic content in different formats for different models yields a Pareto improvement. This is RPO's core value proposition.

3. **Pre-hoc vs. post-hoc compression.** No study measures whether structural organization (RPO) reduces the need for post-hoc compression (LLMLingua). Testable and novel.

4. **`warm_state` as a concept is unvalidated.** RPO's separation of persistent context (facts, decisions) from hot task content has intuitive appeal but no direct empirical support. Needs a controlled experiment.
