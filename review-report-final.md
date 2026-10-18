# Review and limitations report

Tim Hughes, project owner/research coordinator | Public AI-generated draft

## Result and interpretation

The manuscript proves the sharp fixed-basis premium bound 0 <= rho(G,B)-beta2(G) <= 1 for every minimum metric basis B of every finite connected simple unweighted subcubic unicyclic graph. A seven-vertex example attains equality. This is a modest structural contribution to pure graph theory. Basis-preserving fault-tolerant augmentation itself is established prior work, and no practical deployment improvement or efficient optimization algorithm is claimed.

The independently audited finite pilot covers 331 graph classes, all 3,900 minimum bases and 237,928 subset entries through ten vertices. Penalties were zero for 3,761 bases and one for 139. That audit is distinct from the general proof and is not used to extrapolate to arbitrary orders. Original evidence and earlier pilot deliverables remain unchanged.

## Mathematical review and revisions

Separate AI sessions reviewed the arguments. The final supplied mathematical referee verdict was "proved as written" for source revision 9f7eb2405505942945724cabdd7131110e4b964c63e8c354130a98ab11044b3c. Its two minor exposition findings are addressed: the failed sensor remains a target vertex and distances remain unchanged; the source's branch parameter is explicitly identified with the terminal-fork count, with branch resolution exactly requiring each U_w to be met. Fault tolerance is defined by two distinguishers per pair, avoiding empty-set vacuity in an erasure-only definition.

The reviewer read the structural source and checked the terminal-thread exchange, one-root repair, odd-cycle distance argument, even-cycle antipodal completion and seven-vertex witness. It did not audit the broad finite experiment; a separate computational reviewer did so. The corrected proof artifact identifier supplied by the coordinating session is 4803bb80a59e854b4097e3729d8ad61c4694aa620b4ff8c9ff48e8519b707ee5. These are supplied source identifiers, not hashes recomputed for locally unavailable originals.

The integrated manuscript uses an elementary basis-size lemma instead of the reviewed revision's Theorem 11 dimension formula. Its explicit midpoint construction shows that any two distinct cycle roots extend to a geodesic triple, including antipodes and triangles. This variant was supplied in the clean proof and locally expanded; the retained referee report is not represented as a byte-identical review of the final typeset manuscript. The source proof and final PDF have their own delivery hashes.

All these checks are AI logical/computational review, not external human peer review, journal acceptance or proof-assistant verification. The manuscript contains a corresponding assistance disclosure. No particular model/tool history, affiliation or ORCID has been invented.

## Precise prior-art comparison

The bounded result-specific search judged the exact sharp prescribed-basis comparison apparently new, with moderate confidence and no guarantee of originality. The defensible manuscript wording is: "We did not find this prescribed-basis comparison in the sources checked."

- Hernando et al. (2008), Lemma 3.1, already augment a given resolving set to a fault-tolerant superset. Remark 2.4 is a direct tree predecessor for local terminal-thread freedom. Augmentation is not claimed as new.
- Sedlar and Skrekovski's arXiv:2104.00577v1, Lemmas 1, 3, 6, 7 and Definition 5, provide the essential ordinary-resolution characterization. The exchange lemma is an attributed application/corollary, not a new characterization. Theorem 11 is not needed in the integrated proof.
- Knor, Sedlar and Skrekovski (2025) and Geneson-Tsai (checked 2025 preprint) compare fault-tolerant with ordinary dimension. The latter also explicitly extends arbitrary sets. No inspected statement directly gives the constrained optimum's additive premium. No exact bound is quoted from the internally inconsistent abstract/Theorem 2.7 constants in the inspected Geneson-Tsai version.
- Hakanen et al. study vertices belonging to all or no ordinary bases, a different quantifier. Their discussion acknowledges known odd/even branch-free unicyclic dimension facts, so those facts are not claimed as discoveries here.
- Estrada-Moreno's k=2 formulas concern unconstrained fault-tolerant dimensions of specified unicyclic subclasses. The seven-vertex witness has two degree-three cycle roots, unlike the single-pendant-path cases.
- Prabhu et al., version 2, use designated attachments that remain available while additional chosen sensors may fail. Here every prescribed sensor is also subject to erasure.
- Bergougnoux et al. use required/forbidden extensions for inclusion-minimal solutions; ordinary inclusion-minimal extension differs from this minimum-cardinality fault-tolerant objective.

