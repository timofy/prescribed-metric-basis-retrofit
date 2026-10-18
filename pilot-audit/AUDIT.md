# Independent bounded sensor pilot audit

**Verdict: PASS for the stated finite domain.** All 331 saved graphs, all 3,900 minimum resolving bases, and every saved optimum and certificate passed an independently written exact verifier. No critical mathematical mismatch or original-code bug was found. The original files were not edited and all their recorded SHA-256 hashes stayed unchanged during the successful run.

Coverage at n=3 through 10 is **1, 2, 4, 9, 17, 38, 80, 180** isomorphism classes. There are **3,761 bases with p=0 and 139 with p=1**. This is a finite computational result, not an unbounded theorem or a verified novelty claim.

## Definition-level verification

`independent_core.py` was written before reading any original implementation or saved-result contents. It imports no pilot module. Breadth-first search computes the fixed original graph's distances. For every one of the 2^n sensor subsets, the oracle constructs distance signatures and tests uniqueness. A nonempty sensor set is FT precisely when every set obtained by deleting one sensor is resolving; those answers are looked up from the exhaustive signature table. The empty set is not FT on these graphs. Minimum cardinalities are then taken over the full tables, including all FT supersets of each minimum resolving base.

The successful run checked **237,928 graph/subset entries**, equality of saved distance matrices, all bases without omissions or duplicates, beta, beta2, rho, p, and feasibility/cardinality of every saved witness. Each certificate's claimed resolving/FT status and every supplied failing vertex pair were independently checked. A failing FT pair is valid exactly when fewer than two sensors distinguish it. We did not require the claimed pair to be lexicographically first; that ordering is irrelevant to certificate validity. We did not require optimum witnesses to be the lexicographically first optimum.

## Coverage proof and generator inspection

The original generator enumerates subcubic trees by adding leaves, then adds each missing edge whose endpoints have degree below three. Inductively, deleting a leaf from any subcubic tree gives a smaller such tree, so leaf extension is complete. Deleting a cycle edge from any connected simple unicyclic graph gives a spanning tree with maximum degree at most three, and both removed-edge endpoints have room for that edge. Thus the original construction is complete if its isomorphism deduplication is exact.

The independently implemented coverage route in `audit.py` instead enumerates cycle lengths k=3..n, compositions of n-k among cycle vertices, and unordered rooted trees having at most two children at every vertex. Each cycle vertex receives at most one attached tree. This exhausts the class because every connected unicyclic graph has a unique cycle; cutting its cycle edges leaves exactly these rooted attachments. Binary child-tree encodings are generated inductively by zero, one, or two children. Balanced-parenthesis encodings uniquely describe unordered rooted trees; the cyclic attachment sequence is canonicalized over rotations and reflection. A unique cycle must map to the unique cycle under an isomorphism, so equality of these keys is necessary and sufficient. The independently constructed set of keys equaled the keys of saved graphs at every order, with no duplicate saved class.

No original generate/solve/verify routine was imported or executed. After implementing the independent coverage route, original verify.py was inspected and found to contain a cycle-attachment cross-check too. Thus this audit supplies independently authored code and a route different from the original primary generator, but does not claim a new third combinatorial characterization. An unused independent tree-extension implementation remains in `independent_core.py`; it was not used for the reported coverage result.

## Seven-vertex witness: exhaustive finite proof

For E={(0,1),(0,2),(0,3),(1,4),(2,5),(4,5),(5,6)} and B={0,5}, all **128 subsets** were checked. `witness-all-128-subsets.csv` exposes each subset's resolving status, FT status, B-containment, and (for every nonempty non-FT subset) an erasure and collision pair. Mask bit i denotes vertex i.

| Cardinality | Resolving subsets | FT subsets | FT supersets of B |
|---|---:|---:|---:|
| 0 | 0 | 0 | 0 |
| 1 | 0 | 0 | 0 |
| 2 | 15 | 0 | 0 |
| 3 | 35 | 12 | 0 |
| 4 | 35 | 35 | 10 |
| 5 | 21 | 21 | 10 |
| 6 | 7 | 7 | 5 |
| 7 | 1 | 1 | 1 |

