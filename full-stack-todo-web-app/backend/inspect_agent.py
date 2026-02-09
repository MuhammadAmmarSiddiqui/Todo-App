import inspect
try:
    from agents import Agent, Runner
    print("Agent.__init__ signature:", inspect.signature(Agent.__init__))
    print("Runner.run signature:", inspect.signature(Runner.run))
except ImportError:
    print("Could not import agents")
except Exception as e:
    print(e)