The universal union observation carries no priority claim. The exchange is a technical lemma with attribution. The sharp example certifies the bound, not discovery of its standard graph family.

## Search and model limits

The public English-language search took approximately ten minutes as of 18 October 2026. It covered fault-tolerant and k-metric dimension, subcubic/unicyclic graphs and fixed, prescribed, imposed, mandatory and forced landmarks, extensions, supersets, exchange and disjoint resolving sets. Relevant definitions/proofs and adjacent references were read. A terminology-focused second pass was by the same searcher, not an independent second review.

This was not an exhaustive MathSciNet/zbMATH search. Theses, non-English or unindexed work and unavailable full texts were incompletely covered. The identified 2025 pseudotree survey was not successfully retrieved and was not used to certify absence of prior art. No authors were contacted. The conclusion may change if an equivalent formulation or overlooked source is found.

The theorem concerns exact unweighted graph distances and an identified single-coordinate erasure. It does not cover physical vertex removal, recomputed distances, a reduced target population, noisy observations, multiple failures, hydraulic flow, pressure, leaks or field performance. The proof begins with an optimal fault-tolerant set and is not by itself a polynomial-time optimization algorithm.

## Independently audited computational extension

The revised manuscript adds Section 9 while retaining the original theorem and proof. All 382 extension cases, 2,984 minimum bases, 68,576 subset entries and 4,675 noise certificates passed a separately authored executable audit. No premium above one was found. The cases comprise 71 baselines, 213 weighted variants, 28 degree-four variants and 70 two-cycle variants; three two-cycle cases are exact labelled repeats. These are finite, label-dependent samples, not an exhaustive or universal extension.

The audit's editorial corrections are integrated. The half-unit noise threshold is generic for connected unit-edge graphs: integer distances give m2>=1 for any exact FT layout, and an adjacent target pair gives m2<=1 by the triangle inequality. Thus m2=1 and the strict guarantee is epsilon<1/2. This is a consistency check, not a new empirical finding. The epsilon=1/4 success of integer-distance FT layouts and zero erasure margin of ordinary minimum bases are also expected consequences. The weighted rows have variable absolute margins: 37 of 1,337 selected augmentations passed at epsilon=1/2 and 13 at epsilon=1. Those counts may share layouts; no margin optimisation, scale normalisation or physical calibration was performed.

The local protocol, case plan and source hashes were recorded before the recorded run, and checked before solving. This is a local freeze, not independently timestamped preregistration; it cannot certify absence of earlier unrecorded analyses. The original frozen files retain their historical wording for evidence integrity, while this revision supplies the corrected interpretation.

A separately authored executable audit reproduced the complete finite case plan, all optima and noise certificates; this is AI computational review, not human peer review or physical validation. The bundle includes extension-audit/AUDIT.md, audit-result.json, case-checks.json and the public-path-adapted extension_audit.py. Their reviewed source hashes are retained, including results.jsonl c202b7e2d20554255bf54f4ffdff6b069593321c3c8dff1ee22f25f6016d4c32. This review status supersedes pending-audit language in the historical addendum. The coordinator authorised this public release; no journal acceptance is implied.

The extension core/postcheck used 2.625 recorded CPU seconds; the separate audit used 0.90625 CPU seconds. Preparation and packaging overhead are additional and unaggregated. The producer enforced hard Windows limits; the separate auditor measured memory and used a cooperative CPU guard without a hard memory quota. No new scientific run was performed during this revision.

## Resources, delivery and next decision

The original scientific/preflight charge was 23.109375 CPU seconds. The external computation audit charged under 30 additional CPU seconds, making the recorded combined amount under 53.109375 seconds against the two-hour pilot cap. The primary runner enforced Windows limits; the separate auditor measured memory and used a cooperative CPU guard without a hard memory quota. This distinction is preserved. Manuscript preparation and rendering did not enumerate further graphs.

Deliverables comprise the dated manuscript PDF, this report PDF, editable Markdown/BibTeX sources, recorded referee and novelty context, and a ZIP containing source and exact computational/audit evidence with SHA-256 manifests. The final PDFs are rendered and visually inspected, with displayed formulas and citation links checked before delivery.

This public AI-generated draft is not human peer reviewed. Tim Hughes is the project owner/research coordinator, with no assertion that he personally verified the proof. No journal acceptance or physical validation is claimed.
