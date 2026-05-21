According to the WMT26 task page last updated on **May 8, 2026**, I would **keep the first-draft idea, but tighten it**. The final approach should not be framed as “we fine-tuned Qwen on better data.” It should be framed as:

> **A single submitted Qwen3.5-2B model built by decomposing low-resource multilingual ability into trainable skill vectors, then recomposing those skills through interference-aware merging.**

That is the key research story. The “go big” contribution is not just data collection. It is **data construction + specialist training + one-model recomposition under WMT26’s equal-task constraint**.

## The WMT26 constraints that define the approach

The official WMT26 setup is very clear on four things.

First, each submitted track must cover **all five tasks**: MT, QA, spell checking, grammar checking, and math reasoning. You cannot submit only MT or only QA. The five task outputs must be generated from the **same model**. The allowed base is **Qwen3.5-2B**, or a quantized/Unsloth variant of the Qwen3.5 family at 2B parameters or less. ([Statistical Machine Translation][1])

Second, the final ranking weights the five tasks equally: MT is evaluated with chrF++ and BLEU, QA/MR with accuracy, and SC/GC with F1 for detection and correction. So the real objective is not “maximize translation.” It is “maximize the average of five different capabilities without negative transfer.” ([Statistical Machine Translation][1])

Third, external data is allowed, but it should be **publicly available for reproducibility**. The GitHub README also explicitly warns against using evaluation benchmark contamination: UNLP/MMLU test splits for Ukrainian QA, any original/modified/translated PolyMath version for MR, Sorbian certificate questions, and WMT2025 test sets. ([GitHub][2])

Fourth, WMT26 is explicitly about **synergy and interference**: the organizers ask whether MT training hurts QA, whether grammar checking helps MT, and whether the model can improve one task while preserving others. That means our system should be designed around **controlling interference**, not merely around collecting more examples. ([Statistical Machine Translation][1])

So yes: the first draft is directionally right. But I would revise it into a more disciplined final design.

# Finalized approach

## Name

I would call it:

> **Skill-Vector Merged Curriculum Adaptation for Low-Resource Multitask LLMs**

Internally, we can still think of it as the “Low-Resource Language School,” but the paper/submission framing should emphasize **skill vectors**, **curriculum generation**, and **interference-aware merging**.

The core hypothesis:

> In WMT26, a single 2B model can be improved more reliably by first learning separable language/task skills and then merging them into one final model than by training one large multitask mixture end-to-end.

That is more interesting than generic SFT.

---

# Why this is grounded in last year’s evidence

Last year’s most important result was TartuNLP’s Sorbian system. They did not merely do normal supervised fine-tuning. They continued pretraining Qwen2.5-3B-Instruct on a mixture of Sorbian monolingual data, parallel translation data, and instruction-following data, explicitly combining **language acquisition** and **instruction-following** in one step. Their system ranked highest in both Sorbian tracks. ([ACL Anthology][3])

Their later analysis is even more important: they found that task/language-specific continued pretraining improved the model, that joint Upper/Lower Sorbian training was beneficial, and that instruction data helped preserve broader model behavior. This directly supports our Stage 1: language acquisition should not be isolated from instruction-following. ([ACL Anthology][4])

JGU Mainz also gives useful lessons. They used backtranslation for Sorbian MT, translated many English MCQ datasets for QA, used RAG for Ukrainian QA, used similarity-based few-shot examples for MT, and reduced QA label/order bias by evaluating shuffled option orders. ([Statistical Machine Translation][5])

But WMT26’s model-submission format makes live RAG or complex inference-time pipelines risky unless explicitly allowed. So we should borrow JGU’s insight but change the form: **use retrieval and teachers during data construction/training, then distill that behavior into the final submitted model weights**. JGU’s paper also noted Ukrainian MT weaknesses due to lack of training data and a mismatch between sentence-level training and document/conversation-style test inputs, which should inform our Ukrainian MT curriculum. ([Statistical Machine Translation][5])

So the approach is not invented from nowhere. It combines:

1. **TartuNLP’s language acquisition + instruction training insight**.
2. **JGU’s data augmentation, QA robustness, and retrieval insight**.
3. **A new WMT26-specific answer to the one-model/five-task interference problem: specialist skill vectors merged into one model.**

---

# The final design

## Stage 0: governance and evaluation firewall

Before any “clever” modeling, we need a strict data policy.

We create a public/reproducible data registry with every source labeled:

```text
source
language
task
license
public availability
allowed / risky / forbidden
used for train / tune / locked validation
contamination notes
```

This is not busywork. It is necessary because WMT26 allows public external data but warns against benchmark contamination, especially PolyMath, MMLU/UNLP test splits, Sorbian certificate questions, and WMT2025 test sets. ([GitHub][2])

My policy would be:

> Official dev data is for format inspection, prompt design, and local evaluation. We do not dump all dev data into training during method development.

