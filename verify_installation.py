#!/usr/bin/env python
"""
Installation verification script for GLUMF package.

This script checks that all components of GLUMF are correctly installed
and functioning.
"""

import sys
import importlib


def check_python_version():
    """Check Python version."""
    print("Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print(f"  ❌ Python {version.major}.{version.minor} detected")
        print(f"  GLUMF requires Python 3.7 or higher")
        return False
    print(f"  ✓ Python {version.major}.{version.minor}.{version.micro}")
    return True


def check_glumf_import():
    """Check GLUMF package import."""
    print("\nChecking GLUMF import...")
    try:
        import glumf
        print(f"  ✓ GLUMF version {glumf.__version__}")
        return True
    except ImportError as e:
        print(f"  ❌ Cannot import GLUMF: {e}")
        print("  Try: pip install -e .")
        return False


def check_dependencies():
    """Check required dependencies."""
    print("\nChecking dependencies...")
    
    required = {
        'numpy': '1.20.0',
        'pandas': '1.3.0',
        'matplotlib': '3.4.0',
        'scipy': '1.7.0',
        'lmfit': '1.0.0',
        'emcee': '3.0.0',
        'corner': '2.2.0',
    }
    
    all_ok = True
    for package, min_version in required.items():
        try:
            mod = importlib.import_module(package)
            version = getattr(mod, '__version__', 'unknown')
            print(f"  ✓ {package} {version}")
        except ImportError:
            print(f"  ❌ {package} not found (required: >={min_version})")
            all_ok = False
    
    return all_ok


def check_glumf_modules():
    """Check GLUMF submodules."""
    print("\nChecking GLUMF modules...")
    
    modules = [
        'glumf.core',
        'glumf.data_loader',
        'glumf.models',
        'glumf.plotting',
    ]
    
    all_ok = True
    for module in modules:
        try:
            importlib.import_module(module)
            print(f"  ✓ {module}")
        except ImportError as e:
            print(f"  ❌ {module}: {e}")
            all_ok = False
    
    return all_ok


def check_data_files():
    """Check data files are present."""
    print("\nChecking data files...")
    import os
    
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    
    if not os.path.exists(data_dir):
        print(f"  ❌ Data directory not found: {data_dir}")
        return False
    
    required_files = [
        'Ha_Database_20250501.xlsx',
        'EMU_GAMA_20250902',
    ]
    
    all_ok = True
    for filename in required_files:
        filepath = os.path.join(data_dir, filename)
        if os.path.exists(filepath):
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            print(f"  ✓ {filename} ({size_mb:.1f} MB)")
        else:
            print(f"  ❌ {filename} not found")
            all_ok = False
    
    return all_ok


def check_functions():
    """Check core functions are accessible."""
    print("\nChecking core functions...")
    
    try:
        from glumf import (
            schechter,
            fit_schechter_emcee,
            load_excel_sheets,
            convert_ha_to_radio,
            calculate_csfd,
            plot_luminosity_functions,
        )
        
        functions = [
            schechter,
            fit_schechter_emcee,
            load_excel_sheets,
            convert_ha_to_radio,
            calculate_csfd,
            plot_luminosity_functions,
        ]
        
        for func in functions:
            print(f"  ✓ {func.__name__}")
        
        return True
        
    except ImportError as e:
        print(f"  ❌ Cannot import functions: {e}")
        return False


def run_quick_test():
    """Run a quick functional test."""
    print("\nRunning quick functional test...")
    
    try:
        import numpy as np
        from glumf.core import schechter
        
        # Test Schechter function
        L = 10**np.array([40, 41, 42])
        phi = schechter(L, 1e-3, 1e41, -1.5)
        
        if len(phi) == 3 and all(np.isfinite(phi)):
            print("  ✓ Schechter function working")
        else:
            print("  ❌ Schechter function returned unexpected result")
            return False
        
        # Test data loading (if file exists)
        try:
            import os
            from glumf import load_excel_sheets
            
            data_path = os.path.join(os.path.dirname(__file__), 
                                    'data', 'Ha_Database_20250501.xlsx')
            if os.path.exists(data_path):
                data = load_excel_sheets(data_path)
                print(f"  ✓ Data loading working ({len(data)} sheets loaded)")
            else:
                print("  ⚠ Skipping data loading test (file not found)")
        except Exception as e:
            print(f"  ❌ Data loading failed: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Quick test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all checks."""
    print("=" * 70)
    print("GLUMF INSTALLATION VERIFICATION")
    print("=" * 70)
    
    checks = [
        ("Python Version", check_python_version),
        ("GLUMF Import", check_glumf_import),
        ("Dependencies", check_dependencies),
        ("GLUMF Modules", check_glumf_modules),
        ("Data Files", check_data_files),
        ("Core Functions", check_functions),
        ("Quick Test", run_quick_test),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n  ❌ {name} check crashed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    
    for name, result in results:
        status = "✓ PASSED" if result else "❌ FAILED"
        print(f"{name:.<50} {status}")
    
    all_passed = all(result for _, result in results)
    
    print("=" * 70)
    if all_passed:
        print("✓ ALL CHECKS PASSED!")
        print("\nGLUMF is correctly installed and ready to use.")
        print("\nNext steps:")
        print("  1. Read QUICKSTART.md for a 5-minute introduction")
        print("  2. Run examples/complete_workflow.py")
        print("  3. Check out the README.md for detailed documentation")
    else:
        print("❌ SOME CHECKS FAILED")
        print("\nPlease address the issues above.")
        print("\nCommon solutions:")
        print("  • Missing dependencies: pip install -r requirements.txt")
        print("  • Import errors: pip install -e .")
        print("  • See INSTALL.md for troubleshooting")
    print("=" * 70)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
