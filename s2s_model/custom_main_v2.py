from __future__ import annotations
import sys
from pathlib import Path
import re

# Add parent directory to Python path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

from dotenv import load_dotenv
load_dotenv()

from livekit import rtc
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    JobProcess,
    WorkerOptions,
    cli,
    llm,
)
from livekit.agents.multimodal import MultimodalAgent
from livekit.plugins import openai

#### FUNCTION TOOLING SETUP ####
from function_tooling.function_tool_vva import ServiceDeskFunctionContext
from function_tooling.function_def_prompts import functions

def extract_phone_number(room_name: str) -> str:
    """Extract phone number from room name format 'number-_+XXXXXXXXXX_XXXXX'"""
    match = re.search(r'number-_(\+\d+)_', room_name)
    if match:
        return match.group(1)
    return None


updated_functions = []
for func in functions: 
    updated_func = func.copy()
    updated_func["auto_retry"] = False
    updated_functions.append(updated_func)
#### FUNCTION TOOLING SETUP ####


#### PREWARM FUNCTION ####
from service_instances import ServiceInstances
def prewarm(proc: JobProcess):
    try:
        # Initialize services
        services = ServiceInstances()
        services.initialize_if_needed()
        
        # Store services in process userdata
        proc.userdata["services"] = services
        
        logger.info("Prewarm completed successfully")
    except Exception as e:
        logger.error(f"Prewarm failed: {str(e)}")
        raise
#### PREWARM FUNCTION ####

#### LOGGING FUNCTION ####
from vva_logs.config_logging import configure_logging, LogConfig, Environment
import logging
log_config = LogConfig(
    env=Environment.DEV,  
    log_level=logging.DEBUG,
    log_dir=str(parent_dir / "vva_logs"),
    log_filename="voice_agent.log",
    max_bytes=5 * 1024 * 1024,  #5MB
    backup_count=3
)
configure_logging(log_config)
logger = logging.getLogger("voice-agent")
#### LOGGING FUNCTION ####

from instructions import INSTRUCTIONS


async def entrypoint(ctx: JobContext):
    logger.info(f"connecting to room {ctx.room.name}")
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    def on_participant_disconnected(participant):
        logger.info(f"Participant disconnected: {participant.identity}")

    participant = await ctx.wait_for_participant()
    logger.info(f"starting voice assistant for participant {participant.identity}")
    ctx.room.on("participant_disconnected", on_participant_disconnected)

    run_multimodal_agent(ctx, participant)

    logger.info("agent started")


def run_multimodal_agent(ctx: JobContext, participant: rtc.RemoteParticipant):
    logger.info("starting multimodal agent")

    model = openai.realtime.RealtimeModel(
        instructions=INSTRUCTIONS,
        modalities=["text", "audio"],
        voice = "alloy", # "echo" "shimmer"
        temperature=0.7, # cant be lower than 0.6
    )
    phone_number = extract_phone_number(ctx.room.name)
    logger.info(f"Extracted phone number: {phone_number}")

    #updated_functions = prepare_functions_with_phone(functions, phone_number)
    services = ctx.proc.userdata["services"]
    fnc_ctx = ServiceDeskFunctionContext(updated_functions, 
                                         phone_number,
                                         services.get_service_now(),
                                         services.get_ms365_group())

    assistant = MultimodalAgent(model=model,
                                fnc_ctx=fnc_ctx)

    
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
            prewarm_fnc=prewarm
        )
    )