For larger dev sets, we split them into a **tune/dev-train portion** and a **locked validation portion**. For tiny MR dev sets, we mostly use them to understand format and difficulty, not to train. WMT26 only provides 12 low/medium MR questions during development, with the full test set later, so overfitting these examples would be especially dangerous. ([Statistical Machine Translation][1])

Final optional step: after the approach is frozen, we can decide whether to include more official dev examples in the final training run, but only if the rules do not prohibit it and we report it cleanly.

---

## Stage 1: language acquisition curriculum

This stage is inspired by TartuNLP, but expanded for WMT26.

The goal is not “teach tasks” yet. The goal is to make Qwen3.5-2B more comfortable with Ukrainian, Upper Sorbian, Lower Sorbian, and the relevant neighboring languages.

For **Sorbian**, this is crucial. WMT26 merges Upper and Lower Sorbian into one Sorbian track and requires all six directions:

```text
German ↔ Upper Sorbian
German ↔ Lower Sorbian
Upper Sorbian ↔ Lower Sorbian
```

The official task page also explicitly points to prior WMT very-low-resource resources, WMT2025 data, Leipzig monolingual data, the new Witaj-Sprachzentrum corpora, and Czech/Polish as related higher-resource languages. ([Statistical Machine Translation][1])

So Sorbian language acquisition should include:

```text
hsb monolingual
dsb monolingual
German–hsb parallel
German–dsb parallel
hsb–dsb parallel
allowed WMT2025/WMT2020–2022 resources
Czech transfer data for Upper Sorbian
Polish transfer data for Lower Sorbian
controlled grammar/lexicon drills
```

For **Ukrainian**, the goal is different. Ukrainian is mid-resource and Qwen likely has more prior exposure. The risk is less “the model cannot read Ukrainian” and more “we damage its reasoning or make it overfit to narrow translation behavior.” Ukrainian language acquisition should therefore be lighter and more targeted:

```text
public Ukrainian monolingual
public English–Ukrainian parallel
public Czech–Ukrainian parallel
document-level translation examples
conversation-style translation examples
Ukrainian educational/domain text for QA grounding
```

The document/conversation point matters because last year’s Ukrainian MT systems had trouble when evaluation inputs differed from sentence-level training. ([Statistical Machine Translation][5])

---

## Stage 2: public task compilers

This is the first major novelty. We do not merely “find data.” We build **task compilers** that generate controlled, reproducible training examples from public sources.

The WMT26 repo gives real training data for some things, but many tasks are mostly dev-only. The missing training signal becomes our opportunity.

### MT compiler

The MT compiler creates translation supervision from:

```text
official parallel data
allowed prior WMT data
public parallel corpora
backtranslation
round-trip consistency
Sorbian triangle consistency
document-level Ukrainian examples
```

For Sorbian, the special opportunity is the triangle:

```text
de ↔ hsb
de ↔ dsb
hsb ↔ dsb
```

We can exploit consistency:

```text
de → hsb → de should preserve meaning
de → dsb → de should preserve meaning
hsb → dsb → hsb should preserve meaning
de → hsb → dsb should agree with de → dsb
de → dsb → hsb should agree with de → hsb
```

This is very specific to WMT26 because the Sorbian track now includes both Sorbian languages and all six directions. ([Statistical Machine Translation][1])

For Ukrainian, the MT compiler should include **anti-summarization** examples: long input, paragraph preservation, dialogue preservation, and faithful translation rather than compressed paraphrase. That directly attacks last year’s Ukrainian MT failure mode.

### SC compiler

The spell-checking task asks for one wrong word and one correction; a sentence can have up to two spelling mistakes in one word, and it can also be correct. ([Statistical Machine Translation][1])

So the spell-check compiler generates examples like:

```text
clean sentence → inject typo into exactly one word → wrong word / correct word
clean sentence → no error → CORRECT behavior
```

But it should be language-aware:

```text
Ukrainian Cyrillic confusions
Sorbian diacritic deletion/substitution
keyboard-neighbor substitutions
OCR-like substitutions
single-character insertion/deletion
two-character corruptions
punctuation-preserving examples
```

This is likely a high-ROI task because many teams will underbuild it.

### GC compiler

The grammar-checking task is similar but morphosyntactic: one grammatical error in one word, or no error. ([Statistical Machine Translation][1])

The grammar compiler should generate **minimal pairs**, not random corruption:

```text
correct case → wrong case
correct number → wrong number
correct gender agreement → wrong gender
correct verb person/tense → wrong form
correct adjective-noun agreement → wrong adjective form
correct preposition-case pairing → wrong case
```

This is where the “language school” idea becomes real. We are not simply training the model to rewrite sentences. We are training it to identify exactly one local linguistic failure.

### QA compiler

For Ukrainian, WMT26 uses ZNO-style data and Ukrainian MMLU; for Sorbian, it uses language-certificate-style data and includes a hidden Upper Sorbian QA set. ([Statistical Machine Translation][1])

The QA compiler should create public, reproducible multiple-choice examples from:

```text
public Ukrainian educational material
public Ukrainian history/literature/geography/language resources
public Sorbian language-learning/cultural material
public bilingual educational resources
```

