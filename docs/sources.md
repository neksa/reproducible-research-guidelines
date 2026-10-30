# Research sources and evidence limits

The evidence supports exact input preservation, executable methods, provenance capture, explicit validation, and durable result access.

Research date: 2026-10-29.
The sources below include research papers, community principles, standards, and official software documentation.
The asynchronous record model and publication protocol are recommendations that combine these sources.
No cited source establishes that one tool guarantees reproducible research.

## Foundations

| Source | Contribution | Limit |
| --- | --- | --- |
| [National Academies, 2019](https://www.nationalacademies.org/read/25303/chapter/3) | Distinguishes computational reproduction from replication with new data. | Terminology varies across disciplines. |
| [Sandve et al., 2013](https://doi.org/10.1371/journal.pcbi.1003285) | Connects data, code versions, execution steps, intermediate results, and figures. | It provides practical guidance without specifying a software architecture. |
| [FAIR principles, 2016](https://doi.org/10.1038/sdata.2016.18) | Establishes findability, accessibility, interoperability, and reuse principles. | FAIR does not certify successful recomputation. |
| [FAIR4RS, 2022](https://doi.org/10.1038/s41597-022-01710-x) | Addresses software identity, versions, provenance, dependencies, and licensing. | The principles require concrete implementation choices. |
| [W3C PROV-DM, 2013](https://www.w3.org/TR/prov-dm/) | Defines entities, activities, responsible agents, derivations, and collections. | It does not schedule work or preserve artifact bytes. |
| [Huber et al., 2020](https://doi.org/10.1038/s41597-020-00638-4) | Demonstrates automated scientific workflows with persistent, queryable provenance through AiiDA. | Its design provides implementation evidence without requiring adoption of AiiDA. |
| [Leo et al., 2024](https://doi.org/10.1371/journal.pone.0309210) | Introduces Workflow Run RO-Crate for interoperable execution provenance. | Packaging metadata does not validate scientific conclusions. |

## Documented tool behavior

| Source | Verified behavior relevant to these guidelines |
| --- | --- |
| [DVC pipeline files](https://dvc.org/doc/user-guide/project-structure/dvcyaml-files) | Declared stages, dependencies, outputs, parameters, and resolved lockfile contents |
| [DVC run cache](https://dvc.org/doc/user-guide/pipelines/run-cache) | Stage-output reuse and the effect of `cache: false` |
| [DVC reproduction](https://dvc.org/doc/command-reference/repro) | Stage execution, output handling, force options, and run-cache controls |
| [DVC push](https://dvc.org/doc/command-reference/push) | Separate transfers for artifact contents and Git-managed metadata |
| [DVC pull](https://dvc.org/doc/command-reference/pull) | Retrieval of recorded artifact versions from remote storage |
| [DVC garbage collection](https://dvc.org/doc/command-reference/gc) | Retention scopes, remote deletion, and shared-cache risks |
| [PyTorch reproducibility](https://docs.pytorch.org/docs/2.15/notes/randomness.html) | Limits across platforms and releases; control of randomness and nondeterministic operations |
| [Kubernetes Jobs](https://kubernetes.io/docs/concepts/workloads/controllers/job/#handling-pod-and-container-failures) | Retries, partial-output handling, concurrency, and possible duplicate execution |
| [Nextflow caching and resuming](https://docs.seqera.io/nextflow/cache-and-resume) | Resume requires task-cache metadata and corresponding work outputs |

Documentation describes tool behavior at the research date.
Pin tool versions and verify these contracts in the environment that executes the research.

## Scientific and agent evaluation

| Source | Contribution | Limit |
| --- | --- | --- |
| [Kapoor and Narayanan, leakage research](https://arxiv.org/abs/2207.07048) | Examines data leakage and its effects on ML-based scientific claims. | Leakage checks depend on the scientific unit of independence. |
| [REFORMS](https://arxiv.org/abs/2308.07832) | Provides reporting guidance for ML-based science. | A reporting checklist does not replace validation. |
| [AI Agents That Matter, 2024](https://arxiv.org/abs/2407.01502) | Examines cost, holdout design, overfitting, and reproducibility in agent evaluation. | Its evaluated benchmarks do not establish biological reliability. |
| [Baek and Pradel, 2026, version 2](https://arxiv.org/abs/2602.10046v2) | Produces reproduction scripts that users can inspect and execute independently of the agent. | This preprint evaluates software-engineering artifacts. |
| [OpenTelemetry agent spans](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-agent-spans.md) | Defines agent and tool telemetry fields. | The document declares Development status. |

## Boundaries of the recommendations

The proposed calculation/request/attempt model is an engineering synthesis.
Its field names do not constitute a new standard.
Existing platforms can satisfy the same requirements with different schemas.

The guidance does not prescribe a universal numerical tolerance, replicate count, convergence threshold, or retention period.
Choose these values from the method, scientific claim, data sensitivity, and recovery cost.
Record those choices before evaluating results.

Agent response replay and repeated agent execution answer different questions.
The sources do not establish universal bitwise reproduction for hosted models or complete agent trajectories.
Preserve observable evidence and state the tested limits.
