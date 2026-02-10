# RPO academic research — annotated bibliography (2026-02-10)

Purpose: collect academic research that supports (or stress-tests) the RPO idea: **structured prompts with explicit sections (rules/context/task/output contract), prompt contracts, constrained outputs, checklists, and prompt programming languages**.

## 1-page synthesis: what the literature implies for “RPO”

**RPO framing:** treat prompts as *interfaces* — a “contract” between user intent and model behavior.

### Pillar 1) Prompt as program / prompt as specification
Work like **LMQL** and **DSPy** formalizes prompting with **variables, constraints, control flow, and optimization loops**. This is “prompt contracts” implemented as code: you don’t just *ask* for JSON; you *constrain* or *compile* generations toward a schema/goal metric.

**Implication:** RPO should be designed like an API: typed fields, explicit invariants, and defined failure modes (what to do when constraints can’t be satisfied).

### Pillar 2) Reliability via decomposition + self-verification
**CoT / least-to-most / ToT / ReAct / Reflexion / PoT / PAL** show consistent gains when you (a) decompose tasks, (b) separate reasoning from execution, (c) search over candidates, and/or (d) incorporate feedback or tool outputs.

**Implication:** RPO “checklists” and structured sections aren’t only formatting — they are *cognitive scaffolds* that reduce instruction conflict and increase controllability.

### Pillar 3) Evaluation needs behavioral tests, not just average accuracy
**CheckList**, **HELM**, **BIG-bench**, **BBH** support systematic evaluation of robustness, failure modes, and generalization.

**Implication:** For RPO, define **contract compliance metrics**: schema validity rate, constraint satisfaction rate, refusal correctness, calibration/uncertainty behavior, instruction hierarchy robustness, and cost/latency.

### Cross-cutting hypotheses worth testing
- **H1 (Contract compliance):** an explicit “Output Contract” section increases **parseable structured-output rate** and reduces post-processing repairs.
- **H2 (Conflict handling):** a dedicated “Rules / Priority” section reduces instruction-following errors under conflicting constraints.
- **H3 (Self-check):** adding a final “Checklist / Verify” step improves factuality/consistency.
- **H4 (Programmatic constraints):** “ask for JSON” → “constrain decoding / typed variables” yields higher validity at equal or lower cost.
- **H5 (Optimization loop):** prompts treated as parameters optimized against a metric (DSPy) beat static templates in accuracy and robustness.

---

## Annotated bibliography (20 items)

### Theme A — Prompt programming languages, “prompt as code”, and prompt tooling

1) **Fischer et al. (2023). _Prompting Is Programming: A Query Language for Large Language Models (LMQL)._ PLDI’23.**  
Link: https://arxiv.org/abs/2212.06094  
Summary: LMQL is a language for *language model programming* with **control flow + constraints** over generations, compiled into efficient inference that can reduce cost while maintaining/improving accuracy.  
Implication for RPO: “Output contracts” can be enforceable (not aspirational) via constraints/typed slots.  
Hypothesis: constrained variables (LMQL-style) yield higher schema-valid rate (e.g., JSON parse success) than plain-text instructions at similar temperature.

2) **Khattab et al. (2023). _DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines._**  
Link: https://arxiv.org/abs/2310.03714  
Summary: Replaces hand-written prompt strings with **declarative modules** and a compiler that optimizes pipelines against a metric (bootstrapping demos, etc.).  
Implication for RPO: RPO templates become **optimizable artifacts**; “rules/context/task/contract” sections can be tuned for a given metric.  
Hypothesis: DSPy-optimized RPO templates outperform static RPO templates by ≥X% on held-out tasks (accuracy + contract compliance).

3) **Bach et al. (2022). _PromptSource: An Integrated Development Environment and Repository for Natural Language Prompts._ ACL’22 Demo.**  
Link: https://arxiv.org/abs/2202.01279  
Summary: Prompt templating language + IDE workflow for creating/sharing prompts tied to datasets; iteration via many examples.  
Implication for RPO: RPO should have versioning, linting, and test suites — treat prompts like code with CI.  
Hypothesis: prompt IDE + test harness reduces regression rate when editing RPO prompts.