We should also incorporate JGU’s answer-order insight. They found that label choice and option ordering affected QA performance, and that averaging over shuffled orders helped. ([Statistical Machine Translation][5])

Since WMT26 likely evaluates hidden data from the submitted model, we should train the model to be invariant to:

```text
A/B/C/D labels
0/1/2/3 labels
answer order
distractor order
question phrasing
```

If inference-time option shuffling is allowed, it may help. But our core approach should not depend on it.

### MR compiler

For math reasoning, the rule is strict: WMT26 evaluates a translated, manually verified version of Qwen PolyMath, and participants are asked to avoid the original or translated PolyMath benchmark for training or inference. ([Statistical Machine Translation][1])

Therefore:

```text
No PolyMath.
No translated PolyMath.
No modified PolyMath.
No “PolyMath-like” reconstruction from dev examples.
```

Instead, use public unrelated math datasets and translated/rephrased math curricula. The objective is modest:

```text
preserve Qwen’s base math ability
teach final-answer formatting
teach target-language math phrasing
avoid harming MT/QA/SC/GC
```

This is not where we should over-optimize. Overtraining math could easily hurt the other tasks.

---

## Stage 3: specialist skill training

This is the centerpiece.

Instead of one giant multitask training run, we train several specialist adaptations from the same base or from the same language-adapted checkpoint:

```text
M_lang      language acquisition
M_mt        translation
M_edit      spell + grammar checking
M_qa        multiple-choice QA
M_mr        math reasoning / answer formatting
M_format    exact WMT output behavior
```

These are **not** final models. They are not separate adapters we switch at inference time. They are sources of skill deltas.

This matters because WMT26 says all five tasks for a track must be generated from the same model. So task-specific inference adapters are risky. But training specialists and then merging them into one final set of weights is aligned with the one-model requirement.

LoRA/QLoRA is a good practical mechanism here because LoRA freezes the base model and trains low-rank adaptation matrices, greatly reducing trainable parameters while preserving the base model’s general behavior. ([arXiv][6])

But conceptually, the important thing is not “LoRA.” It is:

> Train skills separately enough to measure them, then recombine them deliberately.

---

## Stage 4: interference-aware model merging

This is the second major novelty.

We turn each specialist into a skill vector:

```text
Δ_lang   = M_lang   - M_base
Δ_mt     = M_mt     - M_base
Δ_edit   = M_edit   - M_base
Δ_qa     = M_qa     - M_base
Δ_mr     = M_mr     - M_base
Δ_format = M_format - M_base
```

Then we search for a merged model:

```text
M_final = M_base
        + aΔ_lang
        + bΔ_mt
        + cΔ_edit
        + dΔ_qa
        + eΔ_mr
        + fΔ_format
```

The merge is optimized against our locked local validation score using WMT26’s equal-task logic. This directly addresses the competition’s real challenge: avoiding negative transfer.

This is grounded in existing work. “Model soups” showed that averaging multiple fine-tuned models can improve accuracy and robustness without adding inference cost. TIES-Merging was specifically proposed to reduce interference when merging task-specific models by dealing with redundant changes and sign conflicts. ([Proceedings of Machine Learning Research][7])

The reason this is especially attractive for WMT26 is that it produces **one final model**. No ensemble. No router. No per-task adapter switching. No extra inference stack.

That gives us a strong paper claim:

> We satisfy the WMT26 same-model constraint by learning task skills separately and recomposing them into one model through interference-aware merging.

---

## Stage 5: final behavior polish

The final pass is not about adding knowledge. It is about preventing evaluation-killing behavior.

For WMT26, outputs are brittle:

```text
QA/MR: accuracy depends on the correct answer format
SC/GC: F1 depends on exact wrong-word and correction extraction
MT: chrF++/BLEU punish hallucination, summarization, and formatting drift
```

So the final polish should train preferences like:

```text
chosen: exact required output
rejected: verbose explanation

chosen: wrong word + corrected word
rejected: full sentence rewrite

chosen: CORRECT when no error
rejected: hallucinated error

chosen: answer label only
rejected: long reasoning when label requested

chosen: faithful translation
rejected: summary-like translation
```

This could be DPO, contrastive SFT, or another preference-style pass. The exact implementation can wait. The conceptual point is:

> The final polish is about evaluation behavior, not broad capability acquisition.

---

# Track strategy: one model or two?

WMT26 has two leaderboards: Ukrainian and Sorbian. The rules say participants may submit one or both leaderboards, and for each track they must submit all five tasks from the same model. ([Statistical Machine Translation][1])

My recommendation:

> Build **one final merged model per track**: one Ukrainian model and one Sorbian model.

That is safer than one global Ukrainian+Sorbian model. It still respects the rules because each track’s five tasks come from the same model. A single global model for both tracks would be more ambitious, but it increases interference risk. We can mention a global variant as an ablation or secondary experiment, but the main leaderboard strategy should be track-specific final models.

