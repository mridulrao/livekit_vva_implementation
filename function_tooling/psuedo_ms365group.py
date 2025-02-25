import requests
import msal
import os
from datetime import datetime
import json

from dotenv import load_dotenv
load_dotenv()



ERRORS = {
    "NOT_FOUND": {"code": 404, "message": "The requested resource was not found"},
    "UNAUTHORIZED": {
        "code": 401,
        "message": "You are not authorized to access this resource",
    },
    "INTERNAL_SERVER_ERROR": {"code": 500, "message": "Internal server error occurred"},
    "EMPTY_DATA": {"code": 422, "message": "The provided data is empty or invalid"},
    "BAD_REQUEST": {"code": 400, "message": "Bad request"},
}

SUCCESS = {"code": 200, "message": "The request was successful"}

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET_DL")
AUTHORITY = os.getenv("AUTHORITY")
TENANT_ID = os.getenv("TENANT_ID")
USER_EMAIL = os.getenv("USER_EMAIL")
EMAIL_CLIENT_ID = os.getenv("EMAIL_CLIENT_ID")
EMAIL_CLIENT_SECRET = os.getenv("EMAIL_CLIENT_SECRET")
EMAIL_TENANT_ID = os.getenv("EMAIL_TENANT_ID")


class MS365Group:
    def __init__(self):
        self.client_id = EMAIL_CLIENT_ID
        self.client_secret = EMAIL_CLIENT_SECRET
        self.authority = f"{AUTHORITY}/{EMAIL_TENANT_ID}"
        self.scope = ["https://graph.microsoft.com/.default"]
        print(
            f"Initializing MS365!"
        )
        self.client = msal.ConfidentialClientApplication(
            self.client_id,
            authority=self.authority,
            client_credential=self.client_secret,
        )
        self.access_token = self._get_access_token()

    def _get_access_token(self):
        token_result = self.client.acquire_token_silent(self.scope, account=None)
        if not token_result:
            token_result = self.client.acquire_token_for_client(scopes=self.scope)
        if "access_token" in token_result:
            return token_result["access_token"]
        raise Exception("Failed to acquire access token")

    def _make_request(self, url, method="GET", data=None):
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        try:
            response = requests.request(method, url, headers=headers, json=data)
            response.raise_for_status()
            if response.status_code == 204:  # No Content
                return SUCCESS
            if not response.text:
                return SUCCESS
            return {**SUCCESS, "data": response.json()}
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                return ERRORS["NOT_FOUND"]
            elif e.response.status_code == 401:
                return ERRORS["UNAUTHORIZED"]
            elif e.response.status_code == 400:
                return {**ERRORS["BAD_REQUEST"], "details": e.response.text}
            else:
                return {**ERRORS["INTERNAL_SERVER_ERROR"], "details": str(e)}
        except requests.RequestException as e:
            return {**ERRORS["INTERNAL_SERVER_ERROR"], "details": str(e)}
        
    def _get_group_by_name(self, group_name):
        url = f"https://graph.microsoft.com/v1.0/groups?$filter=displayName eq '{group_name}'"
        result = self._make_request(url)
        if (
            result["code"] == 200
            and "data" in result
            and "value" in result["data"]
            and result["data"]["value"]
        ):
            return {"code": 200, "data": result["data"]["value"][0]}
        return ERRORS["NOT_FOUND"]
    
    def _get_user_by_email(self, email):
        url = f"https://graph.microsoft.com/v1.0/users/{email}"
        result = self._make_request(url)
        if result["code"] == 200 and "data" in result:
            return result["data"]["id"]
        return None
        
    async def create_empty_group(self, **kwargs):
        group_name = kwargs.get('groupName')
        description = kwargs.get('description')
        
        url = "https://graph.microsoft.com/v1.0/groups"
        data = {
            "displayName": group_name,
            "mailEnabled": True,
            "mailNickname": group_name.replace(" ", "").lower(),
            "securityEnabled": False,
            "groupTypes": ["Unified"],
            "description": description,
        }

        result = self._make_request(url, method="POST", data=data)
        if result["code"] == 200 and "data" in result:
            print(f"Successfully created group: {group_name}")
            return {"result": json.dumps({
                "status": "success",
                "message": "Distribution list created successfully",
                "group_id": result["data"].get("id")
            })}
        print(f"Failed to create group: {group_name}")
        return {"result": json.dumps({
            "status": "error",
            "message": "Failed to create distribution list"
        })}
    
    async def add_users_to_group(self, **kwargs):
        group_name = kwargs.get('groupName')
        user_names = kwargs.get('userNames')
        user_emails = kwargs.get('userEmails')

        group = self._get_group_by_name(group_name)

        if not group or "data" not in group:
            return {**ERRORS["NOT_FOUND"], "details": f"Group not found: {group_name}"}

        if user_names and not isinstance(user_names, list):
            user_names = [user_names]
        if user_emails and not isinstance(user_emails, list):
            user_emails = [user_emails]

        if user_names and not user_emails:
            user_emails = [f"{name}@futurepath.dev" for name in user_names]
        elif not user_emails:
            return {**ERRORS["BAD_REQUEST"], "details": "No users provided"}

        members_url = (
            f"https://graph.microsoft.com/v1.0/groups/{group['data']['id']}/members"
        )
        members_result = self._make_request(members_url)

        if members_result["code"] != 200:
            return {
                "code": 400,
                "message": "Failed to fetch current group members",
                "data": {"failed": user_emails},
            }

        existing_members = [
            member["id"] for member in members_result["data"].get("value", [])
        ]

        success_emails = []
        existing_emails = []
        failed_emails = []

        for user_email in user_emails:
            user_id = self._get_user_by_email(user_email)
            if not user_id:
                failed_emails.append(user_email)
                continue

            if user_id in existing_members:
                existing_emails.append(user_email)
                continue

            url = f"https://graph.microsoft.com/v1.0/groups/{group['data']['id']}/members/$ref"
            data = {
                "@odata.id": f"https://graph.microsoft.com/v1.0/directoryObjects/{user_id}"
            }
            result = self._make_request(url, method="POST", data=data)

            if result["code"] == 200:
                success_emails.append(user_email)
            else:
                failed_emails.append(user_email)

        return {"result": json.dumps({
            "status": "success" if len(failed_emails) == 0 else "error",
            "message": "Completed adding users to group",
            "added_users": success_emails,
            "existing_users": existing_emails,
            "failed_users": failed_emails
        })}
    
    async def send_email_to_group(self, **kwargs):
        group_name = kwargs.get('groupName')
        subject = kwargs.get('subject')
        content = kwargs.get('content')

        group = self._get_group_by_name(group_name)

        if not group or "data" not in group:
            return {"code": 404, "message": f"Group not found: {group_name}"}

        group_mail = group["data"]["mail"]
        if not group_mail:
            print(f"Group email not found for: {group_name}")
            return {"code": 404, "message": f"Group email not found for: {group_name}"}

        url = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/sendMail"
        data = {
            "message": {
                "subject": f"Re:{subject}",
                "body": {"contentType": "HTML", "content": content},
                "toRecipients": [{"emailAddress": {"address": group_mail}}],
                "from": {"emailAddress": {"address": USER_EMAIL}},
            },
            "saveToSentItems": "true",
        }

        print(f"Sending email to {group_mail} with subject:")
        result = self._make_request(url, method="POST", data=data)

        if result["code"] == 200:
            return {"result": json.dumps({
                "status": "success",
                "message": "Successfully sent the email to the group",
                "group_name": group_name
            })}
        
        return {"result": json.dumps({
            "status": "error",
            "message": "Failed to send the email to the group",
            "group_name": group_name
        })}
        
    async def schedule_meeting(self, **kwargs):
        subject = kwargs.get('meetingSubject')
        start_time = kwargs.get('meetingStartTime')
        end_time = kwargs.get('meetingEndTime')
        group_name = kwargs.get('groupName')
        content = kwargs.get('content')

        if isinstance(start_time, str):
            start_time = datetime.fromisoformat(start_time)
        if isinstance(end_time, str):
            end_time = datetime.fromisoformat(end_time)

        group = self._get_group_by_name(group_name)
        if not group or "data" not in group:
            return {"code": 404, "message": f"Group not found: {group_name}"}

        group_mail = group["data"]["mail"]
        if not group_mail:
            print(f"Group email not found for: {group_name}")
            return {"code": 404, "message": f"Group email not found for: {group_name}"}

        url = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/events"

        data = {
            "subject": subject,
            "body": {"contentType": "HTML", "content": content},
            "start": {"dateTime": start_time.isoformat(), "timeZone": "PST"},
            "end": {"dateTime": end_time.isoformat(), "timeZone": "PST"},
            "attendees": [
                {
                    "emailAddress": {
                        "address": group_mail,
                        "name": group_name,  # Optional, for display purposes
                    },
                    "type": "required",  # Can also be "optional"
                }
            ],
            "location": {"displayName": "Online Meeting"},
            "isOnlineMeeting": True,
            "onlineMeetingProvider": "teamsForBusiness",
        }

        print(f"Sending invite to {group_mail}")
        result = self._make_request(url, method="POST", data=data)
        if result["code"] == 200:
            return {"result": json.dumps({
                "status": "success",
                "message": "Successfully scheduled meeting",
                "meeting_details": result.get("data", {})
            })}
        
        return {"result": json.dumps({
            "status": "error",
            "message": "Failed to schedule meeting"
        })}
        
    async def remove_users_from_group(self, **kwargs):
        group_name = kwargs.get('groupName')
        user_names = kwargs.get('userNames')
        user_emails = kwargs.get('userEmails')

        group = self._get_group_by_name(group_name)
        if not group or "data" not in group:
            return {"code": 404, "message": f"Group not found: {group_name}"}

        # Convert single values to lists for consistent handling
        if user_names and not isinstance(user_names, list):
            user_names = [user_names]
        if user_emails and not isinstance(user_emails, list):
            user_emails = [user_emails]

        # Generate emails from usernames if needed
        if not user_emails and user_names:
            user_emails = [f"{name}@futurepath.dev" for name in user_names]
        elif not user_emails:
            return {"code": 400, "message": "No users specified for removal"}

        success_emails = []
        failed_emails = []

        for email in user_emails:
            user_id = self._get_user_by_email(email)
            if not user_id:
                failed_emails.append(email)
                continue

            url = f"https://graph.microsoft.com/v1.0/groups/{group['data']['id']}/members/{user_id}/$ref"
            result = self._make_request(url, method="DELETE")

            if result["code"] == 200:
                success_emails.append(email)
            else:
                failed_emails.append(email)

        # Prepare response message based on results
        message_parts = []
        if success_emails:
            message_parts.append("Some users were successfully removed")
        if failed_emails:
            message_parts.append("Some users failed to be removed")

        return {"result": json.dumps({
            "status": "success" if success_emails else "error",
            "message": " and ".join(message_parts) or "No users were processed",
            "removed_users": success_emails,
            "failed_users": failed_emails
        })}
        



