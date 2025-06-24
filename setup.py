#!/usr/bin/env python3
"""
Setup script for AI Agent Template.
"""
import os
import sys
import subprocess
import shutil


def check_python_version():
    """Check if Python version is supported."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version}")
    return True


def install_dependencies():
    """Install project dependencies."""
    print("📦 Installing dependencies...")

    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        )
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def setup_environment():
    """Setup environment configuration."""
    print("🔧 Setting up environment...")

    if not os.path.exists(".env"):
        if os.path.exists("env.example"):
            shutil.copy("env.example", ".env")
            print("✅ Created .env file from template")
            print("⚠️  Please edit .env and add your OPENROUTER_API_KEY")
        else:
            print("❌ env.example not found")
            return False
    else:
        print("✅ .env file already exists")

    return True


def run_tests():
    """Run the test suite."""
    print("🧪 Running tests...")

    try:
        subprocess.check_call([sys.executable, "-m", "pytest", "tests/", "-v"])
        print("✅ All tests passed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Some tests failed: {e}")
        return False


def validate_setup():
    """Validate the setup by running basic checks."""
    print("🔍 Validating setup...")

    try:
        # Try importing the main components
        sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
        from agent import AIAgent
        from config import settings

        print("✅ Imports successful")

        # Check configuration
        if settings.validate_api_key():
            print("✅ API key is configured")
        else:
            print("⚠️  API key not configured - edit .env file")

        return True
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        return False


def main():
    """Main setup function."""
    print("🚀 AI Agent Template Setup")
    print("=" * 40)

    # Check Python version
    if not check_python_version():
        return

    # Install dependencies
    if not install_dependencies():
        return

    # Setup environment
    if not setup_environment():
        return

    # Run tests
    if not run_tests():
        print("⚠️  Tests failed, but setup can continue")

    # Validate setup
    if not validate_setup():
        return

    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file and add your OPENROUTER_API_KEY")
    print("2. Run: python main.py")
    print("3. Choose demo mode or interactive chat")
    print("\nHappy coding! 🤖")


if __name__ == "__main__":
    main()