So:

```text
Ukrainian final model:
- en→uk MT
- cs→uk MT
- Ukrainian QA
- Ukrainian SC
- Ukrainian GC
- Ukrainian MR

Sorbian final model:
- de↔hsb MT
- de↔dsb MT
- hsb↔dsb MT
- Sorbian QA
- Sorbian SC
- Sorbian GC
- Sorbian MR
```

Each is one model for its track.

---

# What we explicitly should not do

I would rule out these approaches as primary strategies:

**Do not rely on live RAG at final inference** unless the organizers explicitly confirm that custom inference pipelines are allowed. WMT26 emphasizes model submission for hidden evaluation, so retrieval should be used as a teacher during data construction, not as a required final-time component. ([Statistical Machine Translation][1])

**Do not switch task-specific adapters at inference.** Even if technically possible, it undermines the “same model” requirement. Specialist adapters are acceptable as training artifacts; the final submitted model should be a single merged model.

**Do not train on PolyMath or translated PolyMath.** That is explicitly discouraged for MR fairness. ([Statistical Machine Translation][1])

**Do not make MT dominate the mixture.** Last year already showed the risk: systems optimized around MT could hurt QA/general ability. WMT26’s equal weighting makes this even more dangerous.

**Do not treat SC/GC as afterthoughts.** They are new, exactly formatted, equal-weighted tasks. A strong SC/GC compiler may be one of the easiest ways to beat generic multitask SFT systems.

---

# The final research story

The paper/system description should not say:

> We collected public data and fine-tuned Qwen3.5-2B.

It should say:

> WMT26 requires one small model to perform five heterogeneous tasks under severe data scarcity. We propose a skill-vector curriculum approach: construct public task curricula for missing supervision, train specialist skill adaptations, merge the learned task vectors into a single model, and apply a final behavior-polishing step to satisfy exact WMT output formats.

The main contributions would be:

1. **A public low-resource curriculum/data factory** for MT, QA, SC, GC, and MR.
2. **Morphology-aware SC/GC compilers** for Ukrainian, Upper Sorbian, and Lower Sorbian.
3. **Triangle-consistency training for Sorbian MT** across German, Upper Sorbian, and Lower Sorbian.
4. **RAG-to-weights distillation** for QA instead of risky live retrieval.
5. **Interference-aware skill-vector merging** to satisfy the one-model/five-task WMT26 constraint.

That is the finalized approach I would commit to.

## My recommendation

Keep the first draft, but revise it into this final form:

```text
1. Data governance + contamination firewall
2. Language acquisition curriculum
3. Public task compilers
4. Specialist skill adaptation
5. Skill-vector / TIES-style merging into one final model
6. Final exact-format behavior polish
```

The centerpiece should be:

> **specialist skill vectors merged into one submitted model.**

The most distinctive supporting piece should be:

> **SC/GC morphology-aware compilers plus Sorbian triangle consistency.**

That gives us both a leaderboard strategy and a publishable story.

[1]: https://www2.statmt.org/wmt26/limited-resources-llm.html "Multitask LLMs with Limited Resources"
[2]: https://github.com/TUM-NLP/llms-limited-resources2026 "GitHub - TUM-NLP/llms-limited-resources2026: The GitHub repository for Multitask LLMs with Limited Resources @ WMT2026 shared task https://www2.statmt.org/wmt26/limited-resources-llm.html · GitHub"
[3]: https://aclanthology.org/2025.wmt-1.88/ "TartuNLP at WMT25 LLMs with Limited Resources for Slavic Languages Shared Task - ACL Anthology"
[4]: https://aclanthology.org/2025.wmt-1.88.pdf "TartuNLP at WMT25 LLMs with Limited Resources for Slavic Languages Shared Task"
[5]: https://www2.statmt.org/wmt25/pdf/2025.wmt-1.89.pdf "JGU Mainz's Submission to the WMT25 Shared Task on LLMs with Limited Resources for Slavic Languages: MT and QA"
[6]: https://arxiv.org/abs/2106.09685?utm_source=chatgpt.com "LoRA: Low-Rank Adaptation of Large Language Models"
[7]: https://proceedings.mlr.press/v162/wortsman22a.html?utm_source=chatgpt.com "Model soups: averaging weights of multiple fine-tuned models ..."


Yes. Before implementation, I would lock the strategy down as a **research approach**, not just a training recipe.

My revised recommendation is:

> **Skill-Merged Curriculum Adaptation for WMT26 Multitask Low-Resource LLMs**
> A single submitted model per track, trained through public/reproducible data compilers, task-specialist adaptations, and weight-space merging to reduce negative transfer across MT, QA, SC, GC, and MR.

This keeps the “go big” idea from the first draft, but sharpens it around the actual WMT26 rules.

---

## 1. The 2026 rules force the core research problem

