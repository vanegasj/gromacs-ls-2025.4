# Analysis: constr.cpp (Constraints)

## File Location
- **2016.3 (gromacs-ls)**: `src/gromacs/mdlib/constr.cpp`
- **2025.4 (gromacs-ls-2025.4)**: Need to locate - constraints may be in different location

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

1. **Locate constraint implementation** in 2025.4:
   - Check `src/gromacs/mdlib/` for constraint files
   - SETTLE may be in separate file
   - LINCS may have been rewritten

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

3. **Update headers** in `constr.h`

## Critical Notes
- The 2025.4 constraint implementation may use different algorithms
- SETTLE may have been optimized for SIMD
- Check if constraints still have the same interface
- Parallelization (OpenMP) may require thread synchronization for stress grid
