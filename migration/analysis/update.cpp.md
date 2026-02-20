# Analysis: update.cpp (Kinetic Stress)

## File Location
- **2016.3 (gromacs-ls)**: `src/gromacs/mdlib/update.cpp`
- **2025.4 (gromacs-ls-2025.4)**: `src/gromacs/mdlib/update.cpp`

## Functionality in 2016.3
The update.cpp file handles velocity and position updates (integration). The kinetic contribution to stress requires velocities and positions to be distributed to the stress grid.

### Key Modifications

1. **`update_coordinates()`** (around line 1304):
   - Added `mds::StressGrid *locals_grid` parameter
   - After updating positions, may need to update stress grid

2. **`update_velocities()`** (around line 1358):
   - Added locals_grid parameter
   - Key location for kinetic stress distribution:
   ```cpp
   if (locals_grid != NULL && 
       (locals_grid->settings.contrib == mds_all || 
        locals_grid->settings.contrib == mds_kin)) {
       // Distribute kinetic stress
       locals_grid->DistributeKinetic(mass, x, v_previous, v_current);
   }
   ```

3. **md.cpp integration** (lines 1751-1801 in 2016.3):
   - The main MD loop (md.cpp) handles the actual kinetic stress calls
   - Uses half-step velocities (v_half) for kinetic energy
   - Handles both MD-VV and other integrators differently

### Required Changes in 2025.4

1. **Confirm where kinetic stress is implemented**:
    - `src/gromacs/mdrun/md.cpp` already distributes kinetic stress (around lines 2280-2330)
    - The implementation uses half-step velocities for VV and a half-step/full-step mix for leap-frog

2. **Decide whether update.cpp should be modified**:
    - If you want kinetic stress inside the integrator, thread `mds::StressGrid*` through
      `Update::update_coords()` / `update_velocities()` and add the distribution there
    - If you keep the current `md.cpp` hook, ensure the velocity/position snapshots are consistent

3. **Thread synchronization**:
    - If using OpenMP, ensure thread-safe access to stress grid
    - May need reduction operations before `SumGrid()`

## Critical Notes
- Kinetic stress is crucial for accurate total stress
- Must use velocities at correct time level (half-step for Verlet)
- Mass weighting is important for correct stress distribution
- The 2025.4 version already has kinetic stress in `md.cpp`; verify velocity time-levels for all integrators
- The current implementation calls `SaveCheckpoint(nullptr, nullptr)` per step; this is not integrated with
  the main checkpoint file format and should be reconciled
