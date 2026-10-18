# Independent audit of extension-001

**Verdict: computational PASS; make the editorial corrections below before manuscript integration.** No wrong optimum, missing basis, distance error, case-coverage mismatch or invalid noise certificate was found. All original extension files and previously reviewed manuscript/PDF/source-archive hashes remain unchanged. No new cases, paid services, network communications or publication were used.

## Independent reproduction

The auditor inspected the frozen protocol, report, draft addendum, all code, manifest and complete saved results. `../extension_audit.py` imports none of the extension modules and does not rerun the scientific runner. It reconstructs the ordered plan directly from the protocol and original seed records, including the seed, shared random stream, constant-assignment correction, first eligible degree-three attachment vertex and lexicographically first eligible nonedge. The planned cases agree exactly, including IDs and stored weighted edges. Input SHA-256 matches the original independently audited pilot graph file. The 71 seed graphs through order eight inherit that earlier complete isomorphism-class audit.

For every case, an independently written Bellman-Ford edge-relaxation routine computes all weighted distances, rather than the producer's Floyd-Warshall or Dijkstra. All weights are positive, graph edges are simple and valid, connectivity is checked, and degree/cycle-rank restrictions match each family. Exhaustive tuple-signature tables determine resolving sets. Deletion of each sensor uses those exhaustive tables without changing the graph. Every minimum base, FT minimum and smallest-mask constrained optimum is recomputed. All 68,576 saved subset-flag entries agree.

| Family | Cases | Bases | p=0 | p=1 | Exact labelled distinct cases |
|---|---:|---:|---:|---:|---:|
| Baseline | 71 | 697 | 679 | 18 | 71 |
| Weighted | 213 | 1,337 | 1,317 | 20 | 213 |
| Degree four | 28 | 278 | 198 | 80 | 28 |
| Bicyclic | 70 | 672 | 602 | 70 | 67 |
| Total | 382 | 2,984 | 2,796 | 188 | — |

There is no p>1 example in these cases. All cases completed, so no stopping-rule skip should occur and none does. The three repeated labelled bicyclic cases are accurately disclosed. No isomorphism-distinct or exhaustive weighted/topological coverage claim is justified beyond the original baseline seeds.

## Noise definition and certificates

The model is adversarial coordinatewise error in closed intervals of radius epsilon, with an identified erased coordinate. Target vertices, shortest-path distances, and the graph remain fixed. For two candidate targets, their error boxes intersect exactly when all surviving coordinate gaps are at most 2 epsilon. Therefore the strict inequality in the protocol is correct, including the failure of a universal guarantee at equality. Such failure means that an ambiguous allowed observation exists, not that all observations are ambiguous.

The independent audit enumerates every target pair and every possible erased sensor, taking the minimum of the largest surviving gap. It does not rely on the producer's second-largest-gap shortcut. It independently checks m1, m2 and every flag at epsilon=0,1/4,1/2,1. The expected selected-layout set agrees exactly: every minimum base, its smallest-mask optimum FT augmentation, and one smallest-mask unconstrained FT optimum. All **4,675** stored per-case unique-layout boundary certificates were checked, not only representatives. Each pair is valid, the erased sensor belongs to the layout, the surviving list is exactly correct, and the stored doubled midpoint lies in both closed error boxes at epsilon=m2/2. Singleton ordinary bases correctly leave no coordinate after erasure and have zero margin.

The reported augmentation counts are reproduced: all 2,984 rows pass at epsilon=1/4; among weighted rows 37 pass at 1/2 and 13 at 1. The weighted m2 histogram is 1:1,300; 2:24; 3:13. Weighted unconstrained selected optima pass in 213,8,1 cases at 1/4,1/2,1. Every ordinary minimum base has m2=0. These are deterministic basis-conditioned counts, possibly sharing layouts; they are not independent trials or probabilities. Margin-optimal ties and robust minimum sensor sets were not searched.

## Required corrections before integration

1. **Make the generic unit-edge implication explicit.** Replace any framing of the half-unit threshold as an experimental discovery with the following explanation:

   > For any connected unit-edge graph with at least two vertices and any exact fault-tolerant layout S, m2(S)=1. Integer distances and two distinguishers give m2(S)>=1. For adjacent targets u,v, the triangle inequality gives |d(u,s)-d(v,s)|<=1 for every sensor s, so m2(S)<=1. Consequently the worst-case one-erasure guarantee holds exactly for epsilon<1/2. The observed unit-edge thresholds are a consistency check of this generic fact, not a graph-class-specific discovery.

   Integrality alone gives the lower bound; the adjacent-pair triangle-inequality argument gives the upper bound. Do not say that all integer-weighted graphs have threshold 1/2. Likewise, all integer-distance FT layouts pass at epsilon=1/4 by integrality. Ordinary minimum bases having m2=0 follows from their minimality: removing any sensor cannot still resolve. These are expected consequences rather than new empirical findings. This clarification requires no new search or experiment.

