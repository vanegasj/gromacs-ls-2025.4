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

1. **Locate update functions** in 2025.4:
   - May have been refactored
   - Check `src/gromacs/mdlib/update.cpp`

2. **Add kinetic stress distribution**:
   - After velocity update in integration loop
   - Use: `locals_grid->DistributeKinetic(mass, x, v_half, v_current)`
   - The formula: σ_kin = -m * v ⊗ v

3. **Update md.cpp** if not already done:
   - Already has some local stress modifications (lines 2280-2330)
   - Verify kinetic stress is properly distributed

4. **Thread synchronization**:
   - If using OpenMP, ensure thread-safe access to stress grid
   - May need reduction operations

## Critical Notes
- Kinetic stress is crucial for accurate total stress
- Must use velocities at correct time level (half-step for Verlet)
- Mass weighting is important for correct stress distribution
- The 2025.4 version appears to already have some kinetic stress code in md.cpp - verify it's complete