The key WMT26 constraint is not just “use Qwen.” It is: **for each leaderboard, the same model must generate outputs for all five tasks: MT, QA, spell checking, grammar checking, and math reasoning.** Participants may submit to the Ukrainian track, the Sorbian track, or both, but for each track they must submit all five tasks, and the MT/QA/SC/GC/MR outputs must come from the same Qwen3.5-family 2B-or-smaller model. ([Statistical Machine Translation][1]) 

That means our central research question should be:

> **How do we teach a 2B LLM low-resource language ability without destroying the general instruction-following, QA, and math abilities it already has?**

This is exactly what the official task is trying to measure. The task page says the organizers want to study task synergy: whether MT training hurts QA, whether linguistic tasks like grammar checking help MT, and whether MT can improve while other capabilities remain stable. ([Statistical Machine Translation][1])

The final leaderboard also weights all five tasks equally: chrF++ for MT, accuracy for QA/MR, and F1 for SC/GC detection and correction. ([Statistical Machine Translation][1]) So a system that crushes translation but forgets QA or math is strategically bad.

---

## 2. What the repo implies about data

You are also right that the repo is not a full conventional train/dev/test release for every task. The official page and GitHub make clear that external public data is expected/allowed, as long as it is publicly available for reproducibility. ([Statistical Machine Translation][1])

For Ukrainian, the repo gives MT **development** sets for English–Ukrainian and Czech–Ukrainian, and real QA train/dev data for ZNO and Ukrainian MMLU. The Ukrainian folder lists 2,450 ZNO train questions, 1,531 Ukrainian MMLU train questions, and dev splits for both; it also lists 2,000 SC examples, 2,000 GC examples, and only 24 MR examples. ([GitHub][2])

For Sorbian, the repo is much stronger on MT: it provides new parallel training corpora for de–hsb, de–dsb, and hsb–dsb, plus monolingual corpora with 512,671 Upper Sorbian sentences and 38,028 Lower Sorbian sentences. But Sorbian QA is tiny, and SC/GC/MR are mostly development-style supervision. ([GitHub][3])

So the practical interpretation is:

> **WMT26 is a public-data construction and negative-transfer mitigation challenge.**

The official warning is important: do **not** use UNLP/MMLU test splits, any original/modified/translated PolyMath benchmark, Sorbian certificate questions beyond what they provide, or WMT2025 test sets. ([GitHub][4])

That shapes our whole approach.

---

## 3. What WMT25 teaches us

Last year’s shared task had only MT + QA, but the lessons are directly relevant.

The WMT25 findings paper reports that all submissions improved over the baseline, but it also explicitly notes that **training purely on MT degraded QA capabilities**. ([ACL Anthology][5]) That is the exact failure mode we need to avoid in WMT26.

TartuNLP’s winning Sorbian system is the strongest precedent. They did not simply do task SFT. They continued pretraining Qwen2.5-3B-Instruct on Sorbian monolingual data, parallel MT data, and general instruction data together, “combining language acquisition and instruction-following in a single step,” and ranked highest in both MT and QA for hsb/dsb. ([ACL Anthology][6]) Their paper reports that MT data produced large translation gains, instruction data helped both MT and QA, reverse-direction MT helped slightly without hurting QA, and German monolingual data did not help. ([ACL Anthology][7])

TartuNLP also showed that separate MT SFT increased BLEU but damaged QA, so that strategy “does not satisfy the goals of the shared task.” They even tried merging back toward the base model with SLERP and saw slight QA recovery but translation harm at higher base weight. ([ACL Anthology][7])

JGU Mainz took a more pipeline-heavy approach: LoRA fine-tuning, added translation/QA data, translated English MCQs into target languages, RAG for Ukrainian QA, similarity-based few-shot retrieval for MT, and option-order probability averaging for QA to reduce positional bias. ([ACL Anthology][8]) NRC is the cautionary case: they focused primarily on MT, ranked first by chrF on MT, but underperformed on QA; their paper says they trained only for MT as their primary submission after unsatisfactory QA experiments. ([ACL Anthology][9])

So the WMT25 lesson is clear:

> The winning idea is not “more SFT.”
> The winning idea is **language adaptation + instruction preservation + explicit anti-forgetting strategy**.

For WMT26, with five equal-weighted tasks, that lesson becomes even more important.

---

# Finalized approach

## Name

I would use a more academic name than “Language School” in the paper:

> **Skill-Merged Curriculum Adaptation for Multitask Low-Resource LLMs**

Internally, we can still think of it as:

> **Skill-Vector Merged Low-Resource Language School**

The system has three pillars:

1. **Curriculum data factories** for the missing/weak tasks.
2. **Specialist skill adaptations** trained from a shared checkpoint.
3. **Weight-space merging** into one final submitted model.

The novelty is not that we fine-tune. Everyone will fine-tune. The novelty is that we treat WMT26 as a **multi-skill interference problem** and use data compilers + model merging to construct one Pareto-balanced model.

---

## 4. Track strategy: probably two submitted models, not one giant model

The WMT26 page defines two leaderboards: Ukrainian and Sorbian. For each track, all five tasks must come from the same model. It does **not** appear to require the same model across Ukrainian and Sorbian leaderboards. ([Statistical Machine Translation][1])

