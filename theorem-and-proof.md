# Sharp prescribed-basis premium bound



AI-generated research draft | Tim Hughes, project owner/research coordinator | Not human peer reviewed.



The bounded prior-art assessment found no statement of the exact comparison in checked sources; originality is not guaranteed. Separate AI logical review is not human peer review.



# 2. Definitions and conventions



All graphs in the experiment are finite, connected, simple, undirected and unweighted. Let d_G(u,v) be the number of edges in a shortest u-v path. For distinct u,v define



\[

D_G(u,v)=\{s\in V(G):d_G(u,s)\ne d_G(v,s)\}.

\]



A set S resolves G when S intersects every D_G(u,v). Its minimum possible size is beta(G). We call a resolving set B a metric basis only when |B|=beta(G); mere inclusion-minimality is insufficient.



A set S is fault-tolerant when |S intersect D_G(u,v)|>=2 for every distinct pair u,v. Equivalently, S without s resolves G for each s in S, with the empty set excluded on the graphs considered here. To see equivalence, two distinguishers leave at least one after any erasure. If a pair has at most one distinguisher, either it is already unresolved or erasure of that sole distinguisher makes it unresolved. Distances are always taken in the unchanged graph G. Erasing a sensor does not delete its vertex, incident edges or paths through it. The failed sensor vertex remains in the target population and distances are not recomputed.



Write FT(G) for the family of fault-tolerant sets and define



\[

\beta_2(G)=\min_{S\in\operatorname{FT}(G)}|S|,\qquad

\rho(G,B)=\min_{S\in\operatorname{FT}(G),\,B\subseteq S}|S|,

\qquad p(G,B)=\rho(G,B)-\beta_2(G).

\]



The subscript in beta2 denotes the two-distinguishers condition; it is not an assertion that every cited source uses identical notation. All optima exist: for every pair u,v, both u and v distinguish that pair, so V(G) is fault-tolerant. Containment restricts feasible sets, hence p(G,B)>=0. The quantity rho counts all sensors in the superset; rho-|B| counts additions. These are different statistics.



A connected graph is unicyclic when it has exactly one cycle; for a simple connected graph this is equivalent to |E|=|V|. Subcubic means maximum degree at most three. The finite domain is 3<=|V|<=10; no simple unicyclic graph has fewer than three vertices. Pure cycles are included.



# 6. A seven-vertex example with a direct proof



Let V={0,1,2,3,4,5,6} and



\[

E=\{01,02,03,14,25,45,56\}.

\]



Here ij denotes the undirected edge {i,j}. The cycle is 0-1-4-5-2-0; leaves 3 and 6 attach to 0 and 5. Let B={0,5}.



**Proposition 3.** This graph and base satisfy beta(G)=2, beta2(G)=3 and rho(G,B)=4, hence p(G,B)=1.



*Proof.* The following table gives signatures in the indicated sensor order.



| Vertex | B=(0,5) | C=(1,2) | T=(1,2,3) |

|---:|---|---|---|

| 0 | (0,2) | (1,1) | (1,1,1) |

| 1 | (1,2) | (0,2) | (0,2,2) |

| 2 | (1,1) | (2,0) | (2,0,2) |

| 3 | (1,3) | (2,2) | (2,2,0) |

| 4 | (2,1) | (1,2) | (1,2,3) |

| 5 | (2,0) | (2,1) | (2,1,3) |

| 6 | (3,1) | (3,2) | (3,2,4) |



Every B-signature is distinct, so B resolves. No singleton resolves: for singleton sensors 0,1,2,3,4,5,6 respectively, the equal-distance pairs {1,2}, {0,4}, {0,5}, {1,2}, {0,2}, {0,1}, {0,1} are obstructions. Hence beta(G)=2 and B is a metric basis.



Every two distinct T-signatures differ in at least two coordinates, as direct inspection of the seven displayed triples verifies. Thus T is fault-tolerant and beta2<=3. If a set of cardinality at most two were fault-tolerant, erasing a sensor would leave at most a singleton resolving set, impossible here. Hence beta2=3.



There are five possible size-three supersets of B. The following table gives a pair with only one distinguishing sensor in each, together with that sensor. Its erasure causes the displayed collision.



| Added vertex a | Pair | Sole distinguishing sensor in B union {a} |

|---:|---|---:|

| 1 | {2,3} | 5 |

| 2 | {1,3} | 5 |

| 3 | {1,2} | 5 |

| 4 | {2,6} | 0 |

| 6 | {0,1} | 0 |