2. **Qualify freeze/preregistration language.** Replace “frozen before any extension outcome was computed” and unqualified “preregistered” with “the local protocol, case plan and source hashes were recorded before the recorded run; the runner checked those hashes before solving.” Add that the files are a local freeze, not an independently timestamped preregistration. There is no evidence here of a protocol violation, but the available evidence cannot establish the absence of earlier unrecorded analyses.

3. **Update review status, without inflating it.** Replace the addendum's final “has not yet received independent review” sentence with “A separately authored executable audit reproduced the complete finite case plan, all optima and noise certificates; this is AI computational review, not human peer review or physical validation.” Link this report and its exact reviewed hashes. Manuscript integration still needs the author's editorial decision and does not authorize publication.

4. **Retain existing scope and scale cautions.** Do not modify the theorem's unweighted, subcubic, unicyclic hypotheses. The weighted/topological variants are finite, label-dependent stress tests, not evidence establishing a universal extension. Absolute weighted margins depend on edge-length units and do not establish improved physical sensing. The current addendum already correctly distinguishes these points; preserve them when shortening it.

No numerical table correction or scientific rerun is needed.

## Freeze evidence and gaps

Local UTC timestamps read during this audit:

- Protocol modification: 2026-10-18 19:48:35.326184.
- Planned-case modification: 19:48:52.482643.
- Freeze file creation/modification: 19:49:25.698507.
- Recorded run start: 19:49:31.964785.
- Results creation: 19:49:32.242196; last modification: 19:49:34.214798.

All six freeze hashes match current bytes. Source inspection confirms hash verification precedes fixtures and case solving. The plan is explicitly included in the freeze. These facts support the recorded chronology. The freeze JSON itself contains no timestamp/signature, the filesystem timestamps are mutable, and the final run manifest is a rewritten local record; there is no external timestamp or append-only log proving precommitment. The claim that no earlier extension outcome was computed cannot be independently certified from this package. This is an evidentiary limitation, not a detected fabrication.

The audit also verified the outer delivery hashes, ZIP CRC and archived payload hashes. Both original draft PDFs and all files pinned in the prior final-manuscript QA remain byte-identical. Original resource measurements are recorded observations rather than measurements independently recreated by this audit. Resource code was inspected but its enforcement was not stress-tested again. The producer correctly separates same-process dual implementation from separate-agent review and correctly excludes preparation/packaging from its 2.625 CPU-second subtotal.

## Resources and deliverables

Independent full check: **0.90625 process CPU seconds**, **0.904914 wall seconds**, **54,587,392 bytes peak working set (52.06 MiB)**. The single-process audit has a cooperative 120-CPU-second stop between cases, no workers, no hard memory quota and no external packages. Minor file inspection and archive verification commands are additional, unaggregated overhead; total work remained lightweight. No original scientific runner or original limit installer was executed.

`audit-result.json` records all family aggregates, resource readings, local timestamps and SHA-256 hashes of every original extension file. `case-checks.json` records per-case independent counts. The audit source is `../extension_audit.py`. These audit deliverables are separate from all originals.

Key exact reviewed SHA-256 values:

| Original file | SHA-256 |
|---|---|
| PROTOCOL.md | 2964c93f725b19c25c8accaa86f8853806ab8248223a145a8cc0d0c039876730 |
| freeze.json | 687c34d77bb5b9a87643af5749ed0f006cf11b269726190ded210103e1bb8817 |
| run_extension.py | ca536e6407fe739a8250d9c4716f518cca3ef901f1d42e432386e98c68588122 |
| results.jsonl | c202b7e2d20554255bf54f4ffdff6b069593321c3c8dff1ee22f25f6016d4c32 |
| noise-boundary-certificates.jsonl | f3fe7a989b6e89d989005383934ee789c94009d2766ca29324576bef24fd4423 |
| REPORT.md | 43991aa0c1537e840327ddc8201c68cce4c22b608e9f8e56b1bfe2926bf3b15d |
| DRAFT_ADDENDUM.md | 4e16a931c59b5239dc17247af4f57bf966af638ccbf51da859d1bcecbd150a99 |