No singleton resolves; B resolves, so beta=2. There is no FT set of size at most two, and {1,2,3} is FT, so beta2=3. No size-three FT set contains B, and {0,1,2,5} is FT, so rho(B)=4 and p=1. The full lists of resolving masks, FT masks, minimum bases, and their rho values are in `audit-result.json`. This witness attains the largest penalty observed in this bounded domain; no general upper bound is asserted.

## Calibration and optional finite cross-check

Paths P3..P10 returned beta=1, beta2=2. Cycles C3..C10 returned beta=2, beta2=3 except **C4, beta2=4**. The three-leaf star returned beta=2, beta2=3. These are calibration examples, not an enumeration of all trees.

The optional proposed inequality p <= beta-L had **no contradiction in the saved 3,900 bases**. Here an off-cycle terminal fork was counted as an off-cycle degree-three vertex incident with two paths whose internal vertices have degree two and whose other ends are leaves. The count L is recorded per graph in `graph-audit.json`. No new graph search was run for this question. The proposed exchange lemma remains unproved, including the assertion for arbitrary orders.

## Resources, reproducibility, and limitations

- Successful exhaustive audit: **5.125 process CPU seconds**, **5.373 wall seconds**, **83.05 MiB peak working set**, on Python 3.13.1, single process, no workers or external packages.
- The first run completed the mathematical assertions but failed while reporting Windows process memory because ctypes initially interpreted a process handle with the wrong width. This audit-only instrumentation defect was corrected. Its original error is retained as `first-run-resource-reporting-error.txt`; it was not a mathematical mismatch. Its CPU counter was not persisted; file timestamps bound its post-initialization duration to about six seconds (conservatively under eight seconds). Including the successful rerun and small interpreter/inspection/reporting commands, charged audit compute is conservatively **under 30 CPU seconds**, far below the approved 600-second ceiling. This is a conservative charge, not a fabricated exact aggregate measurement. The successful run has a 570-process-CPU-second guard between graphs/coverage steps; it is not a hard OS quota.
- No GPU, paid service, Pi, network-account changes, package installation, larger graph search, or publication was used. Memory was far below 4 GB; no hard memory quota was installed.
- Scope is connected simple unweighted unicyclic maximum-degree-three graphs through order ten, up to isomorphism, with every base on each saved representative. Isomorphism transports the result to any labeling. It excludes larger orders, weighted/directed/multigraph cases, and vertex-removal fault models.
- This is independently authored executable verification with explicit completeness arguments, not a machine-checked proof in a proof assistant. It still trusts Python and the mathematical canonicalization argument. Run `python audit.py` then `python deliver.py` in this workspace to reproduce; the source path is explicit in the script. No remaining blockers.

## Source and result hashes

SHA-256 of key original inputs:

- `generate.py`: `72b31a974050a9eaa8d275758932756706782c3d47d93b023d686412c20f49cb`
- `solve.py`: `e06c139310458cb54a81d6648ac161068d499f697ae578811375191b93b3963f`
- `verify.py`: `2927b07bd449dd21e28a220417c53d55e38515d868353ab86eaa8e2dd6c501cc`
- `runs\pilot-001\graphs.jsonl`: `62e60f9bb99846634ed134a1340e4d054fc33600676bf68f1271f1e82db94f17`
- `runs\pilot-001\bases.jsonl`: `a9fc7c35757ac5e680c06ef315ff1fa6e0660b1168924759bed8acc94703d18e`
- `runs\pilot-001\certificates.jsonl`: `11569ee3a65bd4b46d209278a7a67b3c991bf2c5ef45fe062e53bc96270cfff1`

`source-before.sha256.json` contains hashes of all original non-cache files. `audit-delivery.sha256.json` contains hashes of this audit's code and deliverables, including the report and machine-readable results.
