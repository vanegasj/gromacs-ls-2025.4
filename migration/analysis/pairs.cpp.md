# Analysis: pairs.cpp (listed_forces)

## File Location
- **2016.3 (gromacs-ls)**: `src/gromacs/listed-forces/pairs.cpp`
- **2025.4 (gromacs-ls-2025.4)**: `src/gromacs/listed_forces/pairs.cpp`

## Functionality in 2016.3
The pairs.cpp file handles non-bonded pair interactions (1-4 interactions, exclusions) and distributes their stress contributions to the local stress grid.

### Key Modifications

1. **`gmx_pairs_distribute_stress()`** (lines 348-540)
   - Takes additional parameter: `mds::StressGrid *locals_grid`
   - Handles vdw and coulomb contributions separately
   - Calls `locals_grid->DistributeInteraction(2, lpR, lpF, nullptr, nullptr)`

2. **Stress contribution control**:
   - Checks `locals_grid->settings.contrib` to determine what to compute:
     - `mds_vdw` - van der Waals only
     - `mds_cou` - Coulomb only  
     - `mds_all` - Both contributions
   - Lines 471-475: Zero out contributions based on what's requested

3. **Function signature changes**:
   - `gmx_pairs()` now takes `mds::StressGrid *locals_grid` parameter
   - `gmx_pairs_distribute_stress()` added

### Required Changes in 2025.4

1. **Add include**:
   ```cpp
   #include "mdstress/mds_stressgrid.h"
   ```

2. **Add new function** `gmx_pairs_distribute_stress()`:
   - Copy from 2016.3 lines 348-540
   - Modify to match 2025.4 coding style

3. **Update `gmx_pairs()` function**:
   - Add `mds::StressGrid *locals_grid` parameter
   - Call stress distribution when locals_grid != nullptr

4. **Update header file** `pairs.h`:
   - Add parameter to function declarations

5. **Update call sites** in `listed_forces.cpp`

## Critical Notes
- In 2025.4, pair interactions may be handled differently due to the new nbnxm architecture
- Need to verify if pairs are still calculated in listed-forces or moved to nbnxm
- Check if 1-4 interactions still go through listed-forces in 2025.4
