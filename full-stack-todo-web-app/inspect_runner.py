import sys
from pathlib import Path
import inspect

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

try:
    from agents import Runner
    print(f"Runner.run signature: {inspect.signature(Runner.run)}")
    print(f"Runner.run doc: {Runner.run.__doc__}")
except ImportError:
    print("Could not import agents.Runner")
except Exception as e:
    print(f"Error: {e}")
