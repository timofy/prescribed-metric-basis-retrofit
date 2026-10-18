# Prescribed metric-basis retrofit

**Maths | AI-generated research draft | Not human peer reviewed**

Tim Hughes is the project owner and research coordinator. AI systems generated and revised the arguments, manuscript, code and checks under his direction. This does not assert personal verification of the proof by the owner, or identify AI as a legal author. Originality is not guaranteed. There is no physical validation.

[Public reading page](https://timofy.github.io/prescribed-metric-basis-retrofit/) · [Read paper](paper.html) · [PDF](output/paper.pdf) · [LaTeX](paper.tex) · [Review](output/review.pdf) · [Evidence ZIP](evidence.zip)

## Result and scope

The draft gives a proof of the sharp bound 0 <= rho(G,B)-beta2(G) <= 1 for every minimum metric basis of a finite connected simple unweighted subcubic unicyclic graph. The independently checked original finite enumeration covers 331 graph classes, 3,900 bases and 237,928 subset entries through ten vertices (3,761 premiums zero; 139 one).

The separately audited extension covers 382 labelled cases, 2,984 bases, 68,576 subsets and 4,675 noise certificates. No premium above one was found in that sample. This is not a universal weighted or changed-topology theorem. Three bicyclic cases repeat labelled edge lists. The one-half distance-unit noise boundary is generic for connected unit-edge graphs, not a new empirical discovery. Weighted margins are scale-dependent; no physical or stochastic error calibration is claimed.

## Reproduce and audit

Python 3.13 was used; graph arithmetic and subset searches use the standard library. Windows Job Objects implement the recorded bounded runners. Preserve saved reference outputs; rerun only in a fresh copy with explicitly assigned resources. Original pilot: `python pilot/launch.py` (remove only the copied existing run directory first). Extension: `python extension/run_extension.py` (remove only copied run-manifest/results before a fresh bounded run). Independent audits: `python pilot-audit/audit.py` and `python extension_audit.py`; preserve copied audit outputs before rerunning. The public scripts have documented relative-path adaptations. No scientific experiment was rerun merely to publish this release.

`PROVENANCE.json` records original and public file hashes. `SHA256SUMS.json` pins the public release payload. Public sanitisation removes machine-specific paths and internal delivery records; historical hashes are evidence identifiers, not claims that adapted scripts are byte-identical. The extension's public freeze hashes are recomputed for the adapted sources. Its original local pre-run record was not independently timestamped preregistration.

`pilot/` contains original code and exact results; `pilot-audit/` the original independent computational audit; `extension/` the fixed extension cases/results; `extension-audit/` its separate executable audit report and checks. These are AI computational reviews, not human peer review. Historical audit wording is read with the corrected paper and review report.

## Licences and reuse

Original paper/documentation: [CC BY 4.0](LICENSE-DOCS.md). Original code: [MIT](LICENSE-CODE). Grants apply only to rights the project owner may grant, to the extent copyright exists; they do not claim ownership of AI outputs where no copyright exists. Cited third-party works and dependencies retain their own rights. No third-party full-text papers, tools, fonts or private workspace files are bundled. See [NOTICE](NOTICE.md) and [citation metadata](CITATION.cff).

This repository is one Maths project. `project.json` supplies stable category and project identifiers; other fields of research should use separate repositories. There is no private Hub content here.