So the best practical strategy is:

```text
Model A: Ukrainian-track model
- uk MT, QA, SC, GC, MR

Model B: Sorbian-track model
- hsb + dsb MT, QA, SC, GC, MR
- all six Sorbian MT directions
```

The Sorbian model absolutely must be unified for hsb and dsb because WMT26 merges the Sorbian tracks and requires one model for all six directions. ([Statistical Machine Translation][1])

A single universal uk+hsb+dsb model would be a nice ablation or paper appendix, but I would not make that the primary competitive strategy unless the organizers later clarify that one all-language model is required.

---

# 5. Stage 1: language acquisition without instruction collapse

This stage stays from the first draft, but we should be precise.

The goal is not just “continued pretraining.” The goal is:

> **Teach the low-resource language while preserving the base model’s general instruction behavior.**

For Sorbian, this stage is central. We use official hsb/dsb monolingual data, official Sorbian parallel data, allowed WMT2025/WMT2020–2022 Sorbian resources, public hsb/dsb text, and carefully selected related-language transfer from Czech and Polish. The official WMT26 page explicitly points to earlier WMT Sorbian data and notes Czech/Polish as closely related better-resourced languages. ([Statistical Machine Translation][1])

For Ukrainian, this stage should be lighter. Ukrainian is mid-resource and Qwen likely already has meaningful Ukrainian competence. Overtraining Ukrainian language modeling could waste budget or damage reasoning. Ukrainian should get targeted adaptation: document-level MT, QA-domain exposure, SC/GC linguistic precision, and format control.

This stage should mix:

```text
monolingual target-language text
parallel MT text
instruction-following data
grammar/orthography drills
short task-formatted examples
```

This directly follows the TartuNLP lesson: language acquisition and instruction following should be trained together, not as separate stages where MT later overwrites instruction behavior. ([ACL Anthology][7])

---

# 6. Stage 2: task compilers, not just scraped datasets

This is the part that can make the submission stand out.

Most teams will gather datasets. We should build **task-specific compilers**: controlled generators that create training signals aligned to the exact WMT26 tasks.

## MT compiler

For Sorbian:

```text
official de–hsb, de–dsb, hsb–dsb training data
both directions for all three pairs
backtranslation from monolingual hsb/dsb
triangle consistency: de → hsb → dsb should agree with de → dsb
cycle consistency: hsb → dsb → hsb should preserve meaning
related-language transfer from Czech/Polish where useful
```

This fits WMT26 particularly well because Sorbian now has a translation triangle: German, Upper Sorbian, and Lower Sorbian. The task explicitly evaluates all six Sorbian directions. ([Statistical Machine Translation][1])

For Ukrainian:

```text
public en–uk and cs–uk parallel data
domain-matched retrieval against the official dev distribution
document-level translation examples
anti-summarization translation examples
long-context paragraph-preserving translation
```

This is motivated by last year’s Ukrainian difficulty: when test examples are long or document-like, sentence-level translation training can produce summary-like behavior. JGU also had to collect public Ukrainian MT data because no Ukrainian MT train data was provided in WMT25. ([ACL Anthology][10])

## SC compiler

The SC task asks for the wrong word and the corrected word, or `CORRECT` if there is no spelling error. The official task says spelling examples can have up to two mistakes in one word. ([Statistical Machine Translation][1])

So we generate minimal spelling corruptions:

```text
diacritic removal/substitution
single-character insertion/deletion
keyboard-neighbor substitutions
OCR-like confusions
Cyrillic lookalike confusions for Ukrainian
Sorbian-specific character confusions
two-error-in-one-word cases
clean no-error cases
```

The point is not to flood the model with random noise. The point is to teach the model the exact behavior:

```text
Wrong word: X
Correct word: Y
```

## GC compiler

The GC task asks for one grammatical error in one word, such as wrong case or number, or `CORRECT` if there is no error. ([Statistical Machine Translation][1])

So we generate controlled morphology minimal pairs:

```text
wrong case ending
wrong number
wrong gender agreement
wrong adjective-noun agreement
wrong verb person/tense
wrong preposition-case combination
wrong inflected form that is itself a valid word
```

This is probably the most underexploited WMT26 opportunity. SC/GC are not merely auxiliary tasks. They force the model to learn morphology and word-form precision, which should help MT, especially for Sorbian.

## QA compiler

For Ukrainian QA, we can use the official train data plus public ZNO-like and Ukrainian educational material, while avoiding UNLP/MMLU test splits. For Sorbian QA, we must avoid extra Sorbian certificate questions, but we can create reading-comprehension and grammar MCQs from public hsb/dsb text and public language-learning material, provided licensing is clean. The GitHub README explicitly warns against using Sorbian language certificate questions beyond the provided material. ([GitHub][4])

The JGU precedent is useful but should be modified. They used translated English MCQs and RAG for Ukrainian QA. ([ACL Anthology][10]) For WMT26, because the model itself is submitted for hidden evaluation, I would not rely on test-time RAG. Instead:

