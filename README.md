# Find-and-Replace on _ChRIS_

[![Version](https://img.shields.io/docker/v/fnndsc/pl-re-sub?sort=semver)](https://hub.docker.com/r/fnndsc/pl-re-sub)
[![MIT License](https://img.shields.io/github/license/fnndsc/pl-re-sub)](https://github.com/FNNDSC/pl-re-sub/blob/master/LICENSE)
[![Build](https://github.com/FNNDSC/pl-re-sub/actions/workflows/ci.yml/badge.svg)](https://github.com/FNNDSC/pl-re-sub/actions)

A _ChRIS ds_ plugin for find-and-replace operations on text files using regular expressions.


## Usage

```bash
singularity exec docker://docker.io/fnndsc/pl-re-sub:latest resub \
    --expression ... --replacement ... \
    --inputPathFilter ... incoming/ outgoing/
```

Files inside `incoming/` matching the glob given by `--inputPathFilder`
are processed and written to `outgoing/`.

#### `--expression`

A string representing a regular expression with matching groups to search for.
Uses [Python `re`](https://docs.python.org/3/library/re.html) syntax.

#### `--replacement`

A string which may include matching groups which should be used to replace
occurrences of what is matched by the value given to [`--expression`](#--expression).

#### `--ifs`

Multiple operations can be chained one after the other using the `--ifs` option.
The value passed to `--ifs` (default `||`) is a delimiter between multiple regexes.

For example, if you wanted to first replace all `B` with `A` and then do a second
pass through the line replacing all `:(` with `:)`:

```bash
singularity exec docker://docker.io/fnndsc/pl-re-sub:latest resub \
    --expression 'B :\(' --replacement 'A :\)' --ifs ' ' \
    --inputPathFilter 'report_card.txt' incoming/ outgoing/
```

Chained operation support can be disabled by passing `--ifs ''`.

### Examples

For every `*.csv` files in the directory `incoming/`,
change dates from `MM/DD/YYYY` format to `YYYY.MM.DD` format,
and saving the results into a new directory `outgoing/`:

```bash
# set up date to be found in the incoming/ directory
mkdir incoming/ outgoing/
mv ./data.csv incoming/data.csv

# convert date formats in all files and write results into outgoing/
singularity exec docker://docker.io/fnndsc/pl-re-sub:latest resub \
    --expression '(\d\d)/(\d\d)/(\d\d\d\d)' \
    --replacement '\3.\1.\2' \
    --inputPathFilter '*.csv' incoming/ outgoing/
```

## Performance

Processing is serial using a single-thread.
When you have a large number of files, you can do parallel processing
using external tools such as _ChRIS_, `sbatch`, or GNU `parallel`.

Examples: TODO

## (Un)Planned Features

- [ ] `eval` support for dynamic replacement text generation
