import sys
from pathlib import Path
import re

# Add parent directory to Python path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

import logging

from dotenv import load_dotenv
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    JobProcess,
    WorkerOptions,
    cli,
    llm,
)
from livekit.agents.pipeline import VoicePipelineAgent
from livekit.plugins import openai, deepgram, silero


load_dotenv()
logger = logging.getLogger()

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

# def prewarm(proc: JobProcess):
#     proc.userdata["vad"] = silero.VAD.load()

def prewarm(proc: JobProcess):
    try:
        # Initialize services
        services = ServiceInstances()
        services.initialize_if_needed()
        
        # Store services in process userdata
        proc.userdata["services"] = services
        
        # Initialize VAD
        proc.userdata["vad"] = silero.VAD.load(min_speech_duration=0.2, min_silence_duration=0.5)
        
        logger.info("Prewarm completed successfully")
    except Exception as e:
        logger.error(f"Prewarm failed: {str(e)}")
        raise

#### PREWARM FUNCTION ####

from instructions import INSTRUCTIONS

async def entrypoint(ctx: JobContext):
    initial_ctx = llm.ChatContext().append(
    role="system",
    text=INSTRUCTIONS)

    def on_participant_disconnected(participant):
        logger.info(f"Participant disconnected: {participant.identity}")
            # Handle any cleanup or logging you need when call ends

    logger.info(f"connecting to room {ctx.room.name}")
    phone_number = extract_phone_number(ctx.room.name)
    logger.info(f"Extracted phone number: {phone_number}")

    services = ctx.proc.userdata["services"]
    fnc_ctx = ServiceDeskFunctionContext(updated_functions, 
                                         phone_number,
                                         services.get_service_now(),
                                         services.get_ms365_group())

    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    # Wait for the first participant to connect
    participant = await ctx.wait_for_participant()
    logger.info(f"starting voice assistant for participant {participant.identity}")
    ctx.room.on("participant_disconnected", on_participant_disconnected)


    assistant = VoicePipelineAgent(
        vad=ctx.proc.userdata["vad"],
        stt=openai.STT(),
        llm=openai.LLM(model="gpt-4o"),
        tts=openai.TTS(),
        chat_ctx=initial_ctx,
        fnc_ctx=fnc_ctx,
    )

    assistant.start(ctx.room, participant)

    # The agent should be polite and greet the user when it joins :)
    await assistant.say("Hello, I'm FIONA, your IT support assistant. Before I can help you, please provide your employee ID for verification.", allow_interruptions=True)



if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            prewarm_fnc=prewarm,
        ),
    )
