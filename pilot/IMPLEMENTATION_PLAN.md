# Exact implementation and verification plan

All components are planned, not executed. Use existing CPython standard library only; no GPU, service, optimizer or third-party dependency is needed. Keep modules separate: `generate.py`, `solve.py`, `verify.py`, `bounded_run.py`, `report.py`. Freeze their hashes before an authorized run. `verify.py` must not import distances, subset predicates, optimum search or canonicalization from the solver.

## Exact core

1. Read a sorted edge list; assert domain invariants. Compute the distance matrix with breadth-first search from each vertex using integer queues.
2. Build each pair's distinguishing sensor bit mask D. Enumerate all 2^n subset masks once. For each compute size and whether every D has intersection popcount >=1 and >=2. No floating arithmetic, approximate solver or pruning assumption.
3. Find beta and beta2 from the full truth tables. Retain every resolving mask of cardinality beta, in integer order.
4. For each minimum base B, scan all fault-tolerant masks S satisfying (S & B)==B, minimize |S| and choose the least mask at that optimum as witness. This direct method is bounded by 4^n mask comparisons per graph. An exact superset minimum transform may replace the scan only after direct cross-checks; it is unnecessary at this scale.
5. Emit all base results including rho, beta2, p and the chosen S. Store graph-level beta, beta2, a chosen unconstrained optimum witness and counts. Flush completed graph records; a partial graph cannot contribute to verified coverage.

## Reproducible certificates

Per graph save sorted edges, n, full canonical key, distance matrix, all minimum-base masks, beta, beta2, and a complete table for all masks 0..2^n-1. A table entry contains cardinality, resolves, fault_tolerant, and the lexicographically first pair failing the count >=1 or >=2 where applicable. Null means no failure. This is a compact exhaustive certificate: all smaller subsets have a checkable obstruction, and every asserted minimum has a witness. Do not rely only on a solver's claimed lower bound.

Per base save B, rho, p, chosen fault-tolerant superset and, for each S containing B with |S|<rho, the first pair with fewer than two distinguishing sensors (can be referenced by mask into the graph certificate). This certifies optimality, containment and the full base quantifier. All tied optima need not be output as separate witnesses because the complete truth table reconstructs them.

Use UTF-8 JSONL with a schema version, integer masks and arrays. `graphs.jsonl`, `bases.jsonl`, `certificates.jsonl`, `coverage.json`, `manifest.json`, `report.md`. Each base record references the graph key and representative edges through its graph record. No fabricated example result records in the output area.

## Independent numerical and combinatorial verification

Reconstruct each graph from its edge list. Compute distances via integer Floyd-Warshall with a finite infinity sentinel n+1, rather than BFS. Enumerate subsets as tuples using combinations rather than solver masks. Check resolving by comparing full distance signatures of all vertices for uniqueness. Check fault tolerance by deleting each selected sensor in turn and testing resolving again, independently of the two-distinguishers predicate. Explicitly reject an empty fault-tolerant set to avoid vacuous deletion semantics. For n>=3 this agrees with the frozen definition.

Recompute beta, the entire list of minimum bases, beta2, and rho for every base using cardinality-ordered combinations and direct containment. Compare full lists and all optima, not just maximum p. Independently check every recorded obstruction pair and witness. Raw certificate bytes are round-tripped through the parser. Any discrepancy stops the run and blocks a conclusion.

## Independent coverage check

Use a second construction: choose a cycle length k=3..n; distribute n-k additional vertices among the k cycle positions; at each position attach either nothing or one rooted tree. Generate rooted trees recursively as unordered child multisets of size at most two, bounded by total size, then connect their roots to the cycle. This covers precisely all subcubic unicyclic graphs because removal of cycle edges leaves these attachments. It does not depend on the spanning-tree-plus-edge construction.

Compare class sets at each n by exact degree-preserving adjacency backtracking isomorphism, with safe degree/cycle-length filters only. The verifier must not use the primary canonical key as its equality oracle. Verify both directions: every primary graph matches a secondary class and vice versa; confirm primary classes contain no isomorphic duplicates. Emit generated counts, duplicate counts, accepted counts and matched counts per n. Counters are measured, not asserted from memory or undocumented sequences.

After the gate, planned small tests include C3 (beta=2, beta2=3, rho=3 for all bases), C4 (beta=2, beta2=4, rho=4 for every base), C5 (beta=2, beta2=3, rho=3), symmetric tied bases, pendant attachments, disconnected/multicyclic/degree-4 rejections, and label changes. Use reversal, cyclic shift and all permutations of small fixtures to check invariance with explicit mapped base masks. Larger representative relabeling checks use deterministic permutations. These are planned expectations, not reported experiment results.

## Optional greedy comparison

Disabled by default. Only after the exact core and its independent verification are complete, and within the remaining original budget, augment each B by a missing vertex maximizing reduction of sum over pairs of max(0,2-count). Tie-break by smallest vertex label. Stop when fault-tolerant. Record its size minus rho, retain label dependence, and do not interpret greedy output as an optimum or proof. Skip entirely after a counterexample or resource stop.
