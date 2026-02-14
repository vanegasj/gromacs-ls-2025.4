# Summary: Remaining Disparity Between gromacs-ls (2016.3) and gromacs-ls-2025.4

## Current Status

### ✅ Already Ported to 2025.4

1. **CMakeLists.txt** - MDStress library integration (lines 626-640)
2. **FindMDStress.cmake** - CMake module for finding MDStress library
3. **mdrun/md.cpp** - Core MD loop with local stress integration
4. **mdrun/legacymdrunoptions.cpp/h** - Command-line options for local stress
5. **README.md** - Updated documentation

### ❌ Not Yet Ported to 2025.4

#### Critical (Must Have)

| File                              | Description                               | Priority |
| --------------------------------- | ----------------------------------------- | -------- |
| `listed_forces/bonded.cpp`        | Bond, angle, dihedral stress distribution | HIGH     |
| `listed_forces/pairs.cpp`         | Pair interaction stress                   | HIGH     |
| `listed_forces/listed_forces.cpp` | Entry point for bonded forces             | HIGH     |
| `mdlib/force.cpp`                 | Force calculation integration             | HIGH     |
| `mdlib/constr.cpp`                | SETTLE, LINCS, SHAKE constraints          | HIGH     |

#### Important (Should Have)

| File                    | Description               | Priority |
| ----------------------- | ------------------------- | -------- |
| `ewald/pme.cpp`         | PME electrostatics        | MEDIUM   |
| `nbnxm/*`               | Non-bonded kernels        | MEDIUM   |
| `fileio/checkpoint.cpp` | Checkpoint save/load      | MEDIUM   |
| `mdlib/update.cpp`      | Kinetic stress (velocity) | MEDIUM   |

#### Lower Priority

| File                 | Description          | Priority |
| -------------------- | -------------------- | -------- |
| `topology/ifunc.cpp` | Function table setup | LOW      |
| `mdlib/sim_util.cpp` | Simulation utilities | LOW      |

## Key Technical Differences

### Architecture Changes

1. **Naming**: `listed-forces` → `listed_forces` (underscore vs hyphen)
2. **Non-bonded**: `nbnxn` → `nbnxm` (complete rewrite)
3. **External libs**: `contrib` → `external` directory

### Code Style Changes

1. C++11/14/17 features in 2025.4
2. Different naming conventions
3. Modular design changes
4. New SIMD architecture

## Implementation Strategy

### Phase 1: Bonded Forces (Highest Priority)

1. Add includes to `listed_forces/bonded.cpp`
2. Copy stress distribution functions from 2016.3
3. Update function signatures
4. Test with simple bond/angle systems

### Phase 2: Constraints

1. Find constraint implementations in 2025.4
2. Add stress distribution for SETTLE
3. Add stress distribution for LINCS
4. Add stress distribution for SHAKE

### Phase 3: Non-bonded (Most Complex)

1. Understand new nbnxm architecture
2. Add atom ID tracking
3. Add stress distribution in kernels
4. Consider GPU kernel implications

### Phase 4: Integration

1. Add checkpoint support
2. Add update.cpp kinetic stress
3. Comprehensive testing

## Testing Recommendations

1. Start with simple systems (water box)
2. Compare 1D stress profiles between 2016.3 and 2025.4
3. Test checkpoint save/load
4. Test with different force fields

## Notes

- The "from ground up" strategy is correct given the massive architectural
  changes
- Some features (e.g., PME stress) may never be fully supported due to
  fundamental physics challenges
- Consider GPU vs CPU tradeoffs for local stress calculations
