"""
Quick test to verify setup is correct
Run: python test_setup.py
"""

print("Testing project setup...\n")

# Test 1: Check files exist
import os
files_to_check = [
    'manage.py',
    'backend/settings.py',
    'feed/models.py',
    'feed/views.py',
    'feed/serializers.py',
    'create_data.py',
]

print("✓ Checking files...")
for file in files_to_check:
    if os.path.exists(file):
        print(f"  ✓ {file}")
    else:
        print(f"  ✗ {file} MISSING!")

# Test 2: Check Python syntax
print("\n✓ Checking Python syntax...")
import py_compile
python_files = [
    'feed/models.py',
    'feed/views.py',
    'feed/serializers.py',
]

for file in python_files:
    try:
        py_compile.compile(file, doraise=True)
        print(f"  ✓ {file}")
    except Exception as e:
        print(f"  ✗ {file}: {e}")

print("\n" + "="*50)
print("SETUP CHECK COMPLETE!")
print("="*50)
print("\nNext steps:")
print("1. Activate venv: venv\\Scripts\\activate (Windows) or source venv/bin/activate (Mac/Linux)")
print("2. Load data: python create_data.py")
print("3. Start server: python manage.py runserver")
print("4. Open: http://localhost:8000/api/posts/")