None is fault-tolerant, so rho(G,B)>=4. The C-signatures are also distinct, and B and C are disjoint. Their union is fault-tolerant: after erasure of a vertex from one of the two sets, the other resolving set remains intact. Thus B union C={0,1,2,5} is a feasible size-four superset and rho(G,B)=4. QED.



For completeness, the saved exhaustive certificate for this graph contains all 128 subsets and all 15 metric bases. It is additional evidence, not needed for the displayed direct argument. Order seven is the first order admitting positive penalty in the completed finite enumeration; this does not assert uniqueness of the example.



# 7. General bound



**Proof dependencies and review.** The complete argument uses the cited ordinary-resolution characterization. Separate AI sessions logically reviewed the proof, including a referee verdict of "proved as written" for the recorded proof revision. This is not human or journal peer review. The integrated elementary size-bound version and the reviewed formula-based revision are distinguished in the accompanying review report. The finite result in Section 3 stands independently and is not used to infer the arbitrary-order bound.



**Theorem 4.** Let G be a connected simple unweighted subcubic unicyclic graph, and let B be any metric basis of G. Then



\[

0\le \rho(G,B)-\beta_2(G)\le 1.

\]



The upper bound is sharp, as shown by Proposition 3. The proof follows from the lemmas and cases below, using the explicitly identified ordinary-resolution results of Sedlar and Skrekovski.



For the propositions, extend rho(G,B) and p(G,B) by the same formulas to any nonempty resolving set B, whether or not it is minimum. When discussing metric dimension we explicitly return to a metric basis.



## 7.1. A general union bound



**Lemma 5 (union bound).** If B is a nonempty resolving set of a connected graph with at least two vertices, then p(G,B)<=|B|-1. In particular, every metric basis of size two satisfies p<=1.



*Proof.* Let F be a minimum fault-tolerant set. If F intersects B, the fault-tolerant superset F union B has cardinality at most |F|+|B|-1. If the sets are disjoint, choose any f in F. Both F without f and B resolve, and are disjoint. Their union is fault-tolerant: erasing any one sensor leaves at least one of the two resolving sets intact. It contains B and has |F|+|B|-1 elements. Subtracting beta2=|F| gives the bound. QED.



## 7.2. Branch definitions and the imported characterization



Let C be the unique cycle. Removing the cycle edges partitions G into rooted trees T_v, one at each v in C. In a subcubic graph a *terminal fork* w is an off-cycle degree-three vertex with two child paths ending at leaves and with only degree-two internal vertices. These two paths are its terminal leafward threads. Let U_w be the union of their vertices, excluding w. Distinct U_w are disjoint. Let L be the number of terminal forks. A *branch-active root* is a cycle root v whose T_v contains an off-cycle degree-three vertex; let b count these roots. This graph-dependent notion is distinct from a root being *active for S*, meaning that S intersects T_v. A *direct cycle thread* is a leafward path attached at a cycle root with only degree-two internal vertices; its occupancy records whether S meets the path away from the root.



The dictionary to the cited source is especially simple here. A cycle vertex has at most one pendant thread. An off-cycle degree-three vertex has a direction leading toward the cycle and contributes a nonvacuous thread-coverage requirement exactly when its other two directions are terminal threads. Each such fork contributes one to the source parameter L(G), so L(G)=L. Being branch-resolving is therefore precisely the condition S intersect U_w is nonempty for every terminal fork w. This identifies both the source's branch parameter and its branch-resolving hypothesis before their use below.



We use Sedlar and Skrekovski [@sedlar-skrekovski], with numbering fixed to arXiv:2104.00577v1. Lemma 1 states that resolving sets are biactive and branch-resolving. Definition 5 and Lemmas 6-7 characterize resolution among such sets by excluding configurations A, B and C. These configurations depend on the active cycle roots, unoccupied pendant threads attached directly to the cycle, and the fixed thread lengths of the graph. The characterization applies to arbitrary biactive branch-resolving sets, not only minimum ones.



Consequently, if R is resolving and R' is branch-resolving with the same active cycle roots and the same occupancy of direct cycle threads as R, then R' resolves. The underlying graph and its thread lengths are unchanged in this use. In the subcubic setting, branch coverage requires precisely that every U_w be met: off-cycle vertices have at most two pendant threads, and cycle vertices at most one. We also use Lemma 3 of the same source: a branch-resolving set resolves if its active roots contain a geodesic triple. For cycle length g, three distinct roots u,v,w form such a triple when d_C(u,v)+d_C(v,w)+d_C(w,u)=g.



These are the source inputs identified and checked against the full preprint in the supplied proof review. The following proof uses elementary basis-size bounds rather than the stronger metric-dimension formula in Theorem 11. It therefore does not require that formula as an additional external premise.



