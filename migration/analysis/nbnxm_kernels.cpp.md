# Analysis: nbnxm/Non-bonded Kernels

## File Location
- **2016.3 (gromacs-ls)**: `src/gromacs/gmxlib/nonbonded/` (NOTE: different directory!)
- **2025.4 (gromacs-ls-2025.4)**: `src/gromacs/nbnxm/`
- **Kernel templates (2025.4)**: `src/gromacs/nbnxm/kernel_file_generator/*` (.pre templates, generated at build)

## Functionality in 2016.3
The non-bonded kernels calculate van der Waals and electrostatic interactions between atoms. Local stress modifications were added to distribute pair interaction stress.

### Key Modifications in 2016.3

1. **`nb_kernel.h`** (line ~45):
   - Added `int *x_id` - atom indices for local stress
   - Added `bool bCoulEwald` - to track if using Ewald

2. **Kernel reference implementations**:
   - `nbnxn_kernel_ref_inner.h` - inner kernel loop
   - `nbnxn_kernel_ref_outer.h` - outer kernel loop
   - Added atom ID tracking for stress distribution

3. **`nbnxn_atomdata.cpp`** (lines 276-388):
   - Added atom ID array `xnb_id` 
   - Tracks which real atom each padded atom corresponds to
   - Sets `fakeid = -1` for padding atoms

4. **Kernel modifications**:
   - Added elasticity calculations for VdW and Coulomb
   - Impulse correction terms for stress
   - Born term elasticity for generalized Born

### Required Changes in 2025.4

The 2025.4 architecture is completely different - it uses `nbnxm` instead of `nbnxn`.

1. **Understand 2025.4 nbnxm architecture**:
    - Check `src/gromacs/nbnxm/` directory and the kernel generator templates
    - SIMD CPU kernels are generated from `.pre` templates at build time
    - GPU kernels exist (CUDA/SYCL) and will need a separate stress path or explicit disablement

2. **Key changes needed**:

   a. **Atom indexing**:
      - Add atom ID tracking to kernel data structures
      - Similar to 2016.3's `xnb_id` array

   b. **Force accumulation**:
      - After calculating pairwise forces
      - Call `locals_grid->DistributeInteraction(2, r_ij, f_ij, ...)`

   c. **Kernel template modifications**:
      - Identify the inner kernel that calculates forces
      - Add stress distribution call

3. **Specific locations to check**:
    - `nbnxm/nbnxm.cpp` - main dispatch and data flow
    - `nbnxm/atomdata.*` (if present) or equivalent atom-data structures
    - `nbnxm/kernel_file_generator/*` for the inner force loops
    - GPU kernel files if present (CUDA/SYCL)

## Critical Notes
⚠️ The non-bonded kernel modifications are the most complex part of the port:
- 2016.3 uses legacy nbnxn (with 'n')
- 2025.4 uses nbnxm (with 'm') - major rewrite
- GPU kernels are substantially different from CPU kernels
- SIMD optimizations in 2025.4 may be incompatible with stress calculations

The workaround may be to:
1. Use CPU-only mode for local stress calculations
2. Use reference (non-SIMD) kernels when computing local stress
