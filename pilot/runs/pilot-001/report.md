# Finite pilot result

For every connected simple unweighted unicyclic graph of maximum degree at most 3 on 3 through 10 vertices, and every minimum-cardinality resolving base in the chosen representative, the computation found **rho(G,B) - beta2(G) <= 1**. No counterexample was found. This is finite computational evidence, not an unbounded proof or novelty claim.

The exact primary solver and a separately written verifier agreed on all **331 graph isomorphism classes, 3,900 minimum bases and 237,928 graph/subset truth-table entries**. The verifier was implemented in the same task, not by an independent external researcher. External verification is pending.

## Coverage and results

| Vertices | Graph classes | Minimum bases | Bases with p=0 | Bases with p=1 | Graphs admitting p=1 | Coverage + solve + verify CPU seconds |
|---:|---:|---:|---:|---:|---:|---:|
| 3 | 1 | 3 | 3 | 0 | 0 | 0.000000 |
| 4 | 2 | 9 | 9 | 0 | 0 | 0.000000 |
| 5 | 4 | 29 | 29 | 0 | 0 | 0.000000 |
| 6 | 9 | 74 | 74 | 0 | 0 | 0.031250 |
| 7 | 17 | 175 | 170 | 5 | 2 | 0.062500 |
| 8 | 38 | 407 | 394 | 13 | 5 | 0.312500 |
| 9 | 80 | 971 | 943 | 28 | 11 | 1.546875 |
| 10 | 180 | 2,232 | 2,139 | 93 | 27 | 8.156250 |
| Total | 331 | 3,900 | 3,761 | 139 | 45 | 10.109375 |

Best penalty: 0. Worst penalty: 1. There are no negative penalties (a constrained optimum cannot improve the unconstrained optimum). Zero timings reflect the timer's resolution; they do not mean no work occurred. Per-order timing starts after primary generation, so the complete worker timing below is the appropriate total.

Primary generation used leaf extension to enumerate all subcubic trees, then added every eligible non-edge and deduplicated by exact rooted-tree/cycle encodings. A second construction assembled cycles with rooted binary-tree attachments. Its raw construction counts for n=3..10 were 1, 4, 11, 29, 73, 181, 444, 1,085. Independent adjacency-backtracking isomorphism matched the same class sets in both directions and detected no duplicate primary classes. The completeness arguments are in `../../SPECIFICATION.md`; the all-roots tree-key implementation clarification is in `../../GATE_RELEASE.md`.

Every minimum base mask was retained, including symmetry-equivalent bases. Graph isomorphisms preserve the objectives and transport the entire base family, so a representative plus all its bases covers all labelings. Cycles C3 through C10 are included. The C3/C4/C5 calibration checks passed, including beta2(C4)=4. Sensor erasure deletes a coordinate only; neither implementation deletes a graph vertex or changes the distance matrix.

Primary logic uses BFS distances, distinguishing-pair bit masks and complete subset scans. The verifier uses Floyd-Warshall distances, tuple combinations, unique distance signatures and explicit deletion of each sensor coordinate. It recomputes every optimum and base family. A post-run audit parsed the saved files, reverified every certificate/optimum, checked hashes and checked 1,182 relabelings (all permutations for graphs through order 5, reversal and cyclic shift for larger representatives). Canonical-key and mapped-witness containment/cardinality invariance passed. The relabeling checks do not independently recompute every optimum under every permutation; invariance also follows from the specification's isomorphism argument.

## Concrete external verification candidate

Choose the seven-vertex graph with edges:

```
(0,1), (0,2), (0,3), (1,4), (2,5), (4,5), (5,6)
```

It consists of a 5-cycle with two pendant leaves. Selected base B={0,5} has beta=2. An unconstrained optimum is {1,2,3}, giving beta2=3. A smallest fault-tolerant superset of B is {0,1,2,5}, giving rho=4 and p=1. This is a tight example, not a counterexample. All five possible size-three supersets of B fail; the saved certificate supplies an explicit obstructing pair for each. The 128-entry complete subset table also certifies beta=2 and beta2=3. The graph has 15 minimum bases, all included in the candidate file. This is an example at the smallest order admitting positive penalty in this fully completed range; it is not claimed uniquely smallest by any secondary ordering.

See `external-verification-candidate.json` for the edge list, distance matrix, all bases and optima, complete subset certificate and selected witness.

| Added vertex to B | Pair distinguished by fewer than two sensors |
|---:|---|
| 1 | {2,3} |
| 2 | {1,3} |
| 3 | {1,2} |
| 4 | {2,6} |
| 6 | {0,1} |

