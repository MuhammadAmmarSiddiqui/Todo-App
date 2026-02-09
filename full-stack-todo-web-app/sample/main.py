from connection import config
import asyncio
from agents import (Agent, Runner, input_guardrail, GuardrailFunctionOutput, InputGuardrailTripwireTriggered)
from pydantic import BaseModel

class MessageOutput(BaseModel):
    response: str
    isTempBelow: bool

FatherAgent = Agent(
    name = "Father Agent",
    instructions="""You are a father agent.
                    Your task is to ensure that children should not set air conditioner
                    temperature below 26 degrees celsius. If they do stop them gracefully.""",
    output_type= MessageOutput
                    
)

@input_guardrail
async def Father(ctx, agent, input):
    result = await Runner.run(FatherAgent, input, run_config=config)
    #print(result.final_output)
    return GuardrailFunctionOutput(
        output_info=result.final_output.response,
        tripwire_triggered=result.final_output.isTempBelow
    )

AirConditioner = Agent(
    name = "Air Conditioner",
    instructions="""You are a children agent.
                    Your task is to set Air Conditioner Temperature.""",
    input_guardrails=[Father]
)

async def main():
    try:
        result= await Runner.run(AirConditioner,
                                "Can you set Air Conditioner temperature up to 26 degree celsius.",
                                run_config=config)
        print(result.final_output)
    except InputGuardrailTripwireTriggered:
        print("Sorry, I am not authorized to run air conditioner below 26 degree celsius.")
    

if __name__ == "__main__":
    asyncio.run(main())