### Theme B — Structured prompting for reasoning & controllability (decomposition, search, tool-use)

4) **Wei et al. (2022). _Chain-of-Thought Prompting Elicits Reasoning in Large Language Models._**  
Link: https://arxiv.org/abs/2201.11903  
Summary: Few-shot reasoning traces improve multi-step reasoning on arithmetic/commonsense/symbolic tasks.  
Implication: “Task” section can mandate intermediate artifacts (plans, rationales) as part of the contract when helpful.  
Hypothesis: requiring an intermediate “Plan” artifact increases multi-step accuracy without unacceptable hallucination increase.

5) **Kojima et al. (2022). _Large Language Models are Zero-Shot Reasoners._**  
Link: https://arxiv.org/abs/2205.11916  
Summary: Simple trigger (“Let’s think step by step”) yields zero-shot reasoning gains.  
Implication: standardized “reasoning mode” cues in Rules can be high leverage.  
Hypothesis: a standardized RPO reasoning snippet improves zero-shot performance vs ad-hoc phrasing.

6) **Wang et al. (2023). _Self-Consistency Improves Chain of Thought Reasoning in Language Models._ ICLR’23.**  
Link: https://arxiv.org/abs/2203.11171  
Summary: Sample multiple reasoning paths and marginalize to the most consistent answer; gains on GSM8K etc.  
Implication: contract can specify n-sample + consensus as a reliability mode.  
Hypothesis: self-consistency increases accuracy and decreases variance vs single-sample CoT at same expected token budget.

7) **Zhou et al. (2022). _Least-to-Most Prompting Enables Complex Reasoning in Large Language Models._**  
Link: https://arxiv.org/abs/2205.10625  
Summary: Decompose hard problems into subproblems; solve incrementally; improves easy-to-hard generalization.  
Implication: RPO can enforce a “Decompose → Solve → Compose” checklist section.  
Hypothesis: least-to-most RPO structure yields higher accuracy on harder-than-exemplar tasks.

8) **Yao et al. (2023). _Tree of Thoughts: Deliberate Problem Solving with Large Language Models._ NeurIPS’23.**  
Link: https://arxiv.org/abs/2305.10601  
Summary: Search over “thoughts” with self-evaluation/backtracking; gains on planning/search tasks.  
Implication: Rules can specify search budget, evaluation criteria, and stop conditions (process contract).  
Hypothesis: ToT-style prompting increases success rate on planning tasks at fixed compute vs linear CoT.

9) **Yao et al. (2022). _ReAct: Synergizing Reasoning and Acting in Language Models._**  
Link: https://arxiv.org/abs/2210.03629  
Summary: Interleaves reasoning with tool actions; reduces hallucination and improves interpretability.  
Implication: separate “thinking artifacts” from “actions/tool I/O” and define allowed actions.  
Hypothesis: explicit action schema reduces hallucinated citations/facts vs pure CoT on open-domain QA.

10) **Shinn et al. (2023). _Reflexion: Language Agents with Verbal Reinforcement Learning._**  
Link: https://arxiv.org/abs/2303.11366  
Summary: Reflection on feedback improves subsequent trials; boosts pass@1 on coding benchmarks.  
Implication: add “Postmortem/Reflection” section for iterative workflows; define memory format.  
Hypothesis: structured reflection memory improves success over N episodes vs no memory.

11) **Chen et al. (2022). _Program of Thoughts Prompting (PoT): Disentangling Computation from Reasoning._**  
Link: https://arxiv.org/abs/2211.12588  
Summary: Have LMs produce programs; execute externally; reduces computation errors.  
Implication: require executable intermediate representations (code/DSL) as contract artifacts.  
Hypothesis: program-based intermediate outputs reduce arithmetic/logical errors vs natural-language reasoning.