## 7.3. Terminal-thread exchange



**Lemma 6 (terminal-thread exchange).** For a nonempty resolving set B in a subcubic unicyclic graph,



\[

p(G,B)\le |B|-L.

\]



*Proof.* At a terminal fork w, let u_1,u_2 be the first vertices on its two leafward threads. A vertex outside U_w has equal distance to u_1 and u_2, whereas every vertex in U_w has different distances to them. Therefore D_G(u_1,u_2)=U_w. Every resolving set meets U_w, and every fault-tolerant set has at least two vertices in U_w.



Choose B_0 by selecting one vertex of B in each U_w, so |B_0|=L. Starting with a minimum fault-tolerant F, for each selected B_0 vertex not already present replace one F vertex in the same U_w by that vertex. Disjointness of the U_w ensures these replacements have no interference or duplication. Write F' for the resulting set and let phi:F->F' be the bijection matching each replaced vertex to its replacement and fixing the others. Then |F'|=|F| and B_0 is contained in F'.



Fix z in F', and put x=phi^{-1}(z). The set F without x resolves. The set F' without z still meets every U_w, since F had at least two vertices in each such set and replacements preserve the count in each U_w, including after matched deletion. Replacements occur within the same attached rooted tree, so active cycle roots are unchanged relative to F without x. They occur on threads of off-cycle forks, not on direct cycle threads, so direct cycle thread occupancy is unchanged too. The imported characterization implies that F' without z resolves. This holds for every z, hence F' is fault-tolerant.



Adding B without B_0 to F' gives a fault-tolerant superset of B of cardinality at most |F|+|B|-L. Subtract beta2=|F|. QED.



**Consequence for metric bases.** If beta=L, then p=0 by this bound and nonnegativity. The elementary size bounds below will give the remaining case division.



### Elementary basis-size bounds



**Lemma 7.** If b>=2, then beta<=L+1; if b=1, then beta<=L+2; and if b=0, then beta<=3.



*Proof.* First, any two distinct vertices a,b on a cycle of length g>=3 can be completed to a geodesic triple. Choose a shortest a-b arc of length d<=floor(g/2); the complementary arc has length ell=g-d, with 2<=ell<=g-1. Choose an interior vertex c splitting that complementary arc into lengths floor(ell/2) and ceil(ell/2). Both lengths are at most floor(g/2), so each is a shortest cycle distance between its endpoints. Therefore



\[

d_C(a,b)+d_C(b,c)+d_C(c,a)=d+\ell=g.

\]



The chosen c is distinct from a and b. This covers antipodal a,b on an even cycle, as well as g=3: no endpoint or short-cycle exception is needed.



Choose one sensor in every U_w. This branch-resolving core has size L and activates exactly the b branch-containing roots. Indeed every such rooted tree contains a terminal fork, by taking a branching vertex farthest from the root. If b>=2, complete two already active roots to a geodesic triple using at most one additional cycle sensor. If b=1, choose a second root and then a third completing the triple, adding at most two sensors. If b=0, branch resolution is vacuous and any geodesic triple of cycle vertices suffices. Apply the cited geodesic-triple lemma in each case. QED.



For a metric basis, b>=2 now gives p<=1 by Lemma 6. The same applies when b=1 and beta<=L+1. Lemma 7 leaves only beta=L+2 in the one-branch-root case.



## 7.4. The one-branch-active-root case



**Lemma 8 (one branch-active root).** If b=1, beta(G)=L+2, and B is a metric basis, then p(G,B)<=1.



*Proof.* In a finite rooted subcubic tree containing a branching vertex, a deepest branching vertex has two terminal leafward threads; therefore b=1 implies L>=1. All terminal forks lie in the unique branch-containing rooted tree T_r. Apply Lemma 6's exchange construction to obtain a minimum fault-tolerant set F containing B_0, with one chosen B vertex in each U_w. Let C=B without B_0; then |C|=2.



If F meets C, F union B has at most |F|+1 vertices and is a sufficient superset. Otherwise F and C are disjoint. Since F resolves, the imported characterization ensures at least two active cycle roots. Choose z in F outside T_r. Every B_0 vertex lies inside T_r, and no vertex of C belongs to F, so z is not in B. Define S=B union (F without z). Then |S|=|F|+1 and S contains B.