# async def main():
#     import asyncio
#     from datetime import datetime, timedelta

#     ms365 = MS365Group()

#     # Test 1: Create Empty Group
#     print("\n=== Testing Create Empty Group ===")
#     create_group_kwargs = {
#         'groupName': 'Test Development Team',
#         'description': 'A test group for development team members'
#     }
#     result = await ms365.create_empty_group(**create_group_kwargs)
#     print(f"Create Group Result: {result}")

#     # Test 2: Add Users to Group
#     print("\n=== Testing Add Users to Group ===")
#     add_users_kwargs = {
#         'groupName': 'Test Development Team',
#         'userNames': ['john.doe', 'jane.smith', 'bob.wilson'],
#         'userEmails': ['john.doe@futurepath.dev', 'jane.smith@futurepath.dev', 'bob.wilson@futurepath.dev']
#     }
#     result = await ms365.add_users_to_group(**add_users_kwargs)
#     print(f"Add Users Result: {result}")

#     # Test 3: Send Email to Group
#     print("\n=== Testing Send Email to Group ===")
#     send_email_kwargs = {
#         'groupName': 'Test Development Team',
#         'subject': 'Test Group Email',
#         'content': '<p>This is a test email sent to the group.</p><p>Please ignore this message.</p>'
#     }
#     result = await ms365.send_email_to_group(**send_email_kwargs)
#     print(f"Send Email Result: {result}")

#     # Test 4: Schedule Meeting
#     print("\n=== Testing Schedule Meeting ===")
#     tomorrow = datetime.now() + timedelta(days=1)
#     start_time = tomorrow.replace(hour=10, minute=0, second=0, microsecond=0)
#     end_time = start_time + timedelta(hours=1)

#     schedule_meeting_kwargs = {
#         'meetingSubject': 'Development Team Sync',
#         'meetingStartTime': start_time.isoformat(),
#         'meetingEndTime': end_time.isoformat(),
#         'groupName': 'Test Development Team',
#         'content': 'Weekly development team sync meeting to discuss project progress.'
#     }
#     result = await ms365.schedule_meeting(**schedule_meeting_kwargs)
#     print(f"Schedule Meeting Result: {result}")

#     # Test 5: Remove Users from Group
#     print("\n=== Testing Remove Users from Group ===")
#     remove_users_kwargs = {
#         'groupName': 'Test Development Team',
#         'userNames': ['bob.wilson'],
#         'userEmails': ['bob.wilson@futurepath.dev']
#     }
#     result = await ms365.remove_users_from_group(**remove_users_kwargs)
#     print(f"Remove Users Result: {result}")

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main())