> Use retrieval during data construction, then distill the knowledge into the model.

That gives us:

```text
public source text → generated MCQ → verified answer → training example
```

The submitted model then answers without external retrieval.

## MR compiler

The MR task is based on translated, manually verified Qwen PolyMath low/medium problems, but the organizers explicitly ask participants not to use the original or translated PolyMath benchmark for training or inference. ([Statistical Machine Translation][1])

So the MR compiler should use only public **non-PolyMath** math-reasoning data. The goal is not to specialize aggressively on math; it is to preserve Qwen’s base reasoning while teaching Ukrainian/Sorbian prompt formats and final-answer discipline.

```text
public non-PolyMath math problems
low/medium difficulty only
translated or rewritten into target languages
strict final-answer format
small amount of reasoning-format training
```

This should be a preservation stage, not a huge math fine-tune.

---

# 7. Stage 3: train specialists, but never submit specialists

This is the key difference from generic multitask SFT.

Instead of training one giant mixed dataset and hoping the sampling ratios are right, we train several specialist adaptations from the same parent checkpoint:

```text
Language specialist
MT specialist
SC/GC edit specialist
QA specialist
MR preservation specialist
Format-control specialist
```

Each specialist learns a different “skill direction.” But we do **not** use task-specific adapters at inference. That would violate the spirit, and possibly the letter, of the same-model requirement.

The final system must be:

```text
one architecture
one set of weights
one model per track
task-specific prompts allowed
no adapter switching
no hidden ensemble
```

This matters because WMT26 requires model submission for hidden evaluation, either publicly on Hugging Face or privately to the organizers. ([Statistical Machine Translation][1])

---

# 8. Stage 4: merge skill vectors into one final model

This is the centerpiece.

The model-merging idea is well grounded. “Model soups” showed that averaging weights of multiple fine-tuned models can improve accuracy and robustness without extra inference cost. ([Proceedings of Machine Learning Research][11]) Task arithmetic treats the difference between a fine-tuned model and its base as a task vector in weight space. ([OpenReview][12]) TIES-Merging specifically addresses interference when merging multiple task-specific models by trimming small updates and resolving sign conflicts. ([arXiv][13])

So our approach becomes:

```text
Base/language-adapted checkpoint
  + MT skill vector
  + SC/GC skill vector
  + QA skill vector
  + MR skill vector
  + format-control skill vector
= one final submitted model
```

Why this is better than plain multitask SFT:

```text
Plain SFT question:
What sampling ratio should I use?

Skill-merge question:
What combination of learned capabilities gives the best equal-weighted WMT score?
```

That directly matches the WMT26 objective. The official ranking treats all five tasks equally, so we should optimize a five-task Pareto balance rather than maximize MT alone. ([GitHub][4])

This also gives us a strong paper story:

> **We reduce negative transfer in WMT26 by training task-specialist skill vectors and merging them into a single compliant model.**

That is much more interesting than “we fine-tuned Qwen on more data.”

---

# 9. Stage 5: small preference/format polish

The final polish should be small and targeted. I would not make a massive DPO run the main strategy. It can easily overfit the dev format or erase useful merged behavior.

But a small preference step is useful because WMT26 has brittle output formats:

```text
SC/GC:
Wrong word: ...
Correct word: ...

QA/MR:
exact answer label or final answer

MT:
translation only, no explanation, no summary
```

Direct Preference Optimization is appropriate here because it optimizes chosen/rejected response pairs directly, without a separate reward model or RL loop. ([NeurIPS Papers][14])

The chosen/rejected pairs should attack predictable evaluation failures:

```text
chosen: exact two-line SC/GC output
rejected: full-sentence rewrite

chosen: CORRECT when no error exists
rejected: hallucinated correction

chosen: answer label only
rejected: verbose explanation with the answer buried inside

chosen: faithful translation
rejected: summary-like translation

chosen: final numeric answer
rejected: chain-of-thought-style rambling
```

This is not about making the model “nicer.” It is about preventing metric-killing format failures.

---

# 10. What changes from the first draft

I would keep the original skeleton, but revise it in five ways.

First, I would use **one final model per leaderboard**, not necessarily one model for all Ukrainian + Sorbian unless we decide to run that as an ablation. The Sorbian model must handle both hsb and dsb.

Second, I would make **model merging the central research contribution**, not just an optional trick.

Third, I would make **SC/GC compilers a major contribution**, because these are the new tasks where most teams may do something shallow.

Fourth, I would treat **RAG as a training-time data-generation/distillation tool**, not a test-time dependency.

Fifth, I would keep the official dev files mostly for validation, prompt inspection, and controlled final calibration. The released dev sets are too important to burn casually, especially since hidden test data arrives later and several tasks have tiny development sets. The task page says test data is released later, around late June 2026. ([Statistical Machine Translation][1])

---

# 11. Final approach by track

## Ukrainian track

Primary risks:

