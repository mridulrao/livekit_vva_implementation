from twilio.rest import Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TwilioTrunkConfigurator:
    def __init__(self):
        # Initialize Twilio client
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.client = Client(self.account_sid, self.auth_token)

    def create_trunk(self, friendly_name: str) -> str:
        """
        Create a new SIP trunk
        """
        try:
            # Create the trunk
            trunk = self.client.trunking.v1.trunks.create(
                friendly_name=friendly_name,
                domain_name=f"{friendly_name.lower().replace(' ', '-')}.pstn.twilio.com"
            )
            print(f"Created trunk: {trunk.sid}")
            return trunk.sid
        except Exception as e:
            print(f"Error creating trunk: {str(e)}")
            raise

    def add_origination_url(
        self,
        trunk_sid: str,
        friendly_name: str,
        sip_url: str,
        weight: int = 1,
        priority: int = 1
    ) -> str:
        """
        Add origination URL to the trunk
        """
        try:
            # Add the origination URL
            origination_url = self.client.trunking.v1.trunks(trunk_sid) \
                .origination_urls.create(
                    friendly_name=friendly_name,
                    sip_url=sip_url,
                    weight=weight,
                    priority=priority,
                    enabled=True
                )
            print(f"Added origination URL: {origination_url.sid}")
            return origination_url.sid
        except Exception as e:
            print(f"Error adding origination URL: {str(e)}")
            raise

    def assign_phone_number(self, trunk_sid: str, phone_number_sid: str) -> str:
        """
        Assign a phone number to the trunk
        """
        try:
            # Assign the phone number
            phone_number = self.client.trunking.v1.trunks(trunk_sid) \
                .phone_numbers.create(phone_number_sid=phone_number_sid)
            print(f"Assigned phone number: {phone_number.sid}")
            return phone_number.sid
        except Exception as e:
            print(f"Error assigning phone number: {str(e)}")
            raise

async def main():
    # Initialize configurator
    configurator = TwilioTrunkConfigurator()

    try:
        trunk_sid = configurator.create_trunk(friendly_name="Auto Twilio trunk")
        print(f"\nCreated trunk with SID: {trunk_sid}")

        # Step 2: Add origination URL (LiveKit SIP URI)
        origination_url_sid = configurator.add_origination_url(
            trunk_sid=trunk_sid,
            friendly_name="LiveKit SIP URI auto twilio trunk",
            sip_url=os.getenv('LIVEKIT_SIP_URI')
        )
        print(f"\nAdded origination URL with SID: {origination_url_sid}")

        # Step 3: Assign phone number
        phone_number_sid = os.getenv('TWILIO_PHONE_NUMBER_SID')
        if phone_number_sid:
            phone_number_assignment_sid = configurator.assign_phone_number(
                trunk_sid=trunk_sid,
                phone_number_sid=phone_number_sid
            )
            print(f"\nAssigned phone number with SID: {phone_number_assignment_sid}")
        else:
            print("\nNo phone number SID provided in environment variables")

        # Print final configuration summary
        print("\nConfiguration completed successfully!")
        print(f"Trunk SID: {trunk_sid}")
        print(f"Origination URL SID: {origination_url_sid}")
        if phone_number_sid:
            print(f"Phone Number Assignment SID: {phone_number_assignment_sid}")

    except Exception as e:
        print(f"\nError during configuration: {str(e)}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())