# Analysis: constr.cpp (Constraints)

## File Location
- **2016.3 (gromacs-ls)**: `src/gromacs/mdlib/constr.cpp`, `src/gromacs/mdlib/settle.cpp`
- **2025.4 (gromacs-ls-2025.4)**: `src/gromacs/mdlib/constr.cpp`, `src/gromacs/mdlib/settle.cpp`
- **GPU/dispatch paths (2025.4)**: `src/gromacs/mdlib/settle_gpu*.{cpp,h}`, `src/gromacs/mdlib/update_constrain_gpu_*.{cpp,h}`, `src/gromacs/modularsimulator/constraintelement.cpp`

## Functionality in 2016.3
The constraints code handles SETTLE (water), LINCS (general constraints), and SHAKE constraints. Local stress modifications distribute constraint stress contributions.

### Key Modifications

1. **SETTLE constraints** (`settle.cpp` in 2016.3):
   - Function: `settle()` 
   - Added `mds::StressGrid *locals_grid` parameter
   - Calls `locals_grid->DistributeInteraction(3, ...)` for water molecules
   - Lines: Check for `locals_grid != NULL` before distributing

2. **LINCS constraints**:
   - Function: `lincs_solver()`
   - Added locals_grid parameter
   - Distributes constraint stress for bond constraints

3. **SHAKE constraints**:
   - Function: `shake()`
   - Added locals_grid parameter

### Required Changes in 2025.4

1. **Identify the constraint entry points** in the modular simulator:
    - `modularsimulator/constraintelement.cpp` orchestrates constraint application
    - CPU implementations live in `mdlib/constr.cpp` and `mdlib/settle.cpp`
    - GPU paths are handled in `mdlib/update_constrain_gpu_*` and `mdlib/settle_gpu*`

2. **For each constraint type**:

   **SETTLE:**
   - Add `mds::StressGrid *locals_grid` to function signature
   - Calculate constraint forces
   - Call `locals_grid->DistributeInteraction(3, r, f, nullptr, nullptr)`
   - Include mass weighting for water (O:2, H:1)

   **LINCS:**
   - Add locals_grid parameter to constraint solving
   - Distribute stress for each constraint bond
   - Handle eigenvalue decomposition for constraint directions

   **SHAKE:**
   - Add locals_grid parameter
   - Similar stress distribution as LINCS

3. **Update headers** in `constr.h` and any modular simulator interfaces to pass `locals_grid`

## Critical Notes
- The 2025.4 constraint implementation is split between the modular simulator and mdlib
- SETTLE has both CPU and GPU code paths; local stress likely needs CPU-only or explicit GPU handling
- Check whether constraints are applied during GPU update paths when `updateTarget == Gpu`
- Parallelization (OpenMP/GPU) may require thread-safe accumulation or a reduction before `SumGrid()`
