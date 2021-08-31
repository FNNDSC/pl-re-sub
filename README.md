# Find-and-Replace on _ChRIS_

[![Version](https://img.shields.io/docker/v/fnndsc/pl-re-sub?sort=semver)](https://hub.docker.com/r/fnndsc/pl-re-sub)
[![MIT License](https://img.shields.io/github/license/fnndsc/pl-re-sub)](https://github.com/FNNDSC/pl-re-sub/blob/master/LICENSE)
[![Build](https://github.com/FNNDSC/pl-re-sub/actions/workflows/ci.yml/badge.svg)](https://github.com/FNNDSC/pl-re-sub/actions)

A _ChRIS ds_ plugin for find-and-replace operations on text files using regular expressions.


## Usage

```bash
singularity exec docker://docker.io/fnndsc/pl-re-sub:latest resub \
    --expression ... --replacement ... \
    --inputPathFilder ... incoming/ outgoing/
```

Files inside `incoming/` matching the glob given by `--inputPathFilder`
are processed and written to `outgoing/`.

#### `--expression`

A string representing a regular expression with matching groups to search for.
Uses [Python `re`](https://docs.python.org/3/library/re.html) syntax.

#### `--replacement`

A string which may include matching groups which should be used to replace
occurrences of what is matched by the value given to [`--expression`](#--expression).


### Examples

Change dates from `MM/DD/YYYY` format to `YYYY.MM.DD` format:

```bash
mkdir incoming/ outgoing/
mv ./data.csv incoming/data.csv

singularity exec docker://docker.io/fnndsc/pl-re-sub:latest resub \
    --expression '(\d\d)/(\d\d)/(\d\d\d\d)' \
    --replacement '\3.\1.\2' \
    incoming/ outgoing/
```

## Performance

Processing is serial using a single-thread.
When you have a large number of files, you can do parallel processing
using external tools such as _ChRIS_, `sbatch`, or GNU `parallel`.

Examples: TODO
