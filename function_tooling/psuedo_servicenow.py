from abc import ABCMeta, abstractmethod
import requests
from requests.auth import HTTPBasicAuth
from typing import Dict, Any
import json

from dotenv import load_dotenv
load_dotenv()

SUCCESS = {"code": 200, "message": "The request was successful"}
# from errors.error_config import ERRORS, SUCCESS
ERRORS = {
    "NOT_FOUND": {"code": 404, "message": "The requested resource was not found"},
    "UNAUTHORIZED": {
        "code": 401,
        "message": "You are not authorized to access this resource",
    },
    "INTERNAL_SERVER_ERROR": {"code": 500, "message": "Internal server error occurred"},
    "EMPTY_DATA": {"code": 422, "message": "The provided data is empty or invalid"},
}

INSTANCE_NAME = "dev209832"
USERNAME = "mridul@futurepath.dev"
PASSWORD = "Best@123"


class ServiceNowBase(metaclass=ABCMeta):
    """
    Abstract base class for interacting with ServiceNow instances.
    This class defines the interface for common ServiceNow operations,
    such as retrieving users, incidents, and creating or updating requests and incidents.
    """

    @abstractmethod
    async def create_ticket(self, **kwargs):
        """
        Creates a new incident with the specified details.

        Params:
            subject (str): A brief description of the incident.
            description (str): A detailed description of the incident.
            urgency (int): The urgency of the incident.
            impact (int): The impact of the incident.
            user_id (str): The ID of the user creating the incident.
            assignee (str, optional): The ID of the user to whom the incident is assigned.

        Returns:
            dict: The result of the incident creation operation.
        """
        pass


    @abstractmethod
    async def create_request(self, **kwargs):
        """
        Creates a service request with the specified details.

        Params:
            short_description (str): A brief description of the service request.
            description (str): Detailed description of the service request.
            caller_id (str): The identifier of the person making the request.
            requested_for (str): The identifier of the person for whom the request is being made.
            approval (str, optional): Approval status. Defaults to 'not requested'.
            priority (int, optional): Priority of the request. Defaults to 3.
            special_instructions (str, optional): Any special instructions related to the service request.

        Returns:
            dict: The result of the service request creation operation.
        """
        pass



'''
In **kwargs we will always have phone_number, it is passed when function_tool is executed. 
None is the default value for dict.get() when no second argument is provided
    - If we dont get any param in input, it would be initialized by None 
'''

