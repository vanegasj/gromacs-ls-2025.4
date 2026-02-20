# Analysis: ewald/PME (Electrostatics)

## File Location
- **2016.3 (gromacs-ls)**: `src/gromacs/ewald/pme.cpp`, `ewald.cpp`, `pme-pp.cpp`
- **2025.4 (gromacs-ls-2025.4)**: `src/gromacs/ewald/pme.cpp`, `src/gromacs/ewald/ewald.cpp`, `src/gromacs/ewald/long_range_correction.cpp`

## Functionality in 2016.3
The PME (Particle Mesh Ewald) implementation calculates electrostatic interactions. In gromacs-ls, modifications were added to distribute the reciprocal space (k-space) stress contributions.

### Key Modifications

1. **`ewald.cpp`**:
   - Added include: `#include "mdstress/mds_stressgrid.h"`
   - Function: `gmx_ewald` (or similar)
   - Added locals_grid parameter
   - Note: The k-space contribution is central (forces balance), but stress needs careful handling

2. **PME stress distribution**:
   - The k-space forces are calculated in Fourier space
   - Stress is distributed based on atom positions in the k-space calculation
   - Called via `locals_grid->DistributeInteraction()` for each atom

3. **Long-Range Correction** (`long-range-correction.cpp`):
   - Added local stress distribution for long-range pressure corrections

### Required Changes in 2025.4

1. **Identify PME implementation location** in 2025.4:
   - Check `src/gromacs/ewald/pme.cpp`
   - May be modularized differently

2. **Add include** to relevant ewald files (only if reciprocal-space stress is actually implemented):
    ```cpp
    #include "mdstress/mds_stressgrid.h"
    ```

3. **Modify k-space calculation**:
   - After computing reciprocal space forces
   - Distribute stress based on:
     - Which atoms contribute to each k-vector
     - The charge distribution
   - This is complex because k-space is delocalized

4. **Real-space PME**:
   - The real-space Ewald is handled in nbnxm kernels
   - May not need separate modification

5. **Reciprocal space stress**:
    - Extract per-atom forces from PME grid
    - Distribute using `locals_grid->DistributeInteraction()`
    - If this is not feasible, explicitly document the limitation and require cutoff electrostatics

## Critical Notes
⚠️ **IMPORTANT**: According to gromacs-ls documentation, PME reciprocal space stress is NOT fully implemented in the 2016.3 version:
> "No. At the moment, electrostatic contributions calculated in reciprocal space are not included in the local stress calculation."

This limitation likely persists in 2025.4. Only real-space Coulomb and short-range interactions should be included.

The workaround for users is to use Cut-off electrostatics instead of PME for local stress calculations.
