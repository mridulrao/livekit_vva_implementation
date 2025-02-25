from __future__ import annotations

import logging
from dotenv import load_dotenv

from livekit import rtc
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    WorkerOptions,
    cli,
    llm,
)
from livekit.agents.multimodal import MultimodalAgent
from livekit.plugins import openai

load_dotenv()

from boiler_plate_implementation.function_tooling import JSONFunctionContext


load_dotenv(dotenv_path=".env.local")
logger = logging.getLogger("my-worker")
logger.setLevel(logging.INFO)

# Suppose you have a JSON array of function definitions (list of dicts)
my_json_functions = [
    {
        "name": "creat_ticket",
        "description": "Create a ticket if the issue is not resolved",
        "auto_retry": False,
        "arguments": {
            "employee_id": {
                "description": "Employee ID of the person creating ticket",
                "type": "string",
                "default": None,
                "choices": None
            }
        }
    }
]


# fnc_ctx = AssistantFnc()
fnc_ctx = JSONFunctionContext(my_json_functions)


async def entrypoint(ctx: JobContext):
    logger.info(f"connecting to room {ctx.room.name}")
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    participant = await ctx.wait_for_participant()

    run_multimodal_agent(ctx, participant)

    logger.info("agent started")


def run_multimodal_agent(ctx: JobContext, participant: rtc.RemoteParticipant):
    logger.info("starting multimodal agent")

    model = openai.realtime.RealtimeModel(
        instructions=(
            "You are an IT agent. You help with troubleshooting steps and then create tickets if the query is not resolved."
        ),
        modalities=["audio", "text"],
        voice = "alloy", # "echo" "shimmer"
        turn_detection={
            "type": "server_vad",
            "threshold": 0.6,
            "prefix_padding_ms": 300,
            "silence_duration_ms": 500
        },
        temperature=0.7, # cant be lower than 0.6
        max_output_token = 250 # 1 token per word

    )
    assistant = MultimodalAgent(model=model,
                                fnc_ctx=fnc_ctx,)

    
    assistant.start(ctx.room, participant)

    session = model.sessions[0]
    session.conversation.item.create(
        llm.ChatMessage(
            role="assistant",
            content="Please begin the interaction with the user in a manner consistent with your instructions.",
        )
    )
    session.response.create()


if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
        )
    )
