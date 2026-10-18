# Frozen specification v1

## Question and finite assertion

Domain: all isomorphism classes of finite connected undirected simple unweighted graphs G with 3 <= |V| <= 10, |E| = |V|, and maximum degree <= 3. Connectivity and |E|=|V| are equivalent to having exactly one cycle in this domain. Orders 0, 1 and 2 have no admissible simple unicyclic graph. Include cycles of every length 3 through 10, with no pendant vertices required.

Distances d(u,v) are integer shortest-path lengths, d(v,v)=0. Sensors may be any vertices, including either member of a pair. For an unordered pair {u,v}, let D(u,v) = {s : d(u,s) != d(v,s)}.

A set S resolves G iff |S intersect D(u,v)| >= 1 for every pair. A set S is fault-tolerant iff that count is >= 2 for every pair. This means remaining sensors resolve after any one identified sensor is erased; it does not model an erroneous or unidentified reading. Since u and v themselves both distinguish their pair, V is always feasible.

beta(G) = min |S| over resolving sets. A minimum base B is any resolving set of size beta(G); inclusion-minimal larger resolving sets are excluded.

beta2(G) = min |S| over fault-tolerant sets.
rho(G,B) = min |S| over fault-tolerant sets with B subseteq S.
p(G,B) = rho(G,B) - beta2(G).

Assertion tested: for every graph in the finite domain and **every** minimum base B, p(G,B) <= 1. No representative base, random base or favorable tie may replace this quantifier. In particular rho is total superset size, not just the number of added sensors. Record rho - |B| separately if useful.

The proposed wider conjecture is neither established true nor established novel. Passing this pilot only verifies the finite assertion, conditional on its implementation and coverage audit. A fully checked pair with p >= 2 refutes any conjecture containing that graph/base pair. Do not expand the range or switch questions on failure. No network, physical, deployment, utility or publication claims.

## Labels and equivalence

Each representative has vertices 0,...,n-1 and sorted edges [u,v] with u<v. Enumerate all minimum-base bit masks for that representative, including automorphism-equivalent masks. Isomorphisms preserve distances, beta, beta2, containment, rho and p, and biject minimum bases. Thus this covers all labeled instances without enumerating every permutation as a different graph.

Keys must be exact canonical structural strings, not floating signatures or hashes used as equality tests. SHA-256 is only a provenance identifier; keep full strings and edge lists. Deterministically select representatives and sort graph keys within each order. Break witness ties by increasing integer mask, with bit i corresponding to vertex i. Never discard tied bases.

## Complete primary construction

Generate all nonisomorphic trees of each order through 10 by leaf extension from one vertex, allowing attachment only at vertices of current degree <=2. Deduplicate with exact tree canonical encodings. Every subcubic tree is generated: deleting a leaf preserves the degree bound, and the deleted leaf can be reattached under this rule. Prove the canonical tree encoding before relying on it: recursively encode sorted child encodings at a center; for two centers encode the sorted pair of rooted half-tree encodings under a distinct tagged form.

For each subcubic tree T of order n>=3, add every non-edge whose endpoints both have degree <=2. Check simple, connected, n edges and degree <=3, then deduplicate exactly. Every target G occurs: delete any edge of its unique cycle to get a subcubic spanning tree T; the deleted edge's endpoints have degree <=2 in T. Conversely every accepted addition creates exactly one cycle.

For a unicyclic canonical key, peel leaves to identify the unique cycle. At each cycle vertex encode its attached off-cycle rooted tree, excluding both cycle edges. Take the lexicographically least sequence among every rotation in both orientations, with unambiguous separators and an explicit cycle-length tag. A root on the cycle has at most one off-cycle child; off-cycle vertices have at most two children. Rooted-tree encodings and the cycle's dihedral equivalence prove this key is complete for graph isomorphism. Pure cycles have identical empty attachment encodings and remain included.

## Stop conditions

Process ascending order and deterministic graph key. Stop new enumeration on a candidate p>=2, independently verify the candidate, preserve certificates and report it. If verification disagrees, stop as an implementation discrepancy. Stop when complete or before a resource cap. Early stopping must explicitly identify the processed prefix and cannot be called exhaustive through 10. No rerun or recovery may reset the total computational allowance.
