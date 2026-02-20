# Analysis: bonded.cpp (listed_forces)

## File Location
- **2016.3 (gromacs-ls)**: `src/gromacs/listed-forces/bonded.cpp`
- **2025.4 (gromacs-ls-2025.4)**: `src/gromacs/listed_forces/bonded.cpp`

## Functionality in 2016.3
The bonded.cpp file in gromacs-ls contains modifications to distribute stress from bonded interactions (bonds, angles, dihedrals, improper dihedrals) to the local stress grid.

### Key Functions Added

1. **`locals_bonds_distribute_stress_born()`** (lines 122-144)
   - Distributes bond stress with Born term support
   - Calls `locals_grid->DistributeInteraction(2, R, F, &phi, &kappa)`

2. **`locals_angles_distribute_stress()`** (lines 155-187)
   - Distributes angle stress 
   - Calls `locals_grid->DistributeInteraction(3, lpR, lpF, nullptr, nullptr)`

3. **`locals_angles_distribute_stress_born()`** (lines 192-246)
   - Distributes angle stress with Born term
   - Includes phi and kappa calculations for elasticity

4. **Dihedral stress distribution** (lines 1800-1965)
   - `calc_proper_dihedrals_locals()` - Proper dihedrals
   - `calc_improper_dihedrals_locals()` - Improper dihedrals
   - `calc_rb_dihedrals_locals()` - Ryckaert-Bellemans dihedrals
   - Support for CMAP corrections

### Required Changes in 2025.4

The 2025.4 version uses different function signatures and code organization. The bonded forces are implemented in `listed_forces/bonded.cpp` but WITHOUT local stress modifications.

**Specific changes needed:**

1. **Add include**:
   ```cpp
   #include "mdstress/mds_stressgrid.h"
   ```

2. **Add stress distribution functions**:
   - Copy `locals_bonds_distribute_stress_born()` from 2016.3
   - Copy `locals_angles_distribute_stress()` from 2016.3
   - Copy `locals_angles_distribute_stress_born()` from 2016.3
   - Copy dihedral stress distribution functions

3. **Modify existing bond functions** to call stress distribution:
   - `bonded_harmonic()` - add locals_grid parameter
   - `bonded_stretch()` - add locals_grid parameter
   - `angle_bend()` - add locals_grid parameter
   - `angle_bend_harmonic()` - add locals_grid parameter
   - `proper_dihedral()` - add locals_grid parameter
   - `improper_dihedral()` - add locals_grid parameter
   - `dihedral_proper()` - RB dihedrals

4. **Update function signatures** in `bonded.h` to include:
   ```cpp
   mds::StressGrid *locals_grid
   ```

5. **Update call sites** in `listed_forces.cpp` to pass locals_grid

## Critical Notes
- The 2025.4 code uses C++11 and different coding conventions
- Some function names may have changed (check `bonded.h` for current names)
- Need to maintain compatibility with both single and double precision builds
- Born term support requires careful handling of implicit vs explicit hydrogen bonds
- There are GPU listed-forces paths (`listed_forces_gpu_*`); local stress is CPU-only unless explicitly added
