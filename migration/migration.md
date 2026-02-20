# Migration Changelog

## Understanding

Looking at the diff between Gromacs v2016.3 and v2025.4
[here](./file-structure-changes.out) it is basically impossible to determine
what the relationship between the two structures are. Therefore I think our
efforts need to be focused on understanding where Gromacs-LS v2016.3 differs
from Gromacs v2016.3, then map those changes into the 2025.4 architecture.

## Current Focus

- The local-stress hook in `mdrun/md.cpp` is in place, but listed forces,
  constraints, and non-bonded kernels still lack stress distribution.
- Checkpoint integration should move into `fileio/checkpoint.cpp` so
  restarts preserve local stress state.
- See `migration/analysis/SUMMARY.md` for the latest porting status.
