with open('modified-files.txt', 'r') as f:
    files = [line.strip() for line in f]

categories = {
    'force_kernels': [],
    'neighbor_search': [],
    'io_system': [],
    'state_management': [],
    'build_system': [],
    'mdrun_core': [],
    'data_structures': [],
    'other': []
}

for file in files:
    if 'kernel' in file.lower() or 'force' in file.lower():
        categories['force_kernels'].append(file)
    elif 'nbnxn' in file or 'neighbor' in file:
        categories['neighbor_search'].append(file)
    elif 'checkpoint' in file or 'state' in file:
        categories['state_management'].append(file)
    elif 'CMake' in file or 'cmake' in file:
        categories['build_system'].append(file)
    elif 'mdrun' in file:
        categories['mdrun_core'].append(file)
    elif '.h' in file and 'types' in file:
        categories['data_structures'].append(file)
    elif any(x in file for x in ['xtc', 'trr', 'edr', 'tng', 'xdr']):
        categories['io_system'].append(file)
    else:
        categories['other'].append(file)

for cat, files in categories.items():
    if files:
        print(f"\n{cat.upper()} ({len(files)} files):")
        for f in files:  # Show first 10
            print(f"  - {f}")
        if len(files) > 10:
            print(f"  ... and {len(files) - 10} more")


