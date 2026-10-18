# Resource bounds and gated run plan

## Envelope

One total pilot budget across implementation tests, graph generation, exact solving, independent verification and optional comparisons: **7,200 CPU seconds and 4,000,000,000 bytes RAM**. Use decimal 4 GB, stricter than 4 GiB. No parallel research workers, GPU or paid service. Metadata/file preparation is not research enumeration; no research CPU has yet been consumed. Record rather than estimate actual research resource use once started.

The bounded enumeration has at most 1,024 sensor subsets and 45 vertex pairs per graph. Direct rho scanning has at most 1,048,576 comparisons per graph. Graph generation is streamed by order with exact deduplication. Do not store all graph certificates in memory; stream completed records. Do not promise a run time or a graph count before measurement.

## Windows enforcement design

The installed audit skill runner's POSIX CPU/address-space limits cannot enforce the requested Windows envelope. Do not silently fall back to monitoring alone. Implement a Windows Job Object supervisor with standard-library ctypes, validate it on synthetic workloads before research, and fail closed if any API or assignment fails. Launch the worker suspended, assign it to the job, set limits, then resume; prevent breakaway. The worker and any children belong to the same job. Kill-on-job-close protects against supervisor loss.

Set an aggregate job user CPU hard limit conservatively below the overall allowance and a job committed-memory hard limit below 4 GB. CPU hard limits based only on user time are insufficient alone: additionally restrict to one logical processor and use a strict wall deadline for the entire job so combined user+kernel CPU is bounded. Use 6,600 seconds wall time, a 6,500-second user-time job limit, 3,000,000,000-byte job memory cap and a one-process job active-process limit. The single Python worker runs both implementations sequentially without subprocesses. Place job affinity at one CPU. The monitor logs aggregate user+kernel time and peak job memory; also poll worker working set and supervisor CPU/working set. Do not equate committed memory to measured resident RAM.

Keep the supervisor small, with 256 MB process memory cap, a 60 CPU-second process limit and a measured wall deadline. A guard checks total sampled working set, stopping at 3.5 GB with reserve; hard job/private-memory limits plus one process provide a conservative allocation backstop, while observed peak resident usage remains a separately reported measurement. If the environment cannot establish a defensible hard RAM ceiling covering supervisor and worker, execution stays blocked until a suitable enforced environment is available. Do not describe sampling alone as a hard RAM guarantee.

Deduct all preflight/synthetic-test CPU and memory use from the same ledger; reserve at most 300 CPU seconds for those tests and later reporting, and require a shorter main deadline when needed. The sum of single-core wall bounds and supervisor/test CPU reservations must remain below 7,200 seconds. Abort before launch if this arithmetic or enforcement cannot be verified. A supervisor must not grant a fresh budget after a restart. An interrupted run with unknown consumption exhausts the remaining budget unless reliable OS accounting recovers it. Budget accounting includes failed attempts.

Before research, independently exercise CPU timeout, memory exhaustion, worker crash, supervisor exit and forbidden child creation with synthetic programs. Record requested/effective caps and observed termination/accounting. These tests do not enumerate graphs, but they occur only after the gate for simplicity. A Windows Job Object configuration is a design requirement here, not an implemented or tested capability.

## Budget allocation and stopping

Primary generation/solving initially receives no more than 3,600 CPU seconds; reserve at least 2,400 seconds for independent verification and coverage, with remaining allowance for controls, evidence and optional work. Check remaining allowance at graph boundaries and checkpoint before it is exhausted. If a candidate counterexample appears, stop generation and prioritize verification of that pair; no need to finish the population. Full completion requires coverage and both solvers to finish for all graphs and bases through 10. If resources prevent that, report exactly the verified subset and distinguish unverified generated results.

## Gate and provenance

1. Receive an explicit literature gate decision from the coordinating session/user, including any revised terminology or scope. Absence of a response is not approval. A gate that changes mathematics requires a new frozen specification and hashes.
2. Record that instruction verbatim with source thread and time in a new gate decision artifact; do not overwrite the preparation gate.
3. Implement runner, generator, solver, verifier and output schema within this project. Record actual code paths and exact argv before executing them. There is intentionally no claimed runnable research command yet.
4. Test controls and fixtures under the aggregate budget, then freeze code/input hashes and actual Python/platform versions. Any control failure blocks research.
5. Run the bounded worker. Every output uses a fresh run directory; no overwritten results. Record start/end UTC, argv, working directory, CPU affinity, interpreter path/version, OS/hardware, no randomness, code/input SHA-256 before and after, exit status, actual CPU/peak memory, caps, stop reason and hashes of all outputs. Do not capture credentials or unrelated environment contents.
6. Produce concise `report.md` and machine-readable outputs. Outcome is one of finite assertion independently verified, counterexample independently verified, discrepancy, resource-limited partial, or launch/control failure. A successful process exit alone is insufficient.

No literature search, external communication, publication, recurring task, account mutation, Pi activity, trading activity or other-project source edit is part of this run. The separate literature worker owns prior-art checking. There is no installed package requirement; use standard-library tooling already present.
