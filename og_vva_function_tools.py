from prisma import Prisma
from twilio.rest import Client
from core.utils.blob_storage import Blob, AzureStorage
from typing import List
from pydantic import BaseModel
import json
import os
import requests
import tempfile
import logging

log = logging.getLogger(__name__)


class FileUploadError(Exception):
    pass


class VoiceVirtualAgent:

    def __init__(self, storage: AzureStorage):
        self.storage = storage
        self.prisma = Prisma()

    async def connect(self):
        """
        Connects to the PostgreSQL database using the Prisma client.
        """
        await self.prisma.connect()

    async def disconnect(self):
        """
        Disconnects from the PostgreSQL database using the Prisma client.
        """
        await self.prisma.disconnect()

    async def get(self, org_id: str):
        response = await self.prisma.voice_virtual_agents.find_many(
            where={"org_id": org_id}
        )
        return {"response": response}

    async def get_virtual_assistant(self, phone_number: str):
        log.debug("get_virtual_assistant called")
        response = await self.prisma.voice_virtual_agents.find_first(
            where={"phone_number": phone_number}
        )
        return {"response": response}

    async def create_virtual_assistant(
        self,
        org_id: str,
        assistant_json: dict,
        phone_number: str,
        agent_type: str,
        name: str,
        agent_id: str = None,
    ):
        assistant_json_str = json.dumps(assistant_json)

        response = await self.prisma.voice_virtual_agents.upsert(
            where={
                "phone_number": phone_number,
            },
            data={
                "create": {
                    "org_id": org_id,
                    "config": assistant_json_str,
                    # "name": assistant_json["name"],
                    "name": name,
                    "phone_number": phone_number,
                    "agent_id": agent_id,
                    "agent_type": agent_type,
                },
                "update": {
                    "org_id": org_id,
                    "config": assistant_json_str,
                    # "name": assistant_json["name"],
                    "name": name,
                    "agent_id": agent_id,
                    "agent_type": agent_type,
                },
            },
        )
        return {"response": response}

    async def upload_to_supabase(self, data: dict):
        json_data = json.dumps(data)
        container_name = "voice-virtual-agents-calls"
        blob_name = f"{data['call']['id']}.json"
        file_content = json_data.encode("utf-8")

        with tempfile.NamedTemporaryFile(delete=False, mode="wb") as tmp:
            tmp.write(file_content)
            tmp_file_name = tmp.name

        try:
            file_url = self.storage.upload_file_by_name(
                tmp_file_name, container_name, blob_name
            )
            return file_url
        except Exception as e:
            raise FileUploadError(f"File upload failed: {str(e)}")
        finally:
            os.remove(tmp_file_name)

    async def insert_to_supabase_table(self, data: dict, file_url: str, ended_at: str):
        response = await self.prisma.voice_virtual_agent_calls.upsert(
            where={"id": data["call"]["id"]},
            data={
                "create": {
                    "id": data["call"]["id"],
                    "ended_reason": data["endedReason"],
                    "details_url": file_url,
                    "ended_at": ended_at,
                    "recordingUrl": data["recordingUrl"],
                },
                "update": {
                    "ended_reason": data["endedReason"],
                    "details_url": file_url,
                    "ended_at": ended_at,
                    "recordingUrl": data["recordingUrl"],
                },
            },
        )
        return {"response": response}

    async def insert_caller_to_supabase_table(self, data: dict, userDetails: dict):
        status = data["status"]
        if status == "in-progress":
            status = "ongoing"
        data["status"] = status
        response = await self.prisma.voice_virtual_agent_calls.upsert(
            where={"id": data["call"]["id"]},
            data={
                "create": {
                    "id": data["call"]["id"],
                    "status": data["status"],
                    "caller": data["call"]["customer"]["number"],
                    "user_name": userDetails["full_name"],
                    "user_sys_id": userDetails["sys_id"],
                    "called_at": data["phoneNumber"]["number"],
                },
                "update": {
                    "status": data["status"],
                    "caller": data["call"]["customer"]["number"],
                    "user_name": userDetails["full_name"],
                    "user_sys_id": userDetails["sys_id"],
                    "called_at": data["phoneNumber"]["number"],
                },
            },
        )
        return {"response": response}

    async def insert_ticketid_to_supabase_table(self, call_id: str, ticket_id: str):
        response = await self.prisma.voice_virtual_agent_calls.upsert(
            where={"id": call_id},
            data={
                "create": {
                    "id": call_id,
                    "ticket_id": ticket_id,
                },
                "update": {
                    "ticket_id": ticket_id,
                },
            },
        )
        return {"response": response}

    async def insert_transcript(self, data: dict):
        transcript_type = data["transcriptType"]
        if transcript_type == "partial":
            transcript_type = "PartialTranscript"
        elif transcript_type == "final":
            transcript_type = "FinalTranscript"

        transcript = {
            "message_type": transcript_type,
            "text": data["transcript"],
        }

        response = await self.prisma.voice_virtual_agent_call_status.upsert(
            where={"id": data["call"]["id"]},
            data={
                "create": {
                    "call_id": data["call"]["id"],
                    "content_type": transcript_type,
                    # "content": {
                    #     "message_type": transcript_type,
                    #     "text": data["transcript"],
                    # },
                    "content": json.dumps(transcript),
                    "role": data["role"],
                },
                "update": {
                    "content_type": transcript_type,
                    # "content": {
                    #     "message_type": transcript_type,
                    #     "text": data["transcript"],
                    # },
                    "content": json.dumps(transcript),
                    "role": data["role"],
                },
            },
        )
        return {"response": response}

    async def update_virtual_assistant_server_url(
        self, org_id: str, phone_number: str, new_server_url: str
    ):
        # First, fetch the existing config
        existing_assistant = await self.prisma.voice_virtual_agents.find_first(
            where={
                "phone_number": phone_number,
            }
        )

        if not existing_assistant:
            return {"error": "Assistant not found"}

        # Parse the existing config
        existing_config = existing_assistant.config

        # Update only the serverUrl
        existing_config["serverUrl"] = new_server_url

        # Convert the updated config back to a JSON string
        updated_config_str = json.dumps(existing_config)

        # Perform the upsert operation
        response = await self.prisma.voice_virtual_agents.upsert(
            where={
                "phone_number": phone_number,
            },
            data={
                "create": {
                    "org_id": org_id,
                    "config": updated_config_str,
                    "name": existing_config["name"],
                    "phone_number": phone_number,
                },
                "update": {
                    "config": updated_config_str,
                },
            },
        )
        return {"response": response}

    async def get_latest_req_number(self, caller: str):
        # Fetch all records matching the caller, sorted by creation date in descending order
        response = await self.prisma.voice_virtual_agent_calls.find_many(
            where={"AND": [{"caller": caller}, {"ticket_id": {"not": None}}]},
            order=[{"created_at": "desc"}],
            take=1,
        )
        response = response[0].ticket_id
        if response:
            log.debug(f"Latest ticket number: {response}")
            # print(f"Latest ticket number: {response}")
            return response
        else:
            return "No ticket found"

    async def setup_voice_agent(
        self, org_id: str, area_code: str, prompt: str, agent_name: str, voice: str
    ):

        ## Procure phone number from twilio
        twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        twilio_client = Client(twilio_account_sid, twilio_auth_token)

        # Search for available phone numbers with the specified area code
        available_phone_numbers = twilio_client.available_phone_numbers(
            "US"
        ).local.list(area_code=area_code, limit=1)

        if not available_phone_numbers:
            raise Exception(
                f"No available phone numbers found with area code {area_code}."
            )

        # Procure a phone number from Twilio
        incoming_phone_number = twilio_client.incoming_phone_numbers.create(
            phone_number=available_phone_numbers[0].phone_number
        )
        log.debug(f"Phone number created: {incoming_phone_number.phone_number}")

        phone_number = incoming_phone_number.phone_number

        payload = {
            "provider": "twilio",
            "number": phone_number,
            "twilioAccountSid": twilio_account_sid,
            "twilioAuthToken": twilio_auth_token,
            "name": agent_name,
            "serverUrl": os.getenv("PHONE_SERVER_URL"),
        }

        headers = {
            "Authorization": "Bearer 4b748535-21d6-46ac-9ec5-a9fc0ccb7b99",
            "Content-Type": "application/json",
        }

        vapi_url = "https://api.vapi.ai/phone-number"

        vapi_response = requests.post(vapi_url, json=payload, headers=headers)
        log.debug(f"VAPI response: {vapi_response.text}")

        phone_number_id = vapi_response.json()["id"]
        log.debug(f"Phone number ID: {phone_number_id}")

        # Create a phone number record in the database
        phone_number_record = await self.prisma.phone_number.create(
            data={
                "org_id": str(org_id),
                "number": phone_number,
                "app_type": "voice_virtual_agent",
                "app_id": phone_number_id,
            }
        )
        log.debug(phone_number_record)

        # get voice copilot number from db
        voice_copilot_number = await self.prisma.phone_number.find_first(
            where={"app_type": "voice_copilot", "org_id": org_id}
        )

        voice_copilot_number = voice_copilot_number.number

        log.debug(f"Voice Copilot Number: {voice_copilot_number}")

        vva_config = {
            "name": agent_name,
            "model": {
                "provider": "openai",
                "model": "gpt-4o",
                "fallbackModels": ["gpt-4-0125-preview", "gpt-4-0613"],
                "temperature": 0.2,
                "maxTokens": 350,
                "emotionRecognitionEnabled": False,
                "systemPrompt": prompt,
                "functions": [
                    {
                        "name": "verify_employee",
                        "description": "Verify employee id and return employee details",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "employeeId": {
                                    "type": "string",
                                    "description": "ID of the employee to verify",
                                }
                            },
                            "required": ["employeeId"],
                        },
                    },
                    {
                        "name": "create_ticket",
                        "description": "Creates an incident ticket in ServiceNow and returns both the incident number. Examples of incidents can be 'system outage' or 'network connectivity issues' or any IT related issue.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "employeeId": {
                                    "type": "string",
                                    "description": "ID of the employee to verify",
                                },
                                "name": {
                                    "type": "string",
                                    "description": "Name of the employee",
                                },
                                "subject": {
                                    "type": "string",
                                    "description": "A brief summary of the incident (short_description in ServiceNow)",
                                },
                                "description": {
                                    "type": "string",
                                    "description": "Detailed description of the incident",
                                },
                                "impact": {
                                    "type": "string",
                                    "description": "The impact of the incident on business operations",
                                    "enum": ["1 - High", "2 - Medium", "3 - Low"],
                                },
                                "urgency": {
                                    "type": "string",
                                    "description": "The urgency with which the incident needs to be resolved",
                                    "enum": ["1 - High", "2 - Medium", "3 - Low"],
                                },
                            },
                            "required": [
                                "subject",
                                "description",
                                "employeeId",
                                "name",
                                "impact",
                                "urgency",
                            ],
                        },
                    },
                    {
                        "name": "create_service_request",
                        "description": "Creates a request in service now and returns the service request number of the created request. Examples of service request can be 'user wanting to install a software'.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "employeeId": {
                                    "type": "string",
                                    "description": "ID of the employee to verify",
                                },
                                "name": {
                                    "type": "string",
                                    "description": "name of the employee",
                                },
                                "justification": {
                                    "type": "string",
                                    "description": "Reason for creation of the request by the user.",
                                },
                                "issueDescription": {
                                    "type": "string",
                                    "description": "A description of the issue that the employee is facing.",
                                },
                            },
                            "required": [
                                "employeeId",
                                "name",
                                "issueDescription",
                                "justification",
                            ],
                        },
                    },
                    {
                        "name": "update_service_request",
                        "description": "Updates a request in service now. Examples of service request can be 'user wanting to install a software'.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "requestNumber": {
                                    "type": "string",
                                    "description": "Request number of service now request.",
                                },
                                "justification": {
                                    "type": "string",
                                    "description": "Reason for updating the request by the user.",
                                },
                                "issueDescription": {
                                    "type": "string",
                                    "description": "A description of the updated issue that the employee is facing.",
                                },
                            },
                            "required": [
                                "employeeId",
                                "issueDescription",
                                "justification",
                            ],
                        },
                    },
                    {
                        "name": "get_service_request",
                        "description": "Retrieves justification, description and approval status of the latest service request from ServiceNow.",
                    },
                    {
                        "name": "create_distribution_list",
                        "description": "Creates a distribution list in Microsoft 365.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "groupName": {
                                    "type": "string",
                                    "description": "Name of the distribution list to be created.",
                                },
                                "description": {
                                    "type": "string",
                                    "description": "Description of the distribution list to be created.",
                                },
                            },
                            "required": ["groupName", "description"],
                        },
                    },
                    {
                        "name": "add_users_to_distribution_list",
                        "description": "Adds users to a distribution list in Microsoft 365.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "groupName": {
                                    "type": "string",
                                    "description": "Name of the distribution list to which users are to be added.",
                                },
                                "userNames": {
                                    "type": "string",
                                    "description": "Username to be added to the distribution list.",
                                },
                            },
                            "required": ["groupName", "userNames"],
                        },
                    },
                    {
                        "name": "remove_users_from_distribution_list",
                        "description": "Removes users from a distribution list in Microsoft 365.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "groupName": {
                                    "type": "string",
                                    "description": "Name of the distribution list from which users are to be removed.",
                                },
                                "userNames": {
                                    "type": "string",
                                    "description": " Username to be removed from the distribution list.",
                                },
                            },
                            "required": ["groupName", "userNames"],
                        },
                    },
                    {
                        "name": "send_email_to_group",
                        "description": "Sends an email to a distribution list in Microsoft 365.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "groupName": {
                                    "type": "string",
                                    "description": "Name of the distribution list to which the email is to be sent.",
                                },
                                "subject": {
                                    "type": "string",
                                    "description": "Subject of the email to be sent.",
                                },
                                "content": {
                                    "type": "string",
                                    "description": "Content of the email to be sent.",
                                },
                            },
                            "required": ["groupName", "subject", "content"],
                        },
                    },
                    {
                        "name": "schedule_meeting",
                        "description": "Schedules a meeting in Microsoft 365.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "meetingSubject": {
                                    "type": "string",
                                    "description": "Subject of the meeting to be scheduled.",
                                },
                                "meetingStartTime": {
                                    "type": "string",
                                    "description": "The date and start time of the meeting to be scheduled in ISO format.",
                                },
                                "meetingEndTime": {
                                    "type": "string",
                                    "description": "The date and end time of the meeting to be scheduled in ISO format.",
                                },
                                "groupName": {
                                    "type": "string",
                                    "description": "Name of the distribution list for the meeting attendees.",
                                },
                                "content": {
                                    "type": "string",
                                    "description": "Content or agenda of the meeting to be scheduled.",
                                },
                            },
                            "required": [
                                "meetingSubject",
                                "meetingStartTime",
                                "meetingEndTime",
                                "groupName",
                                "content",
                            ],
                        },
                    },
                    {
                        "name": "get_slow_computer_troubleshooting",
                        "description": "Get the troubleshooting steps for a slow computer",
                    },
                    {
                        "name": "get_pos_printing_troubleshooting_steps",
                        "description": "Get the troubleshooting steps for POS printing",
                    },
                    {
                        "name": "get_self_checkout_troubleshooting_steps",
                        "description": "Get the troubleshooting steps for self-checkout kiosks",
                    },
                    {
                        "name": "get_microsoft_teams_login_loop_troubleshooting",
                        "description": "Get the troubleshooting steps for Microsoft Teams login loop",
                    },
                    {
                        "name": "get_onedrive_sluggish_performance_troubleshooting",
                        "description": "Get the troubleshooting steps for OneDrive sluggish performance",
                    },
                    {
                        "name": "handle_blue_screen_issue",
                        "description": "Get the troubleshooting steps for blue screen issue",
                    },
                    {
                        "name": "get_google_meet_connectivity_troubleshooting",
                        "description": "Get troubleshooting steps for Google Meet connectivity issues",
                    },
                    {
                        "name": "get_chromebook_performance_troubleshooting",
                        "description": "Get troubleshooting steps for Chromebook performance issues",
                    },
                    {
                        "name": "get_google_drive_syncing_troubleshooting",
                        "description": "Get troubleshooting steps for Google Drive syncing issues",
                    },
                    {
                        "name": "get_chromebook_printing_setup",
                        "description": "Get steps for setting up printing on Chromebooks",
                    },
                    {
                        "name": "get_google_groups_management_troubleshooting",
                        "description": "Get troubleshooting steps for Google Groups management issues",
                    },
                    {
                        "name": "get_concur_expense_login_troubleshooting",
                        "description": "Get troubleshooting steps for Concur expense login issues",
                    },
                    {
                        "name": "get_printer_setup_on_laptop",
                        "description": "Get troubleshooting steps for printer setup on a laptop",
                    },
                    {
                        "name": "get_distribution_list_management",
                        "description": "Get troubleshooting steps for distribution list management",
                    },
                    {
                        "name": "get_shared_drive_access_troubleshooting",
                        "description": "Get troubleshooting steps for shared drive access issues",
                    },
                    {
                        "name": "get_adobe_acrobat_signature_troubleshooting",
                        "description": "Get troubleshooting steps for Adobe Acrobat signature issues",
                    },
                    {
                        "name": "get_bitlocker_recovery_key_access",
                        "description": "Get troubleshooting steps for BitLocker recovery key access",
                    },
                    {
                        "name": "get_bsod_troubleshooting",
                        "description": "Get troubleshooting steps for Blue Screen of Death (BSOD) issues",
                    },
                    {
                        "name": "get_veeva_crm_ipad_installation",
                        "description": "Get troubleshooting steps for Veeva CRM iPad installation",
                    },
                    {
                        "name": "get_sap_gui_installation",
                        "description": "Get troubleshooting steps for SAP GUI installation",
                    },
                    {
                        "name": "reset_password",
                        "description": "Use to reset password of a software used by the employee",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "userName": {
                                    "type": "string",
                                    "description": "Username of the employee whose password is to be reset",
                                },
                                "otp": {
                                    "type": "string",
                                    "description": "OTP sent to the employee's phone number",
                                },
                                "employeeId": {
                                    "type": "string",
                                    "description": "ID of the employee to verify",
                                },
                            },
                            "required": ["userName", "otp", "employeeId"],
                        },
                    },
                ],
            },
            "voice": {
                "provider": "11labs",
                "voiceId": voice,
                "inputPreprocessingEnabled": True,
                "inputMinCharacters": 10,
            },
            "firstMessage": f"Hello, thanks for calling I-T Service desk. This is {voice}. How may I assist you today?",
            "serverUrl": os.getenv("VVA_SERVER_URL") + "/" + str(org_id),
            "recordingEnabled": True,
            "silenceTimeoutSeconds": 45,
            "responseDelaySeconds": 0.4,
            "llmRequestDelaySeconds": 0.4,
            "numWordsToInterruptAssistant": 3,
            "maxDurationSeconds": 1800,
            "backgroundSound": "off",
            "clientMessages": [
                "transcript",
                "hang",
                "tool-calls",
                "speech-update",
                "metadata",
                "conversation-update",
            ],
            "serverMessages": [
                "function-call",
                "end-of-call-report",
                "status-update",
                "hang",
                "conversation-update",
                "transcript",
            ],
            "endCallPhrases": ["goodbye"],
            "endCallMessage": "Thank you for contacting us. Have a great day!",
            "voicemailMessage": "You've reached our voicemail. Please leave a message after the beep, and we'll get back to you as soon as possible.",
            "forwardingPhoneNumber": voice_copilot_number.strip(),
            "transcriber": {
                "provider": "deepgram",
                "model": "nova-2",
                "smartFormat": True,
                "language": "en-US",
            },
        }

        agent_name = json.dumps(vva_config["name"])
        db_response = await self.create_virtual_assistant(
            org_id=org_id,
            assistant_json=vva_config,
            phone_number=phone_number,
            agent_type="Vapi",
            name=agent_name + " - " + phone_number,
        )
        log.debug(db_response)
        return db_response

    async def setup_open_source_voice_agent(
        self, org_id: str, area_code: str, prompt: str, agent_name: str, voice: str
    ):
        ## Procure phone number from twilio
        twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        twilio_client = Client(twilio_account_sid, twilio_auth_token)

        # Search for available phone numbers with the specified area code
        available_phone_numbers = twilio_client.available_phone_numbers(
            "US"
        ).local.list(area_code=area_code, limit=1)

        if not available_phone_numbers:
            raise Exception(
                f"No available phone numbers found with area code {area_code}."
            )

        # Procure a phone number from Twilio
        incoming_phone_number = twilio_client.incoming_phone_numbers.create(
            phone_number=available_phone_numbers[0].phone_number
        )
        log.debug(f"Phone number created: {incoming_phone_number.phone_number}")

        phone_number = incoming_phone_number.phone_number

        # get voice copilot number from db
        voice_copilot_number = await self.prisma.phone_number.find_first(
            where={"app_type": "voice_copilot", "org_id": org_id}
        )
        voice_copilot_number = voice_copilot_number.number
        log.debug(f"Voice Copilot Number: {voice_copilot_number}")

        base_url = os.getenv("OPEN_SOURCE_VOICE_AGENT_WEBHOOK_URL")

        function_webhook_url = f"{base_url}/{org_id}"
        voice_agent_webhook = f"{base_url}/{org_id}"

        # function_webhook_url = f"https://1d87-100-8-219-163.ngrok-free.app/open-source-voice-virtual-agent/{org_id}"  ## webhook for function call
        # voice_agent_webhook = f"https://1d87-100-8-219-163.ngrok-free.app/open-source-voice-virtual-agent/{org_id}"  ## webhook for transcript, end of call report, speech update, hang up, conversation update, metadata

        vva_config = {
            "agent_config": {
                "agent_name": f"{agent_name} - {phone_number}",
                "agent_welcome_message": f"Hello, thanks for calling I-T Service desk. This is {voice}. How may I assist you today?",
                "agent_type": "IT Service",
                "webhook_url": voice_agent_webhook,
                "tasks": [
                    {
                        "task_type": "conversation",
                        "tools_config": {
                            "llm_agent": {
                                "family": "openai",
                                "provider": "openai",
                                "model": "gpt-4o-mini",
                                "base_url": "https://api.openai.com/v1",
                                "max_tokens": 400,
                                "agent_flow_type": "streaming",
                                "use_fallback": True,
                                "temperature": 0.2,
                                "request_json": True,
                                "routes": None,
                            },
                            "synthesizer": {
                                "audio_format": "wav",
                                "provider": "deepgram",  ## AWS Polly
                                "stream": True,
                                "caching": True,
                                "provider_config": {
                                    "voice": voice,
                                    "model": f"aura-{voice.lower()}-en",
                                },
                                "buffer_size": 380,
                            },
                            "transcriber": {
                                "encoding": "linear16",
                                "sampling_rate": 16000,
                                "language": "en",
                                "provider": "deepgram",  ## whisper
                                "model": "nova-2",  ## small
                                "keywords": "",
                                "stream": True,
                                "endpointing": 2200,
                                "task": "transcribe",
                            },
                            "input": {"provider": "twilio", "format": "wav"},
                            "output": {"provider": "twilio", "format": "wav"},
                            "api_tools": {
                                "tools": [
                                    {
                                        "name": "verify_employee",
                                        "description": "Verify employee id and return employee details",
                                        "parameters": {
                                            "type": "object",
                                            "properties": {
                                                "employeeId": {
                                                    "type": "string",
                                                    "description": "ID of the employee to verify",
                                                }
                                            },
                                            "required": ["employeeId"],
                                        },
                                    },
                                    {
                                        "name": "create_service_request",
                                        "description": "Creates a request in service now and returns the service request number of the created request. Examples of service request can be 'user wanting to install a software'.",
                                        "parameters": {
                                            "type": "object",
                                            "properties": {
                                                "employeeId": {
                                                    "type": "string",
                                                    "description": "ID of the employee to verify",
                                                },
                                                "name": {
                                                    "type": "string",
                                                    "description": "name of the employee",
                                                },
                                                "justification": {
                                                    "type": "string",
                                                    "description": "Reason for creation of the request by the user.",
                                                },
                                                "issueDescription": {
                                                    "type": "string",
                                                    "description": "A description of the issue that the employee is facing.",
                                                },
                                            },
                                            "required": [
                                                "employeeId",
                                                "name",
                                                "issueDescription",
                                                "justification",
                                            ],
                                        },
                                    },
                                    {
                                        "name": "update_service_request",
                                        "description": "Updates a request in service now. Examples of service request can be 'user wanting to install a software'.",
                                        "parameters": {
                                            "type": "object",
                                            "properties": {
                                                "requestNumber": {
                                                    "type": "string",
                                                    "description": "Request number of service now request.",
                                                },
                                                "justification": {
                                                    "type": "string",
                                                    "description": "Reason for updating the request by the user.",
                                                },
                                                "issueDescription": {
                                                    "type": "string",
                                                    "description": "A description of the updated issue that the employee is facing.",
                                                },
                                            },
                                            "required": [
                                                "employeeId",
                                                "issueDescription",
                                                "justification",
                                            ],
                                        },
                                    },
                                    {
                                        "name": "get_service_request",
                                        "description": "Retrieves justification, description and approval status of the latest service request from ServiceNow.",
                                        "parameters": {
                                            "type": "object",
                                            "properties": {},
                                            "required": [],
                                        },
                                    },
                                    {
                                        "name": "create_distribution_list",
                                        "description": "Creates a distribution list in Microsoft 365.",
                                        "parameters": {
                                            "type": "object",
                                            "properties": {
                                                "groupName": {
                                                    "type": "string",
                                                    "description": "Name of the distribution list to be created.",
                                                },
                                                "description": {
                                                    "type": "string",
                                                    "description": "Description of the distribution list to be created.",
                                                },
                                            },
                                            "required": ["groupName", "description"],
                                        },
                                    },
                                    {
                                        "name": "add_users_to_distribution_list",
                                        "description": "Adds users to a distribution list in Microsoft 365.",
                                        "parameters": {
                                            "type": "object",
                                            "properties": {
                                                "groupName": {
                                                    "type": "string",
                                                    "description": "Name of the distribution list to which users are to be added.",
                                                },
                                                "userNames": {
                                                    "type": "string",
                                                    "description": "Username to be added to the distribution list.",
                                                },
                                            },
                                            "required": ["groupName", "userNames"],
                                        },
                                    },
                                    {
                                        "name": "remove_users_from_distribution_list",
                                        "description": "Removes users from a distribution list in Microsoft 365.",
                                        "parameters": {
                                            "type": "object",
                                            "properties": {
                                                "groupName": {
                                                    "type": "string",
                                                    "description": "Name of the distribution list from which users are to be removed.",
                                                },
                                                "userNames": {
                                                    "type": "string",
                                                    "description": " Username to be removed from the distribution list.",
                                                },
                                            },
                                            "required": ["groupName", "userNames"],
                                        },
                                    },
                                    {
                                        "name": "send_email_to_group",
                                        "description": "Sends an email to a distribution list in Microsoft 365.",
                                        "parameters": {
                                            "type": "object",
                                            "properties": {
                                                "groupName": {
                                                    "type": "string",
                                                    "description": "Name of the distribution list to which the email is to be sent.",
                                                },
                                                "subject": {
                                                    "type": "string",
                                                    "description": "Subject of the email to be sent.",
                                                },
                                                "content": {
                                                    "type": "string",
                                                    "description": "Content of the email to be sent.",
                                                },
                                            },
                                            "required": [
                                                "groupName",
                                                "subject",
                                                "content",
                                            ],
                                        },
                                    },
                                    {
                                        "name": "schedule_meeting",
                                        "description": "Schedules a meeting in Microsoft 365.",
                                        "parameters": {
                                            "type": "object",
                                            "properties": {
                                                "meetingSubject": {
                                                    "type": "string",
                                                    "description": "Subject of the meeting to be scheduled.",
                                                },
                                                "meetingStartTime": {
                                                    "type": "string",
                                                    "description": "The date and start time of the meeting to be scheduled in ISO format.",
                                                },
                                                "meetingEndTime": {
                                                    "type": "string",
                                                    "description": "The date and end time of the meeting to be scheduled in ISO format.",
                                                },
                                                "groupName": {
                                                    "type": "string",
                                                    "description": "Name of the distribution list for the meeting attendees.",
                                                },
                                                "content": {
                                                    "type": "string",
                                                    "description": "Content or agenda of the meeting to be scheduled.",
                                                },
                                            },
                                            "required": [
                                                "meetingSubject",
                                                "meetingStartTime",
                                                "meetingEndTime",
                                                "groupName",
                                                "content",
                                            ],
                                        },
                                    },
                                    {
                                        "name": "get_pos_printing_troubleshooting_steps",
                                        "description": "Get the troubleshooting steps for POS printing",
                                        "parameters": {
                                            "type": "object",
                                            "properties": {},
                                            "required": [],
                                        },
                                    },
                                    {
                                        "name": "get_self_checkout_troubleshooting_steps",
                                        "description": "Get the troubleshooting steps for self-checkout kiosks",
                                        "parameters": {
                                            "type": "object",
                                            "properties": {},
                                            "required": [],
                                        },
                                    },
                                    {
                                        "name": "get_microsoft_teams_login_loop_troubleshooting",
                                        "description": "Get the troubleshooting steps for Microsoft Teams login loop",
                                        "parameters": {
                                            "type": "object",
                                            "properties": {},
                                            "required": [],
                                        },
                                    },
                                    {
                                        "name": "get_onedrive_sluggish_performance_troubleshooting",
                                        "description": "Get the troubleshooting steps for OneDrive sluggish performance",
                                        "parameters": {
                                            "type": "object",
                                            "properties": {},
                                            "required": [],
                                        },
                                    },
                                    {
                                        "name": "handle_blue_screen_issue",
                                        "description": "Get the troubleshooting steps for blue screen issue",
                                        "parameters": {
                                            "type": "object",
                                            "properties": {},
                                            "required": [],
                                        },
                                    },
                                    {
                                        "name": "get_google_meet_connectivity_troubleshooting",
                                        "description": "Get troubleshooting steps for Google Meet connectivity issues",
                                        "parameters": {
                                            "type": "object",
                                            "properties": {},
                                            "required": [],
                                        },
                                    },
                                    {
                                        "name": "get_chromebook_performance_troubleshooting",
                                        "description": "Get troubleshooting steps for Chromebook performance issues",
                                        "parameters": {
                                            "type": "object",
                                            "properties": {},
                                            "required": [],
                                        },
                                    },
                                    {
                                        "name": "get_google_drive_syncing_troubleshooting",
                                        "description": "Get troubleshooting steps for Google Drive syncing issues",
                                        "parameters": {
                                            "type": "object",
                                            "properties": {},
                                            "required": [],
                                        },
                                    },
                                    {
                                        "name": "get_chromebook_printing_setup",
                                        "description": "Get steps for setting up printing on Chromebooks",
                                        "parameters": {
                                            "type": "object",
                                            "properties": {},
                                            "required": [],
                                        },
                                    },
                                    {
                                        "name": "get_google_groups_management_troubleshooting",
                                        "description": "Get troubleshooting steps for Google Groups management issues",
                                        "parameters": {
                                            "type": "object",
                                            "properties": {},
                                            "required": [],
                                        },
                                    },
                                    {
                                        "name": "get_concur_expense_login_troubleshooting",
                                        "description": "Get troubleshooting steps for Concur expense login issues",
                                        "parameters": {
                                            "type": "object",
                                            "properties": {},
                                            "required": [],
                                        },
                                    },
                                    {
                                        "name": "get_printer_setup_on_laptop",
                                        "description": "Get troubleshooting steps for printer setup on a laptop",
                                        "parameters": {
                                            "type": "object",
                                            "properties": {},
                                            "required": [],
                                        },
                                    },
                                    {
                                        "name": "get_distribution_list_management",
                                        "description": "Get troubleshooting steps for distribution list management",
                                        "parameters": {
                                            "type": "object",
                                            "properties": {},
                                            "required": [],
                                        },
                                    },
                                    {
                                        "name": "get_shared_drive_access_troubleshooting",
                                        "description": "Get troubleshooting steps for shared drive access issues",
                                        "parameters": {
                                            "type": "object",
                                            "properties": {},
                                            "required": [],
                                        },
                                    },
                                    {
                                        "name": "get_adobe_acrobat_signature_troubleshooting",
                                        "description": "Get troubleshooting steps for Adobe Acrobat signature issues",
                                        "parameters": {
                                            "type": "object",
                                            "properties": {},
                                            "required": [],
                                        },
                                    },
                                    {
                                        "name": "get_bitlocker_recovery_key_access",
                                        "description": "Get troubleshooting steps for BitLocker recovery key access",
                                        "parameters": {
                                            "type": "object",
                                            "properties": {},
                                            "required": [],
                                        },
                                    },
                                    {
                                        "name": "get_bsod_troubleshooting",
                                        "description": "Get troubleshooting steps for Blue Screen of Death (BSOD) issues",
                                        "parameters": {
                                            "type": "object",
                                            "properties": {},
                                            "required": [],
                                        },
                                    },
                                    {
                                        "name": "get_veeva_crm_ipad_installation",
                                        "description": "Get troubleshooting steps for Veeva CRM iPad installation",
                                        "parameters": {
                                            "type": "object",
                                            "properties": {},
                                            "required": [],
                                        },
                                    },
                                    {
                                        "name": "get_sap_gui_installation",
                                        "description": "Get troubleshooting steps for SAP GUI installation",
                                        "parameters": {
                                            "type": "object",
                                            "properties": {},
                                            "required": [],
                                        },
                                    },
                                    {
                                        "name": "reset_password",
                                        "description": "Use to reset password of a software used by the employee",
                                        "parameters": {
                                            "type": "object",
                                            "properties": {
                                                "userName": {
                                                    "type": "string",
                                                    "description": "Username of the employee whose password is to be reset",
                                                },
                                                "otp": {
                                                    "type": "string",
                                                    "description": "OTP sent to the employee's phone number",
                                                },
                                                "employeeId": {
                                                    "type": "string",
                                                    "description": "ID of the employee to verify",
                                                },
                                            },
                                            "required": [
                                                "userName",
                                                "otp",
                                                "employeeId",
                                            ],
                                        },
                                    },
                                ],
                                "tools_params": {
                                    "verify_employee": {
                                        "url": function_webhook_url,
                                        "method": "POST",
                                        "api_token": None,
                                        "param": '{"function_call":"verify_employee","employeeId":"%(employeeId)s"}',
                                    },
                                    "create_service_request": {
                                        "url": function_webhook_url,
                                        "method": "POST",
                                        "api_token": None,
                                        "param": '{"function_call":"create_service_request", "employeeId":"%(employeeId)s", "name":"%(name)s", "justification":"%(justification)s", "issueDescription":"%(issueDescription)s"}',
                                    },
                                    "update_service_request": {
                                        "url": function_webhook_url,
                                        "method": "POST",
                                        "api_token": None,
                                        "param": '{"function_call":"update_service_request", "requestNumber":"%(requestNumber)s", "justification":"%(justification)s", "issueDescription":"%(issueDescription)s"}',
                                    },
                                    "get_service_request": {
                                        "url": function_webhook_url,
                                        "method": "POST",
                                        "api_token": None,
                                        "param": '{"function_call":"get_service_request", "employeeId":"%(employeeId)s"}',
                                    },
                                    "create_distribution_list": {
                                        "url": function_webhook_url,
                                        "method": "POST",
                                        "api_token": None,
                                        "param": '{"function_call":"create_distribution_list", "groupName":"%(groupName)s", "description":"%(description)s"}',
                                    },
                                    "add_users_to_distribution_list": {
                                        "url": function_webhook_url,
                                        "method": "POST",
                                        "api_token": None,
                                        "param": '{"function_call":"add_users_to_distribution_list", "groupName":"%(groupName)s", "userNames":"%(userNames)s"}',
                                    },
                                    "remove_users_from_distribution_list": {
                                        "url": function_webhook_url,
                                        "method": "POST",
                                        "api_token": None,
                                        "param": '{"function_call":"remove_users_from_distribution_list", "groupName":"%(groupName)s", "userNames":"%(userNames)s"}',
                                    },
                                    "send_email_to_group": {
                                        "url": function_webhook_url,
                                        "method": "POST",
                                        "api_token": None,
                                        "param": '{"function_call":"send_email_to_group", "groupName":"%(groupName)s", "subject":"%(subject)s", "content":"%(content)s"}',
                                    },
                                    "schedule_meeting": {
                                        "url": function_webhook_url,
                                        "method": "POST",
                                        "api_token": None,
                                        "param": '{"function_call":"schedule_meeting", "meetingSubject":"%(meetingSubject)s", "meetingStartTime":"%(meetingStartTime)s", "meetingEndTime":"%(meetingEndTime)s", "groupName":"%(groupName)s", "content":"%(content)s"}',
                                    },
                                    "get_pos_printing_troubleshooting_steps": {
                                        "url": function_webhook_url,
                                        "method": "POST",
                                        "api_token": None,
                                        "param": '{"function_call":"get_pos_printing_troubleshooting_steps"}',
                                    },
                                    "get_self_checkout_troubleshooting_steps": {
                                        "url": function_webhook_url,
                                        "method": "POST",
                                        "api_token": None,
                                        "param": '{"function_call":"get_self_checkout_troubleshooting_steps"}',
                                    },
                                    "get_microsoft_teams_login_loop_troubleshooting": {
                                        "url": function_webhook_url,
                                        "method": "POST",
                                        "api_token": None,
                                        "param": '{"function_call":"get_microsoft_teams_login_loop_troubleshooting"}',
                                    },
                                    "get_onedrive_sluggish_performance_troubleshooting": {
                                        "url": function_webhook_url,
                                        "method": "POST",
                                        "api_token": None,
                                        "param": '{"function_call":"get_onedrive_sluggish_performance_troubleshooting"}',
                                    },
                                    "handle_blue_screen_issue": {
                                        "url": function_webhook_url,
                                        "method": "POST",
                                        "api_token": None,
                                        "param": '{"function_call":"handle_blue_screen_issue"}',
                                    },
                                    "get_google_meet_connectivity_troubleshooting": {
                                        "url": function_webhook_url,
                                        "method": "POST",
                                        "api_token": None,
                                        "param": '{"function_call":"get_google_meet_connectivity_troubleshooting"}',
                                    },
                                    "get_chromebook_performance_troubleshooting": {
                                        "url": function_webhook_url,
                                        "method": "POST",
                                        "api_token": None,
                                        "param": '{"function_call":"get_chromebook_performance_troubleshooting"}',
                                    },
                                    "get_google_drive_syncing_troubleshooting": {
                                        "url": function_webhook_url,
                                        "method": "POST",
                                        "api_token": None,
                                        "param": '{"function_call":"get_google_drive_syncing_troubleshooting"}',
                                    },
                                    "get_chromebook_printing_setup": {
                                        "url": function_webhook_url,
                                        "method": "POST",
                                        "api_token": None,
                                        "param": '{"function_call":"get_chromebook_printing_setup"}',
                                    },
                                    "get_google_groups_management_troubleshooting": {
                                        "url": function_webhook_url,
                                        "method": "POST",
                                        "api_token": None,
                                        "param": '{"function_call":"get_google_groups_management_troubleshooting"}',
                                    },
                                    "get_concur_expense_login_troubleshooting": {
                                        "url": function_webhook_url,
                                        "method": "POST",
                                        "api_token": None,
                                        "param": '{"function_call":"get_concur_expense_login_troubleshooting"}',
                                    },
                                    "get_printer_setup_on_laptop": {
                                        "url": function_webhook_url,
                                        "method": "POST",
                                        "api_token": None,
                                        "param": '{"function_call":"get_printer_setup_on_laptop"}',
                                    },
                                    "get_distribution_list_management": {
                                        "url": function_webhook_url,
                                        "method": "POST",
                                        "api_token": None,
                                        "param": '{"function_call":"get_distribution_list_management"}',
                                    },
                                    "get_shared_drive_access_troubleshooting": {
                                        "url": function_webhook_url,
                                        "method": "POST",
                                        "api_token": None,
                                        "param": '{"function_call":"get_shared_drive_access_troubleshooting"}',
                                    },
                                    "get_adobe_acrobat_signature_troubleshooting": {
                                        "url": function_webhook_url,
                                        "method": "POST",
                                        "api_token": None,
                                        "param": '{"function_call":"get_adobe_acrobat_signature_troubleshooting"}',
                                    },
                                    "get_bitlocker_recovery_key_access": {
                                        "url": function_webhook_url,
                                        "method": "POST",
                                        "api_token": None,
                                        "param": '{"function_call":"get_bitlocker_recovery_key_access"}',
                                    },
                                    "get_bsod_troubleshooting": {
                                        "url": function_webhook_url,
                                        "method": "POST",
                                        "api_token": None,
                                        "param": '{"function_call":"get_bsod_troubleshooting"}',
                                    },
                                    "get_veeva_crm_ipad_installation": {
                                        "url": function_webhook_url,
                                        "method": "POST",
                                        "api_token": None,
                                        "param": '{"function_call":"get_veeva_crm_ipad_installation"}',
                                    },
                                    "get_sap_gui_installation": {
                                        "url": function_webhook_url,
                                        "method": "POST",
                                        "api_token": None,
                                        "param": '{"function_call":"get_sap_gui_installation"}',
                                    },
                                    "reset_password": {
                                        "url": function_webhook_url,
                                        "method": "POST",
                                        "api_token": None,
                                        "param": '{"function_call":"reset_password", "userName":"%(userName)s", "otp":"%(otp)s", "employeeId":"%(employeeId)s"}',
                                    },
                                },
                            },
                        },
                        "toolchain": {
                            "execution": "parallel",
                            "pipelines": [["transcriber", "llm", "synthesizer"]],
                        },
                        "task_config": {
                            "number_of_words_for_interruption": 3,
                            "incremental_delay": 2000,
                            "hangup_after_LLMCall": False,
                            "call_transfer_number": voice_copilot_number.strip(),
                            "call_terminate": 1800,
                            "optimize_latency": True,
                            "ambient_noise": False,
                            "ambient_noise_track": None,
                            "hangup_after_silence": 300,
                            "backchanneling": False,
                            "call_cancellation_prompt": None,
                            "check_user_online_message": "Hey, are you still there?",
                            "trigger_user_online_message_after": 8,
                            "check_if_user_online": True,
                            "backchanneling_message_gap": 5,
                            "backchanneling_start_delay": 5,
                            "interruption_backoff_period": 100,
                            "use_fillers": False,
                        },
                    },
                    {
                        "tools_config": {
                            "llm_agent": {
                                "model": "gpt-3.5-turbo-1106",
                                "max_tokens": 350,
                                "agent_flow_type": "streaming",
                                "family": "openai",
                                "provider": "openai",
                                "temperature": 0.2,
                                "request_json": True,
                                "base_url": "https://api.openai.com/v1",
                            }
                        },
                        "task_type": "extraction",
                        "toolchain": {
                            "execution": "parallel",
                            "pipelines": [["llm"]],
                        },
                    },
                    {
                        "tools_config": {
                            "llm_agent": {
                                "model": "gpt-3.5-turbo-1106",
                                "max_tokens": 350,
                                "agent_flow_type": "streaming",
                                "family": "openai",
                                "provider": "openai",
                                "temperature": 0.2,
                                "request_json": True,
                                "base_url": "https://api.openai.com/v1",
                            }
                        },
                        "task_type": "summarization",
                        "toolchain": {
                            "execution": "parallel",
                            "pipelines": [["llm"]],
                        },
                    },
                    {
                        "tools_config": {
                            "output": None,
                            "input": None,
                            "synthesizer": None,
                            "llm_agent": None,
                            "transcriber": None,
                            "api_tools": {
                                "tools": "webhook",
                                "tools_params": {
                                    "webhook": {
                                        "method": "POST",
                                        "param": None,
                                        "url": voice_agent_webhook,
                                        "api_token": None,
                                    }
                                },
                            },
                        },
                        "task_type": "webhook",
                        "toolchain": {
                            "execution": "parallel",
                            "pipelines": [["requests"]],
                        },
                    },
                ],
            },
            "agent_prompts": {"task_1": {"system_prompt": prompt}},
        }

        bolna_url = "https://api.bolna.dev/agent"

        headers = {
            "Authorization": "Bearer bn-15f207fa02e04d83be437070270815e4",
            "Content-Type": "application/json",
        }

        ## Create VVA
        try:
            response = requests.post(
                bolna_url, json=vva_config, headers=headers
            )  ## Create VVA
            response.raise_for_status()
            log.debug(response.json())
        except requests.exceptions.RequestException as e:

            log.debug(f"An error occurred: {e}")
            if hasattr(e, "response") and e.response is not None:
                log.debug(f"Response content: {e.response.content}")

        vva_response = response.json()
        agent_id = vva_response.get("agent_id", "No Agent ID found")
        log.debug("Agent ID: ", agent_id)

        ## attach phone number to agent
        inbound_url = "https://api.bolna.dev/inbound/agent"
        inbound_payload = {
            "phone_number": phone_number,
            "agent_id": agent_id,
        }
        response = requests.request(
            "POST", inbound_url, json=inbound_payload, headers=headers
        )
        db_response = await self.create_virtual_assistant(
            org_id=org_id,
            assistant_json=vva_config,
            phone_number=phone_number,
            agent_id=agent_id,
            agent_type="Bolna",
            name=f"{agent_name} - {phone_number}",
        )
        log.debug(db_response)
        return db_response
