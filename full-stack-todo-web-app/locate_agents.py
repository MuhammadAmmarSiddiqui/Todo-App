import importlib.util
import os

try:
    spec = importlib.util.find_spec('agents')
    if spec and spec.origin:
        print(f"agents location: {spec.origin}")
        print(f"agents dir: {os.path.dirname(spec.origin)}")
    else:
        print("agents not found")
except Exception as e:
    print(f"Error: {e}")
