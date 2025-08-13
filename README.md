## Counting Letters via LLM

This is a small CLI program for running tests and analyzing results of large language models counting letters in words. It uses a local Python virtual environment in `.venv`, a main entrypoint `main.py`, and two helper scripts:

- `setup.sh` — creates the virtual environment and installs dependencies from `requirements.txt`.
- `run.sh` — executes the program, passing along arguments.

### Prerequisites

- Python 3 installed (and available as `python3`).
# Optional
- Bash shell (to run setup and execution scripts).

## Setup

Create the virtual environment and install dependencies:

```bash
./setup.sh
```

## Run

Use the helper script to execute the program within the virtual environment:

```bash
./run.sh [options]
```

You can also run it directly:

```bash
./.venv/bin/python main.py [options]
```

### Options

- `-t`, `--test`   — Run test on GPT-5
- `-c`, `--check`  — Print total correct and incorrect results
- `-a`, `--all`    — Print all of the results, organized

Examples:

```bash
# Run the tests
./run.sh -t

# Show totals
./run.sh -c

# Print all organized results
./run.sh -a

# Run a series of tests then print all results and totals
./run.sh -atc
```

## Results

- Test results with parameters are written under the `results/` directory as timestamped JSON files..

## TODO

- Everything

## Credits

- List Of English Words - https://github.com/dwyl/english-words