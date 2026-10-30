# Guidelines for accountable and reproducible computational research

Preserve immutable inputs, executable methods, results, and provenance independently of the machines and batches that perform the computation.

Use Git for code and small manifests.
Use DVC for versioned data and reproducible pipelines where it fits the workflow.
Keep durable records of expensive calculations, including failed attempts.
Treat scheduler batches as temporary execution arrangements.

These recommendations apply to computational biology, simulations, machine learning, and agentic research.
The [source notes](docs/sources.md) distinguish established principles, documented tool behavior, and proposed engineering practices.
The [asynchronous compute design](docs/asynchronous-compute.md) gives implementation details for expensive workloads.

## Start with the minimum

For every reported result, preserve these items:

- Exact input versions and enough metadata to interpret them.
- Executable code, parameters, and the environment that runs them.
- Result artifacts and provenance connecting them to inputs and execution.
- Acceptance criteria and the evidence that supports the result.
- Commands and access instructions that let another researcher inspect or reproduce it.

Start with files and an existing workflow tool.
Add a persistent service only when concurrency, recovery, or query requirements need one.
Use the [adoption checklist](docs/adoption.md) to choose the next improvement.
Try the [small DVC example](examples/dvc/README.md) to inspect dependency tracking and artifact restoration.

## Define what reproduction must demonstrate

Specify the expected comparison before execution.
Different outputs need different acceptance criteria.

| Check | Required evidence |
| --- | --- |
| Restore existing results | Retrieve the recorded artifacts and verify their hashes. |
| Recompute deterministic results | Execute the recorded method and compare outputs exactly. |
| Recompute numerical results | Compare named quantities against declared absolute and relative tolerances. |
| Repeat stochastic calculations | Compare distributions or conclusions across independent runs under declared statistical criteria. |
| Replicate a scientific finding | Test the scientific question with independent data. |