We check every possible sensor erasure from S. If a vertex of C is erased, F without z remains, and resolves by fault tolerance of F. If a vertex of F without B is erased, the resolving set B remains. It remains to erase a vertex q of B_0. The set F without {z,q} is branch-resolving: each U_w originally contained at least two vertices of F, z lies outside T_r, and deleting q removes at most one vertex from one U_w. Relative to the resolving set F without z, the root r stays active because another F vertex remains in q's U_w. Other active roots are unchanged, as is occupancy of direct cycle threads. The characterization implies that F without {z,q} resolves, so the larger set S without q resolves. These cases exhaust S, proving fault tolerance. Thus rho<=|F|+1 and p<=1. QED.



## 7.5. No branch-active roots: odd cycles



Suppose b=0. Then each rooted attachment is a single path, possibly consisting only of its cycle root, and L=0. Write a vertex on the path attached at r as (r,t), where t>=0 is its distance from the cycle. Its distance to a cycle vertex q is t+d_C(r,q).



For an odd cycle of length 2h+1, h>=1, choose cycle vertices a,b at distance h. Consider the root difference d_C(r,a)-d_C(r,b). Along the h-edge arc from a to b its values are



\[

-h,-h+2,\ldots,h.

\]



At the h interior roots of the other arc, traversed from b to a, its values are



\[

h-1,h-3,\ldots,-h+1.

\]



Each list has distinct entries, and their parities differ, so all 2h+1 roots have different differences. The two distances from (r,t) to a and b identify r through their difference and then identify t from either distance. Therefore {a,b} resolves every such graph. The case h=1 includes a triangle and gives differences -1,1,0, so no short-cycle exception is suppressed.



No singleton can resolve a graph containing a cycle: if its sensor is in an attached path at r (including r itself), the two cycle neighbors of r have equal distance to that sensor. Hence beta=2. Lemma 5 gives p<=1 for every metric basis in this odd-cycle case.



## 7.6. No branch-active roots: even cycles



Let the cycle have even length 2h with h>=2. Lemma 7 gives beta<=3. A singleton cannot resolve, by the equal-distance cycle-neighbor argument. Lemma 5 already handles beta=2, so assume beta=3.



Every resolving set has at least two active cycle roots: if only r were active, its two cycle neighbors would have equal distance to every sensor. Furthermore a resolving set cannot have all its active roots in a single antipodal pair {a,a*}. The two cycle neighbors of a have distance one to a and distance h-1 to a*, and thus equal distances to every sensor in paths rooted at a or a*. They would remain unresolved. Consequently a metric basis B has two non-antipodal active roots a,b. Choose sensors x,y in B lying in their respective rooted paths.



Let a*,b* be the cycle antipodes of a,b. The four roots a,b,a*,b* are distinct because a and b are distinct and non-antipodal. The four sensors



\[

F=\{x,y,a^*,b^*\}

\]



also are distinct. After erasing any one of them, the three remaining sensors occupy three distinct roots and contain an antipodal pair of roots. Those three roots form a geodesic triple: for antipodes u,u* and any other cycle vertex v, one of the two semicircles contains v, so d_C(u,v)+d_C(v,u*)=h; adding d_C(u,u*)=h gives the cycle length 2h. This reasoning includes a four-cycle, where any triple of distinct roots contains an antipodal pair.



With b=0, the branch-resolving condition is vacuous. The cited geodesic-triple lemma therefore makes every one-sensor deletion from F resolving, so F is fault-tolerant and beta2<=4. For any graph here, a fault-tolerant set of size k leaves a resolving set of size k-1 after an erasure; hence beta2>=beta+1. Since beta=3, beta2=4. Finally, F contains x and y from B. Adding the remaining third vertex of B produces a fault-tolerant superset of size at most five. Thus rho(G,B)<=5 and p(G,B)<=1.



## 7.7. Completion and sharpness



For b>=2 the exchange bound and Lemma 7 give p<=1. For b=1 the same bound handles beta<=L+1 and Lemma 8 handles beta=L+2, exhausting Lemma 7's possibilities. For b=0, the odd-cycle argument gives beta=2; on an even cycle beta<=3, and the preceding construction handles the only remaining value beta=3. These cases exhaust connected subcubic unicyclic graphs. Nonnegativity was established in Section 2, completing Theorem 4. Proposition 3 supplies equality p=1, so the bound is sharp.



The completed proof has been separately logically reviewed. The bounded novelty assessment and its limitations are stated in Section 1. Neither the computation nor separate-agent review is described as human peer review.





## Source



J. Sedlar and R. Skrekovski, Vertex and edge metric dimensions of unicyclic graphs, Discrete Applied Mathematics 314 (2022), 81-92, DOI 10.1016/j.dam.2022.02.022. Numbering follows arXiv:2104.00577v1. See references.bib for all sources.

