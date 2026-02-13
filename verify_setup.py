#!/usr/bin/env python3
"""
SnapCalories Setup Verification Script
Checks that all components are properly configured and ready to run.
"""

import os
import sys
from pathlib import Path


def check_python_version():
    """Check Python version is 3.11+"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 11:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python 3.11+ required (found {version.major}.{version.minor}.{version.micro})")
        return False


def check_file_structure():
    """Check that all required files and directories exist"""
    print("\n📁 Checking file structure...")

    required_items = {
        "directories": [
            "app",
            "app/api",
            "app/models",
            "app/services",
            "app/utils",
            "tests",
            "tests/unit",
            "tests/integration"
        ],
        "files": [
            "app/main.py",
            "app/config.py",
            "app/api/health.py",
            "app/api/webhooks.py",
            "app/models/message.py",
            "app/models/nutrition.py",
            "app/services/whatsapp.py",
            "app/services/vision.py",
            "app/services/nutrition.py",
            "app/services/calculator.py",
            "app/utils/image.py",
            "app/utils/formatting.py",
            "requirements.txt",
            "requirements-dev.txt",
            ".env.example",
            ".gitignore",
            "README.md"
        ]
    }

    all_exist = True

    for directory in required_items["directories"]:
        if Path(directory).is_dir():
            print(f"  ✅ {directory}/")
        else:
            print(f"  ❌ {directory}/ (missing)")
            all_exist = False

    for file in required_items["files"]:
        if Path(file).is_file():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} (missing)")
            all_exist = False

    return all_exist


def check_dependencies():
    """Check if required packages are installed"""
    print("\n📦 Checking dependencies...")

    required_packages = [
        "fastapi",
        "uvicorn",
        "pydantic",
        "pydantic_settings",
        "httpx",
        "requests",
        "huggingface_hub",
        "PIL",
    ]

    all_installed = True

    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} (not installed)")
            all_installed = False

    if not all_installed:
        print("\n  💡 Run: pip install -r requirements.txt")

    return all_installed


def check_env_file():
    """Check if .env file exists and has required variables"""
    print("\n🔐 Checking environment configuration...")

    if not Path(".env").exists():
        print("  ⚠️  .env file not found")
        print("  💡 Run: cp .env.example .env")
        print("  💡 Then edit .env with your API keys")
        return False

    print("  ✅ .env file exists")

    required_vars = [
        "WHATSAPP_API_TOKEN",
        "WHATSAPP_PHONE_NUMBER_ID",
        "WHATSAPP_VERIFY_TOKEN",
        "WHATSAPP_BUSINESS_ACCOUNT_ID",
        "USDA_API_KEY"
    ]

    # Check if variables are set (but don't print values)
    with open(".env") as f:
        env_content = f.read()

    all_set = True
    for var in required_vars:
        if f"{var}=" in env_content and not f"{var}=your" in env_content:
            print(f"  ✅ {var} (configured)")
        else:
            print(f"  ⚠️  {var} (needs configuration)")
            all_set = False

    if not all_set:
        print("\n  💡 Edit .env and add your API keys")

    return all_set


def check_syntax():
    """Check Python files compile without errors"""
    print("\n🔍 Checking Python syntax...")

    python_files = list(Path("app").rglob("*.py"))

    errors = []
    for file in python_files:
        try:
            with open(file) as f:
                compile(f.read(), file, 'exec')
        except SyntaxError as e:
            errors.append((file, e))

    if errors:
        print(f"  ❌ Found {len(errors)} syntax errors:")
        for file, error in errors:
            print(f"     {file}: {error}")
        return False
    else:
        print(f"  ✅ All {len(python_files)} Python files compile successfully")
        return True


def main():
    """Run all checks"""
    print("🍽️  SnapCalories Setup Verification\n")
    print("=" * 50)

    checks = [
        ("Python version", check_python_version),
        ("File structure", check_file_structure),
        ("Dependencies", check_dependencies),
        ("Environment config", check_env_file),
        ("Python syntax", check_syntax),
    ]

    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Error checking {name}: {e}")
            results.append((name, False))

    print("\n" + "=" * 50)
    print("\n📊 Summary:\n")

    all_passed = True
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {name}")
        if not result:
            all_passed = False

    print("\n" + "=" * 50)

    if all_passed:
        print("\n🎉 All checks passed! Ready to run SnapCalories.")
        print("\n📝 Next steps:")
        print("  1. Ensure .env is configured with your API keys")
        print("  2. Run: uvicorn app.main:app --reload")
        print("  3. Visit: http://localhost:8000/docs")
        print("  4. Set up WhatsApp webhook (see QUICKSTART.md)")
        return 0
    else:
        print("\n⚠️  Some checks failed. Please resolve the issues above.")
        print("\n💡 Tips:")
        print("  - Run ./setup.sh to install dependencies")
        print("  - Copy .env.example to .env and configure")
        print("  - See QUICKSTART.md for detailed setup")
        return 1


if __name__ == "__main__":
    sys.exit(main())
