# Inspect a small DVC workflow

This example demonstrates dependency tracking, cache reuse, artifact restoration, and deliberate recomputation.

The input contains invented integer values and one missing value.
It provides no biological evidence.
The calculation uses the Python standard library.
The [verification record](verification.json) identifies the tested code, environment, artifact hashes, and checks.

## Run in an isolated directory

Prerequisites: Git, a working Python interpreter, and DVC.
Verification uses Python 3.12.12 and DVC 3.66.1 on macOS arm64.
Check which executables your environment exposes before execution.
The example does not supply a production environment lock.
For research use, apply the [environment requirements](../../README.md#preserve-and-enforce-the-execution-environment).

From the guidelines repository root, run these commands:

```sh
python --version
dvc --version
example_dir=$(mktemp -d)
cp -R examples/dvc/. "$example_dir/"
cd "$example_dir"
git init
dvc init
dvc cache dir --local "$example_dir/.dvc/cache"
dvc add input.json
dvc repro
```

The `summarize` stage selects values at or above `minimum_value`.
It preserves selected, excluded, and missing identifiers in `summary.json`.
The `report` stage generates `report.md` from that summary.

For the original inputs, the selected sum is 10.
The summary records five expected records, three selected records, one missing record, and one excluded record.

## Inspect dependency tracking and caching

| Action | Expected behavior |
| --- | --- |
| Repeat `dvc repro` without changes. | DVC skips both stages. |
| Change `minimum_value` from 2 to 3 in `params.json`. | Both stages execute. The selected sum becomes 8. |
| Restore `minimum_value` to 2 and run again. | DVC can restore the earlier outputs from its run cache. |
| Change the report heading in `report.py`. | DVC executes the report stage without repeating the calculation. |
| Add a duplicate identifier to `input.json`. | The summary stage fails and DVC stops downstream execution. |

Before testing restoration or recomputation, restore the original input, parameter, and script contents.
Then run `dvc repro` again.

DVC's run cache reuses recorded stage results. [DVC run cache](https://dvc.org/doc/user-guide/pipelines/run-cache).
Treat a cache hit as reuse, not an independent scientific replicate.

## Force fresh computation

For this small example, both stages complete quickly.
For real workloads, check the resource budget before forcing execution.

```sh
dvc repro --force --no-run-cache
```

Both stage commands execute again.
Their output hashes match the original hashes in the verified environment.
The DVC flags control stage execution and run-cache reuse. [DVC reproduction](https://dvc.org/doc/command-reference/repro).

## Restore artifacts without a shared cache

The following remote is a temporary local directory for demonstration.
For research releases, choose storage with an explicit owner, retention policy, and backup procedure.

First upload artifacts and record the code and DVC metadata:

```sh
remote_dir=$(mktemp -d)
dvc remote add --local -d example "$remote_dir"
dvc push
git add .
git commit -m "Record the example pipeline and artifact versions"
```

Next create a clean clone and configure its independent cache:

```sh
clone_dir=$(mktemp -d)
git clone --no-hardlinks "$example_dir" "$clone_dir"
cd "$clone_dir"
dvc cache dir --local "$clone_dir/.dvc/cache"
dvc remote add --local -d example "$remote_dir"
dvc pull
```

Git restores code and DVC metadata.
DVC retrieves `input.json`, `summary.json`, and `report.md` from the remote. [DVC pull](https://dvc.org/doc/command-reference/pull).
Compare their hashes with the [verification record](verification.json).
For a separate recomputation check, run `dvc repro --force --no-run-cache` in this clone.

## Interpret the verification scope

The local checks cover stage execution, parameter changes, reporting independence, caching, restoration, recomputation, and duplicate-identifier rejection.
They do not test cloud storage, distributed scheduling, agent behavior, or scientific validity.
The [asynchronous design](../../docs/asynchronous-compute.md) describes those execution boundaries separately.