12) **Gao et al. (2022). _PAL: Program-aided Language Models._**  
Link: https://arxiv.org/abs/2211.10435  
Summary: LLM generates runnable steps; interpreter executes; improves math/symbolic tasks.  
Implication: contract specifies when to output code vs final answer and how to handle execution failures.  
Hypothesis: tool-routed computation yields higher correctness and better calibration.

### Theme C — “Rules” as governance: instruction-following, constitutions, and alignment

13) **Bai et al. (2022). _Constitutional AI: Harmlessness from AI Feedback._**  
Link: https://arxiv.org/abs/2212.08073  
Summary: Uses a “constitution” (rule set) plus self-critique/revision for safer outputs.
Implication: first-class “Rules/Constitution” section is a mechanism for consistent constraint application and self-revision.
Hypothesis: explicit constitutional rules increase refusal correctness and reduce policy violations under adversarial prompts.

14) **Ouyang et al. (2022). _Training language models to follow instructions with human feedback (InstructGPT)._**  
Link: https://arxiv.org/abs/2203.02155  
Summary: RLHF improves instruction-following and preference alignment.
Implication: RPO structure should align with instruction-tuned training: clear instruction boundaries, preferences, and delimiters.
Hypothesis: RPO prompts with clear delimitation reduce “instruction bleed” errors vs unstructured prompts.

15) **Chung et al. (2022). _Scaling Instruction-Finetuned Language Models (FLAN)._**  
Link: https://arxiv.org/abs/2210.11416  
Summary: Scaling instruction finetuning improves generalization across prompting setups.
Implication: RPO format should generalize across model families; standard structure may reduce brittleness.
Hypothesis: RPO structure maintains higher cross-model transfer than idiosyncratic prompts.

### Theme D — Constrained / contract-style outputs (decoding constraints; enforceable invariants)

16) **Hokamp & Liu (2017). _Lexically Constrained Decoding for Sequence Generation Using Grid Beam Search._ ACL’17.**  
Link: https://arxiv.org/abs/1704.07138  
Summary: Grid beam search guarantees inclusion of specified words/phrases.
Implication: strong form of output contract: enforce required keys/markers via decoding constraints.
Hypothesis: constrained decoding increases mandatory-field inclusion to ~100% with acceptable quality/cost tradeoff.

### Theme E — Reliability/factuality checks & behavioral evaluation (checklists, benchmarks, holistic eval)

17) **Manakul et al. (2023). _SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection for Generative LLMs._**  
Link: https://arxiv.org/abs/2303.08896  
Summary: Detect hallucinations via inconsistency across multiple sampled responses.
Implication: checklist can include a “consistency self-check” step with thresholds.
Hypothesis: adding SelfCheck-style self-check reduces hallucination rate; quantify tradeoff vs extra samples.

18) **Ribeiro et al. (2020). _Beyond Accuracy: Behavioral Testing of NLP Models with CheckList._ ACL’20.**  
Link: https://arxiv.org/abs/2005.04118  
Summary: Behavioral test design (capability × test type) to find bugs beyond aggregate accuracy.
Implication: build an RPO compliance test matrix and run in CI.
Hypothesis: CheckList-style suites uncover more RPO failure modes than random sampling.

19) **Bommasani et al. (2022). _Holistic Evaluation of Language Models (HELM)._**  
Link: https://arxiv.org/abs/2211.09110  
Summary: Multi-metric evaluation framework (accuracy, calibration, robustness, bias, toxicity, efficiency, etc.).
Implication: evaluate prompts across dimensions: correctness, robustness, cost/latency, compliance.
Hypothesis: RPO templates optimized for one metric may regress others; HELM-style dashboards catch this.

20) **Srivastava et al. (2022). _Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models (BIG-bench)._**  
Link: https://arxiv.org/abs/2206.04615  
Summary: Large benchmark; highlights brittleness and emergent behaviors.
Implication: test RPO across diverse tasks and prompt variations.
Hypothesis: RPO improves average performance but may have regressions; measure per-category deltas.

Optional stress suite:
- **Suzgun et al. (2022). _Challenging BIG-Bench Tasks and Whether Chain-of-Thought Can Solve Them (BBH)._** https://arxiv.org/abs/2210.09261