class ServiceNow(ServiceNowBase):
    def __init__(self, auth=None):
        """Initializes the ServiceNow instance with authentication and headers."""
        if auth:
            self.username = auth.username
            self.password = auth.password
            self.instance_name = auth.instance_name
        else:
            self.username = USERNAME
            self.password = PASSWORD
            self.instance_name = INSTANCE_NAME
        print(
            f"Initializing ServiceNow with username: {self.username}, instance_name: {self.instance_name} , password: {self.password}"
        )
        self.auth = HTTPBasicAuth(self.username, self.password)
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        self.base_url = f"https://{self.instance_name}.service-now.com/api/now/table/"

    def _make_request(self, method, url, data=None):
        try:
            if method == "GET":
                response = requests.get(url, headers=self.headers, auth=self.auth)
            elif method == "POST":
                response = requests.post(
                    url, json=data, headers=self.headers, auth=self.auth
                )
            elif method == "PUT":
                response = requests.put(
                    url, json=data, headers=self.headers, auth=self.auth
                )
            elif method == "PATCH":
                response = requests.patch(
                    url, json=data, headers=self.headers, auth=self.auth
                )
            else:
                return ERRORS["INTERNAL_SERVER_ERROR"]

            if response.status_code in [200, 201]:
                result = response.json().get("result")
                if not result:
                    return {
                        **ERRORS["EMPTY_DATA"],
                        "details": "No data returned by ServiceNow",
                    }
                return {**SUCCESS, "data": result}
            elif response.status_code == 404:
                return ERRORS["NOT_FOUND"]
            elif response.status_code == 401:
                return ERRORS["UNAUTHORIZED"]
            else:
                return {**ERRORS["INTERNAL_SERVER_ERROR"], "details": response.text}
            
        except requests.exceptions.RequestException as error:
            return {**ERRORS["INTERNAL_SERVER_ERROR"], "details": str(error)}
        
    async def get_user_sys_id_by_employee_number(self, employee_number):
        url = f"{self.base_url}sys_user?sysparm_query=employee_number={employee_number}&sysparm_fields=sys_id"
        response = self._make_request("GET", url)
        if response.get("code") == 200 and response.get("data"):
            return response["data"][0]["sys_id"]
        
        return None

    async def create_ticket(self, **kwargs):
        employee_number = kwargs.get('employeeId')
        subject = kwargs.get('subject')
        description = kwargs.get('description')
        urgency = kwargs.get('urgency')
        impact = kwargs.get('impact')
        state = kwargs.get('state')
        assignee = kwargs.get('assignee')
        emp_sys_id = kwargs.get('emp_sys_id')
        name = kwargs.get('name')  # passed in JSON function definition but not used here
        
        if employee_number:
            user_sys_id = await self.get_user_sys_id_by_employee_number(employee_number)
        else:
            user_sys_id = emp_sys_id

        if user_sys_id:
            url = f"{self.base_url}incident"
            data = {
                "short_description": subject,
                "description": description,
                "urgency": urgency,
                "impact": impact,
                "caller_id": user_sys_id,
            }
            if assignee:
                data["assigned_to"] = assignee
            if state:
                data["state"] = state
            response = self._make_request("POST", url, data)
            incident_number = response.get("data", {}).get("number")
            return {"Incident Number": incident_number, "Status": "Ticket Created"}
        
        return ERRORS["NOT_FOUND"]

    
    async def create_request(self, **kwargs):
        name = kwargs.get('name')  # not used but passed in JSON
        employee_number = kwargs.get('employeeId')
        description = kwargs.get('issueDescription')
        justification = kwargs.get('justification')
        
        if employee_number:
            caller_sys_id = await self.get_user_sys_id_by_employee_number(employee_number)
            if not caller_sys_id:
                return ERRORS["NOT_FOUND"]
            
            url = f"{self.base_url}sc_request"
            data = {
                "short_description": justification,
                "description": description,
                "caller_id": caller_sys_id,
                "requested_for": caller_sys_id,
            }
            
            response = self._make_request("POST", url, data)
            if response.get("code") == 200:
                request_number = response.get("data", {}).get("number", "")
                return {
                    "Request_Number": request_number,
                    "ManagersApproval": "Pending",
                    "Notification sent to Manager": "Yes",
                }
        
        return ERRORS["NOT_FOUND"]

    
    async def get_request_by_number(self, **kwargs):
        request_number = kwargs.get('requestNumber', '')
        url = f"{self.base_url}sc_request?number={request_number}"
        
        response = self._make_request("GET", url)
        
        if response["code"] == 200 and response.get("data"):
            request_data = response["data"][0]
            return {
                "short_description": request_data.get("short_description", ""),
                "approval_status": request_data.get("approval", "Pending"),
                "justification": request_data.get("description", ""),
            }
        
        return ERRORS["NOT_FOUND"]
        
    async def update_request_by_sys_id(self, **kwargs):
        request_number = kwargs.get('requestNumber', '')
        description = kwargs.get('issueDescription', '')
        justification = kwargs.get('justification', '')
        
        request = await self.get_request_by_number({"requestNumber": request_number})
        
        if isinstance(request, dict) and "error" in request:
            return request
        
        url = f"{self.base_url}sc_request/{request['sys_id']}"
        update_data = {
            "short_description": justification,
            "description": description,
        }
        
        response = self._make_request("PUT", url, update_data)
        return {
            "result": json.dumps({
                "status": "success" if response["code"] == 200 else "error",
                "message": "Request updated successfully" if response["code"] == 200 else "Failed to update request"
            })
        }
    
    async def verify_employee(self, **kwargs):
        employee_details = [
            {
                "employee_id": "9080",
                "name": "Mridul Rao",
                "username": "mridul.rao",
            }
        ]
        employee_id = str(kwargs.get('employeeId', ''))
        for employee in employee_details:
            if employee["employee_id"] == employee_id:
                print("Verification Successful")
                return {"status": "success", "employee_details": employee}
            
        print("Verification Failed")
        return {"status": "error", "message": "Employee not found"}
        



# async def main():
#     import asyncio
#     snow = ServiceNow()
    
#     # Test case 1: Create Ticket
#     ticket_kwargs = {
#         'employeeId': '9080',
#         'subject': 'Test Incident',
#         'description': 'This is a test incident creation',
#         'urgency': 2,
#         'impact': 2,
#         'state': 1,
#         'name': 'John Doe',
#     }
    
#     print("\nCreating ticket...")
#     result = await snow.create_ticket(**ticket_kwargs)
#     print(f"Ticket creation result: {result}")
    
#     # Test case 2: Create Request
#     request_kwargs = {
#         'employeeId': '9080', 
#         'name': 'John Doe',
#         'issueDescription': 'Need access to development environment',
#         'justification': 'Required for new project development'
#     }
    
#     print("\nCreating request...")
#     result = await snow.create_request(**request_kwargs)
#     print(f"Request creation result: {result}")
    
#     # Test case 3: Get Request Details
#     get_request_kwargs = {
#         'requestNumber': '' 
#     }
    
#     print("\nGetting request details...")
#     result = await snow.get_request_by_number(**get_request_kwargs)
#     print(f"Request details: {result}")
    
#     # Test case 4: Update Request
#     update_request_kwargs = {
#         'requestNumber': '',  
#         'issueDescription': 'Updated description for development environment access',
#         'justification': 'Urgent access needed for project deadline'
#     }
    
#     print("\nUpdating request...")
#     result = await snow.update_request_by_sys_id(**update_request_kwargs)
#     print(f"Update result: {result}")

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main())
    