## Timing and resource accounting

Windows 11, CPython 3.13.1, 64-bit; only the standard library was used. Execution was restricted to one logical CPU. No GPU, paid service or package installation was used.

- Main exact worker: **10.390625 CPU seconds**, **10.904554 wall seconds**, peak resident working set **41,967,616 bytes**.
- Launch including synthetic controls and the main worker: **12.859375 aggregate CPU seconds**, **14.852332 wall seconds**. Launcher peak working set 32,841,728 bytes. Peak job committed memory was 142,348,288 bytes; this is not presented as resident RAM.
- Saved-artifact audit: **8.25 CPU seconds**, **8.508561 wall seconds**, peak resident working set **83,447,808 bytes**.
- Measured aggregate for launch plus audit: **21.109375 CPU seconds**. Charge an additional **2 CPU seconds** conservatively for the failed initial control setup and syntax compilation (their full shell wall durations were 0.639622 and 0.752165 seconds, respectively). Main scientific CPU was not spent during that failed setup. Small metadata reads/report assembly are outside scientific enumeration; ample reserved allowance remains.

The charged scientific/preflight/audit use is **23.109375 CPU seconds**, far below 7,200. The conservative sum of launcher and worker peak resident sets is 74,809,344 bytes; the serial saved-file audit peaked at 83,447,808 bytes. Synthetic control processes had hard resident caps; aggregate hard resident ceilings were below 4,000,000,000 bytes throughout the bounded launch. No claim is made that the exact simultaneous peak resident set of the deliberately memory-exhausting synthetic child was sampled.

Nested Windows Job Objects enforced aggregate committed-memory, CPU affinity, user CPU, active-process and kill-on-close limits, supplemented by wall deadlines and process hard working-set maxima. Parent+child hard working-set maxima were 256 MB + 3 GB, below 4 GB; main worker could not spawn children. Synthetic checks confirmed memory-allocation rejection, child-process rejection, CPU-limit termination and wall-deadline termination. The first control setup failed closed because it demanded exact equality of a page-rounded memory cap. It was corrected to accept positive effective caps no larger than requested, before any enumeration. Recorded cap fields are requested ceilings; precise page-rounded readback values were checked but not persisted. This provenance limitation does not affect the much smaller measured run usage.

The audit ran after the main job with a separately bounded 60-second wall/50-second user CPU/500 MB committed-memory job; its allowance fits the unspent original cap. No failed attempt reset the overall budget. Full result completion stopped research; no optional greedy comparison or larger search was run.

## Files and reproduction

- `graphs.jsonl`: representative edges, distances, beta, beta2 and optimum witness.
- `bases.jsonl`: every minimum base, rho, p and an optimum superset.
- `certificates.jsonl`: complete subset truth tables with first obstructing pairs. Array index is the subset mask; columns are cardinality, first failure for resolving, first failure for fault tolerance. Null means no obstruction.
- `coverage.json`: per-order primary and secondary generation counts and coverage.
- `manifest.json`: exact argv, versions, unchanged code hashes, result hashes and worker resources.
- `saved-artifact-audit.json`: serialization/reverification and relabeling checks.
- `../../launch-record.json`: control-test results and aggregate launch resources.
- `external-verification-candidate.json`: portable worst-penalty example.

Original execution, from the project directory:

```powershell
python launch.py
python audit_saved.py
```

These commands were executed, not merely proposed. The launch deliberately refuses to overwrite its ledger or existing run. For an independently authorized fresh reproduction, copy the project Python sources to a new empty isolated directory, copy the preparation contract/specification/freeze artifacts and gate record there, then use those commands. Do not delete the existing results or treat a fresh directory as authorization to reset this pilot's budget. `audit_saved.py` expects the copied frozen preparation files for its hash check. Python sources captured by the original run manifest must remain byte-identical; `audit_saved.py` is an added post-run tool pinned in the delivery hash manifest.

Scientific results are deterministic; timings, hardware/platform strings and wall-clock timestamps are not. No numerical tolerances or random seeds enter the calculation.

## Interpretation and residual checks

The proposed inequality survives the entire specified finite domain and is tight within that domain. Its behavior beyond 10 vertices and its novelty remain unresolved. Independent external review should first reproduce the supplied seven-vertex candidate, then inspect coverage and the full certificate set. The same-task second implementation substantially reduces shared-algorithm risk but does not replace external verification.

Prior-art context and URLs are preserved in `../../GATE_RELEASE.md`. No source theorem was used to remove graph classes, skip bases or claim novelty. No publication, external communication, recurring task, account change, Pi work or edits outside this isolated project occurred.