```text
MT has no official train file in the repo
SC/GC need synthetic training
MR has only tiny dev supervision
QA has real train data but contamination risk
```

The Ukrainian model should emphasize:

```text
public en–uk and cs–uk MT data
document-level / anti-summarization MT
official ZNO + Ukrainian MMLU train only
public Ukrainian educational QA, carefully filtered
synthetic Ukrainian SC/GC minimal pairs
small non-PolyMath Ukrainian math preservation data
format control
```

The research angle for Ukrainian:

> **Can synthetic linguistic editing and document-level translation adaptation improve Ukrainian MT/SC/GC while preserving QA and MR?**

## Sorbian track

Primary risks:

```text
very low-resource hsb/dsb
tiny QA
SC/GC mostly dev-style supervision
must handle six MT directions
hidden Upper Sorbian QA dataset
```

The Sorbian model should emphasize:

```text
official 2026 parallel + monolingual Sorbian data
allowed WMT2025 and prior WMT Sorbian data
joint hsb/dsb training
triangle consistency across de/hsb/dsb
public hsb/dsb grammar/orthography curriculum
synthetic SC/GC from monolingual sentences
CEFR-like generated QA from public text, not certificate leakage
non-PolyMath math format preservation
```

The research angle for Sorbian:

> **Can a synthetic language curriculum plus task-vector merging build one hsb/dsb model that handles translation, language exams, error correction, and reasoning?**

---

# 12. The final system description in one paragraph

Here is the version I would put at the top of the project plan:

> We develop a WMT26-compliant Qwen3.5-2B-based multitask system for low-resource Slavic languages. Rather than relying on a single multitask SFT mixture, we construct public, reproducible task-specific data compilers for translation, spelling correction, grammar correction, QA, and math-reasoning preservation. We first perform instruction-preserving language adaptation, then train task-specialist adaptations from the same checkpoint. These specialists are merged in weight space into a single final model per leaderboard, optimized against a held-out equal-weighted five-task validation score. A small final preference/format-alignment stage teaches exact WMT output behavior and reduces failures such as verbose QA answers, hallucinated corrections, and summary-like translations.

That is the finalized approach.

It is grounded in the 2026 guidelines, avoids known contamination traps, directly addresses the WMT25 failure mode, and gives us a real research contribution beyond “we collected data and fine-tuned Qwen.”

[1]: https://www2.statmt.org/wmt26/limited-resources-llm.html "Multitask LLMs with Limited Resources"
[2]: https://github.com/TUM-NLP/llms-limited-resources2026/tree/main/Ukrainian "llms-limited-resources2026/Ukrainian at main · TUM-NLP/llms-limited-resources2026 · GitHub"
[3]: https://github.com/TUM-NLP/llms-limited-resources2026/tree/main/Sorbian "llms-limited-resources2026/Sorbian at main · TUM-NLP/llms-limited-resources2026 · GitHub"
[4]: https://github.com/TUM-NLP/llms-limited-resources2026 "GitHub - TUM-NLP/llms-limited-resources2026: The GitHub repository for Multitask LLMs with Limited Resources @ WMT2026 shared task https://www2.statmt.org/wmt26/limited-resources-llm.html · GitHub"
[5]: https://aclanthology.org/2025.wmt-1.27/ "Findings of the WMT 2025 Shared Task LLMs with Limited Resources for Slavic Languages: MT and QA - ACL Anthology"
[6]: https://aclanthology.org/2025.wmt-1.88/ "TartuNLP at WMT25 LLMs with Limited Resources for Slavic Languages Shared Task - ACL Anthology"
[7]: https://aclanthology.org/2025.wmt-1.88.pdf "TartuNLP at WMT25 LLMs with Limited Resources for Slavic Languages Shared Task"
[8]: https://aclanthology.org/2025.wmt-1.89/ "JGU Mainz’s Submission to the WMT25 Shared Task on LLMs with Limited Resources for Slavic Languages: MT and QA - ACL Anthology"
[9]: https://aclanthology.org/2025.wmt-1.87/ "NRC Systems for the WMT2025-LRSL Shared Task - ACL Anthology"
[10]: https://aclanthology.org/2025.wmt-1.89.pdf "JGU Mainz's Submission to the WMT25 Shared Task on LLMs with Limited Resources for Slavic Languages: MT and QA"
[11]: https://proceedings.mlr.press/v162/wortsman22a.html?utm_source=chatgpt.com "Model soups: averaging weights of multiple fine-tuned models ..."
[12]: https://openreview.net/forum?id=6t0Kwf8-jrj&utm_source=chatgpt.com "Editing models with task arithmetic"
[13]: https://arxiv.org/abs/2306.01708?utm_source=chatgpt.com "TIES-Merging: Resolving Interference When Merging Models"
[14]: https://papers.nips.cc/paper/2023/hash/a85b405ed65c6477a4fe8302b5e06ce7-Abstract-Conference.html?utm_source=chatgpt.com "Direct Preference Optimization: Your Language Model is ..."
