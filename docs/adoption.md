# Adopt reproducible research practices

First make one real result reproducible from exact inputs with a documented command.
Extend the same record structure to the remaining results.

## Choose the minimum infrastructure

| Workload | Starting point | Add when necessary |
| --- | --- | --- |
| Small analysis | Git, immutable input files, scripts, environment lock, and result manifest | DVC for data versions and incremental execution |
| Expensive pipeline | DVC or an existing workflow engine, durable artifacts, and execution records | Checkpoints and scheduler integration |
| Concurrent asynchronous work | Durable requests, attempts, and collection snapshots | Reconciliation and conditional result publication |
| Agentic research | The same scientific workflow plus model, context, and action records | Response replay and repeated agent evaluation |

These are implementation recommendations.
One platform can satisfy several rows.
A database is optional when versioned files adequately preserve the records.

## Establish one reproducible result

1. Choose a reported figure, table, or numerical conclusion.
2. Identify the exact input files, metadata, and reference versions that produce it.
3. Put every transformation and analysis choice into code or explicit configuration.
4. Bind execution to the recorded environment.
5. Preserve outputs and record the input-to-output relationships.
6. Restore the result from a clean location.
7. Recompute an affordable representative case and compare against declared criteria.

Record the commands, environment, comparison results, and remaining limitations.
Use the [DVC example](../examples/dvc/README.md) to examine the distinction between restoration and execution.

## Add durable asynchronous execution

Before submitting expensive work, assign a calculation specification and request identity.
Preserve an attempt record for every execution.
Finalize collections independently of scheduler batches.

Implement the [failure checks](asynchronous-compute.md#verify-the-design-with-failures) before depending on automatic retries.
Retain evidence of partial work and failures.
An unavailable scheduler record must not erase the scientific history.

## Add agents without changing the acceptance criteria

Require agents to write executable methods and explicit calculation specifications.
Capture model inputs, observable actions, source evidence, and interventions.
Link the agent run to the calculations it requests and the artifacts it produces.
Use independent checks to evaluate those artifacts.

When the agent changes a method, preserve the previous specification and the reason for the change.
Protect evaluation data from exploratory selection.
Record unsuccessful attempts and the complete search budget.

## Decide what to retain

| Material | Retention rule |
| --- | --- |
| Original observations and external snapshots | Preserve when access conditions permit. Document any access restrictions. |
| Inputs and outputs behind a release | Preserve for the declared release lifetime. |
| Metadata, specifications, attempt history, and collection membership | Preserve with the scientific record. |
| Expensive intermediates | Preserve when reconstruction cost or diagnostic value justifies storage. |
| Checkpoints and workflow caches | Preserve while restart or reuse depends on them. |
| Temporary batches and scratch files | Delete after durable records and recovery requirements no longer need them. |

Set the retention period, owner, storage location, and recovery procedure explicitly.
For costly work, document the tradeoff between storage cost and recomputation cost.
Keep an independent backup of records that the research cannot reconstruct.

## Check a release

- Every claim identifies the result or collection version that supports it.
- Every result identifies its method, inputs, environment, and producing attempt.
- Every referenced artifact resolves to preserved content with the expected hash.
- Every exclusion and missing member appears in the collection record.
- Restoration and reproduction claims identify the checks that actually pass.
- The release includes limitations, access requirements, resource estimates, and a responsible contact.

Use the [record template](../templates/provenance.yaml) as a field checklist.
Adapt it to the existing workflow engine or registry.
The template does not implement a scheduler, validator, or provenance standard.

Before computing digests, define the canonical serialization and the fields that contribute to each digest.
Exclude the digest itself and any identifier that derives from it.
Maintain an artifact inventory that maps each hash to its location and access conditions.
Document unknown and inapplicable values explicitly.
