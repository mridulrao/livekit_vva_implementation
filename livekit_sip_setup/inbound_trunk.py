from livekit import api
from livekit.protocol.sip import (
    CreateSIPInboundTrunkRequest,
    CreateSIPDispatchRuleRequest,
    SIPDispatchRule,
    SIPDispatchRuleIndividual,
    SIPInboundTrunkInfo
)
import asyncio
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


'''
Each trunk has its own dispatch rule. Based on dispatch rule 
 - Create private room for each call 
 - Create a shared room for each call 


 ** Current Implementation **
  - Create private room for each call

'''

async def setup_livekit_trunk_dynamic():
    # Initialize LiveKit API
    livekit_api = api.LiveKitAPI()
    
    try:
        # Step 1: Create inbound trunk
        print("Creating inbound trunk...")

        trunk = SIPInboundTrunkInfo(
          name = "Auto Inbound trunk",
          numbers = [str(os.getenv('TWILIO_PHONE_NUMBER'))],
        )
        
        request = CreateSIPInboundTrunkRequest(
          trunk = trunk
        )
        
        trunk_response = await livekit_api.sip.create_sip_inbound_trunk(request)

        print(f"Trunk Created: {trunk_response.sip_trunk_id}")
        
        # Step 2: Create dynamic dispatch rule
        print("\nCreating dynamic dispatch rule...")
        rule = SIPDispatchRule(
            dispatch_rule_individual=SIPDispatchRuleIndividual(
                room_prefix="number-"  # Each caller gets a room prefixed with "call-"
            )
        )
        
        dispatch_request = CreateSIPDispatchRuleRequest(
            rule=rule,
            name="Dynamic Room Dispatch",
            trunk_ids=[trunk_response.sip_trunk_id], # can add multiple
            hide_phone_number=False
        )
        
        try:
            dispatch_response = await livekit_api.sip.create_sip_dispatch_rule(dispatch_request)
            print(f"Successfully created dynamic dispatch rule: {dispatch_response}")
        except api.twirp_client.TwirpError as e:
            print(f"Error creating dispatch rule: {e.code} - {e.message}")
            
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        await livekit_api.aclose()

async def main():
    print("Setting up LiveKit SIP trunk with dynamic room dispatch...")
    await setup_livekit_trunk_dynamic()
    print("\nSetup complete!")

if __name__ == "__main__":
    asyncio.run(main())
