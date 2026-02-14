# Analysis: checkpoint.cpp (File I/O)

## File Location
- **2016.3 (gromacs-ls)**: `src/gromacs/fileio/checkpoint.cpp`
- **2025.4 (gromacs-ls-2025.4)**: `src/gromacs/fileio/checkpoint.cpp`

## Functionality in 2016.3
The checkpoint code saves and loads simulation state for restarts. Local stress modifications allow saving/resuming local stress calculations.

### Key Modifications

1. **Checkpoint save** (`checkpoint.cpp` line 1519):
   ```cpp
   locals_grid.SaveCheckpoint(fn, fntemp);
   ```

2. **Checkpoint load** (`checkpoint.cpp` line 2290):
   ```cpp
   locals_grid.LoadCheckpoint(fn);
   ```

3. **Global variable declaration** (`checkpoint.h`):
   - Added include: `#include "mdstress/mds_stressgrid.h"`
   - The `locals_grid` is typically declared as extern in header

### Required Changes in 2025.4

1. **Add include** to `checkpoint.cpp`:
   ```cpp
   #include "mdstress/mds_stressgrid.h"
   ```

2. **Add checkpoint save call**:
   - Find appropriate location in checkpoint writing code
   - After other state variables are saved
   - Add: `locals_grid.SaveCheckpoint(fn, fntemp);`

3. **Add checkpoint load call**:
   - Find appropriate location in checkpoint reading code  
   - Before or after other state variables are loaded
   - Add: `locals_grid.LoadCheckpoint(fn);`

4. **Verify extern declaration**:
   - Check that `extern mds::StressGrid locals_grid;` is visible in checkpoint.cpp

## Critical Notes
- The checkpoint format may have changed in 2025.4
- Need to ensure binary compatibility for checkpoint files
- The MDStress library's SaveCheckpoint/LoadCheckpoint methods handle the actual serialization
- This enables long simulations to be checkpointed and resumed without losing accumulated stress data