Restoring an artifact demonstrates availability and integrity.
It does not demonstrate fresh computation.
Computational reproduction also does not establish biological validity.
The National Academies distinguishes computational reproducibility from replication with new data. [National Academies, 2019](https://www.nationalacademies.org/read/25303/chapter/3).

Record which checks actually pass.
State the tested dataset, environment, and scope.
If full reproduction exceeds available resources, report the partial check and the remaining requirement.

## Preserve the exact research inputs

Keep raw observations immutable.
Represent corrections and transformations as new versions with links to their sources.
Freeze every external input that can change the result.

| Input | Record and preserve |
| --- | --- |
| Dataset | Exact files, content hashes, source accession, release, acquisition date, and access conditions |
| Sample metadata | Stable identifiers, units, missing-value definitions, inclusion rules, and schema version |
| Reference resources | Genome assembly, annotation release, sequence database, ontology, or other reference version |
| Model | Weights, configuration, tokenizer when applicable, and their content hashes |
| External query | Endpoint, query, retrieval time, source version when available, and exact response |
| Analysis selection | Cohort membership, exclusions, train/test assignments, and selection code |

An accession or URL identifies a source but may not identify its exact contents.
Preserve the downloaded bytes and a checksum when access conditions permit.
If restrictions prevent preservation, document the access procedure and the resulting reproduction limit.

Preserve scientific context alongside file identity.
In biology, this includes species, sample relationships, assay metadata, and identifier mappings when relevant.
Preserve missing evidence as missing.
Do not interpret a missing result as a biological negative.

FAIR addresses discovery, access, interoperability, and reuse.
It allows authentication and authorization where necessary. [FAIR principles](https://www.nature.com/articles/sdata201618).
Give code and data explicit licenses or access terms.
Give released software versions distinct identifiers. [FAIR4RS principles](https://www.nature.com/articles/s41597-022-01710-x).

## Make the analysis executable

Encode transformations, filtering, analysis, and figure generation in scripts or workflow stages.
Keep parameters in versioned configuration files.
Declare inputs and outputs explicitly.
Record unavoidable manual decisions as structured inputs with an author and reason.

Generate tables, figures, and reported numbers from preserved result data.
Keep plotting separate from expensive computation.
Execute notebooks from a clean kernel in the documented order.
Do not depend on interactive state.
These practices extend established computational research guidance. [Sandve et al., 2013](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003285).

### Use DVC for data identity and pipeline state

Commit `.dvc` files, `dvc.yaml`, `dvc.lock`, parameters, and source code to Git.
Store large artifacts in a durable DVC remote.

| DVC component | Purpose |
| --- | --- |
| `.dvc` files | Track data or model artifacts outside ordinary Git storage. |
| `dvc.yaml` | Declare stage commands, dependencies, parameters, and outputs. |
| `dvc.lock` | Record resolved pipeline state, dependency hashes, parameter values, and output hashes. |
| Data cache | Store artifact contents for reuse. |
| Run cache | Reuse outputs from matching recorded stage executions. |
| Remote storage | Preserve and share artifact contents beyond one workspace. |

DVC checks declared dependencies.
Include source modules, configuration, environment lockfiles, reference data, and model files that influence each stage.
A path inside a manifest does not automatically become a DVC dependency.
Declare the referenced files or verify and materialize them through an explicit stage. [DVC pipeline files](https://dvc.org/doc/user-guide/project-structure/dvcyaml-files).

Use caching to avoid unnecessary computation.
Record whether a result comes from execution or cache reuse.
A cache hit does not provide an independent replicate.
DVC disables a stage's run cache when an output uses `cache: false`. [DVC run cache](https://dvc.org/doc/user-guide/pipelines/run-cache).

Use `dvc push` to upload artifact contents.
Use Git to publish code and DVC metadata.
Verify both destinations before declaring a release available. [DVC push](https://dvc.org/doc/command-reference/push).

Keep attempt history separately when the research needs it.
The pipeline lockfile describes pipeline state.
It does not supply a complete ledger of failures, retries, or human decisions.
Git history preserves committed lockfile versions. [DVC lockfile](https://dvc.org/doc/user-guide/project-structure/dvcyaml-files#dvclock-file).

### Preserve and enforce the execution environment

Record the source commit and preserve any uncommitted changes that affect execution.
Prefer clean commits for releases.
Lock dependencies and preserve the lockfile.
Pin container images by digest and preserve their availability.
Make the launcher actually use the recorded environment.

Record relevant hardware, operating system, accelerator drivers, numerical precision, and parallel execution settings.
A container does not remove dependencies on the host kernel, drivers, or hardware.
Treat these settings as part of the method when they affect results.

Record random seeds and the random number generators that use them.
Control nondeterministic operations where practical.
PyTorch explicitly limits reproducibility across releases, platforms, and CPU/GPU execution, even with identical seeds. [PyTorch reproducibility](https://docs.pytorch.org/docs/2.15/notes/randomness.html).

## Separate expensive calculations from temporary batches

Give scientific calculations stable identities before submission.
Give each execution attempt its own identity.
Preserve artifacts and metadata outside the job's temporary filesystem.

| Record | Lifetime and purpose |
| --- | --- |
| Calculation specification | Preserve exact inputs, method, parameters, environment, and requested replicate. |
| Execution attempt | Preserve actual execution details, status, logs, failures, and output references. |
| Artifact | Preserve contents, hash, format, and the attempt that produces it. |
| Collection version | Preserve exact membership and the rules that select results. |
| Scheduler batch | Preserve relevant operational facts in attempt records before removing the batch. |

This separation is a design recommendation grounded in provenance models and scientific workflow systems.
W3C PROV separates entities, activities, agents, and collections. [PROV-DM](https://www.w3.org/TR/prov-dm/).
AiiDA demonstrates automated workflows with persistent, queryable provenance. [Huber et al., 2020](https://doi.org/10.1038/s41597-020-00638-4).

Use this execution sequence:

1. Freeze the calculation specification and expected collection membership.
2. Register the request durably before submission.
3. Submit pending calculations through temporary batches.
4. Record each attempt and checkpoint expensive work when practical.
5. Upload outputs, verify integrity, and evaluate scientific acceptance criteria.
6. Finalize an immutable collection version for analysis and reporting.

Mark submission, execution success, artifact availability, and scientific acceptance separately.
A successful scheduler exit does not establish valid scientific output.

Retries must preserve their history.
Publish results idempotently, so duplicate execution cannot create duplicate collection members.
Schedulers can execute work more than once. [Kubernetes Job failure handling](https://kubernetes.io/docs/concepts/workloads/controllers/job/#handling-pod-and-container-failures).

Keep scientific batching in the specification when it changes the calculation.
Examples include minibatch size, joint normalization, input order, and cross-item interactions.
Only scheduling groups with no scientific effect can disappear without changing the recorded method.

For details, use the [asynchronous compute design](docs/asynchronous-compute.md).

## Make agentic research auditable and replayable

Require agents to produce the same research artifacts as human researchers.
Preserve executable code, explicit calculation specifications, source evidence, and validation results.
Use agent transcripts to explain actions and decisions.
Use executable workflows to reproduce calculations.

Recent research demonstrates agent-generated reproduction scripts that execute independently of the agent.
This provides a useful design pattern, with evidence currently specific to its evaluation tasks. [Baek and Pradel, 2026](https://arxiv.org/abs/2602.10046v2).

### Capture the context that determines agent actions

| Component | Minimum record |
| --- | --- |
| Agent implementation | Source commit, framework version, instructions, skills, and tool definitions |
| Model invocation | Provider, requested and returned model identifiers, settings, and available version metadata |
| Context | User task, accessible prompts, retrieved documents, memory snapshots, and conversation state |
| Actions | Ordered tool calls, exact arguments, results, timestamps, and parent execution identifiers |
| Changes | Code patches, parameter changes, dataset selections, and human interventions |
| Decisions | Hypothesis, selection rationale, stopping rule, and supporting evidence references |
| Resources | Token usage, compute use, elapsed time, limits, and retry history |

Preserve source snapshots behind retrieved evidence.
Record context truncation or summarization when it changes the agent's inputs.
Record observable actions and explicit decision summaries.
Hidden model reasoning is not a prerequisite.
Exclude credentials from traces.
Control access to sensitive prompts, data, and tool responses.
Document redactions and their effect on replay.

OpenTelemetry offers conventions for agent and tool spans.
Its agent conventions currently carry Development status. [OpenTelemetry agent spans](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-agent-spans.md).
If you adopt these conventions, pin their schema version.

### Test three separate capabilities

1. Reproduce the scientific calculation from the agent's preserved code and inputs.
2. Replay downstream processing using recorded model and tool responses.
3. Repeat the agent protocol with fresh model calls and measure outcome variation.

Response replay tests the preserved execution path.
Replay recorded responses without repeating external side effects.
Fresh calls test whether the agent reaches acceptable results again.
Preserve original responses when a provider cannot supply an immutable model version.
State that limitation instead of promising identical future decisions.

Set evaluation criteria, holdout data, resource limits, and stopping rules before evaluating the agent.
Report failures and unsuccessful trajectories alongside successes.
Measure cost as well as scientific accuracy.
Agent benchmark research identifies reproducibility, overfitting, and cost accounting as recurring problems. [Kapoor et al., 2024](https://arxiv.org/abs/2407.01502).

When an agent changes the hypothesis or method, create a new specification.
Link it to the previous specification and record the reason.
An agent's assertion of success does not replace an independent result check.

## Validate the method and the scientific claim

Choose checks that can detect consequential errors.
Version the checks and their acceptance criteria with the analysis.

| Check | Purpose |
| --- | --- |
| Small end-to-end example | Verify installation, input handling, workflow connections, and expected outputs. |
| Representative fresh calculation | Verify that the actual method executes beyond cached or synthetic results. |
| Data validation | Check identifiers, joins, units, duplicates, ranges, and missingness. |
| Statistical validation | Check uncertainty, convergence, sensitivity, and the unit of replication. |
| Independent review | Check analysis choices, evidence interpretation, and reproduction instructions. |

For predictive models, preserve exact train, validation, and test assignments.
Prevent related samples or preprocessing choices from leaking evaluation information into training.
For biology, consider patient, donor, sequence-family, and other relevant relationships.
Keep exploratory choices distinct from confirmatory tests. [REFORMS](https://arxiv.org/abs/2308.07832), [leakage research](https://arxiv.org/abs/2207.07048).

Numerical completion and scientific convergence require separate checks.
Select convergence diagnostics for the actual method.
Preserve excluded and failed cases so reviewers can inspect selection effects.

For expensive projects, run inexpensive checks routinely.
Recompute representative workloads after consequential changes and before release.
Declare the scope of every reproduction claim.

For a deliberate fresh DVC run, first use an isolated checkout and confirm the compute budget.
Check for frozen stages and caches inside the invoked tools.
Then force the selected stage to execute with `dvc repro --force --no-run-cache <stage>`.
Replace `<stage>` with the intended stage name.
DVC flags do not disable caches inside external applications. [DVC reproduction](https://dvc.org/doc/command-reference/repro).

## Release a result that someone else can inspect

Create a release manifest that connects each claim, table, and figure to its exact inputs and results.
Include these items:

- Code revision, workflow definition, parameters, and environment identifiers.
- Input and output hashes, artifact locations, and collection versions.
- Attempt provenance, validation results, and known limitations.
- Reproduction commands, resource estimates, and access requirements.
- Licenses, responsible contacts, and persistent release identifiers.

Keep underlying numerical tables available independently of figure rendering.
Use a durable archive for release artifacts and metadata.
Workflow Run RO-Crate provides an interoperable way to package workflow execution provenance. [Leo et al., 2024](https://doi.org/10.1371/journal.pone.0309210).

Test restoration from a clean location with no shared local cache.
Verify hashes and reproduce the inexpensive reporting steps.
Keep the result of this check with the release.

Assign an owner and retention policy to the archive.
Preserve raw inputs, accepted results, costly intermediates, and metadata needed to explain the findings.
Delete reconstructible scratch files only after durable preservation succeeds.

**Warning:** Cache cleanup can destroy historical reproducibility.
Before garbage collection, protect every retained release and every project that shares the storage.
DVC documents remote deletion risks and shared-cache interactions. [DVC garbage collection](https://dvc.org/doc/command-reference/gc).

A checksum cannot retrieve missing data.
Test backups and access procedures as well as metadata integrity.
