import json

async def create_ticket(**kwargs):
    print("Ticket Details:")
    print(f"Subject: {kwargs.get('subject', '')}")
    print(f"Description: {kwargs.get('description', '')}")
    print(f"Urgency: {kwargs.get('urgency', '')}")
    print(f"Impact: {kwargs.get('impact', '')}")
    print(f"Employee ID: {kwargs.get('employeeId', '')}")
    print(f"Name: {kwargs.get('name', '')}")
    print(f"Name: {kwargs.get('phone_number', '')}")

    incident_number = "INC678905"
    return {
        "Incident Number": incident_number,
        "Status": "Ticket Created"
    }

async def create_request(**kwargs):
    print("Service Request Details:")
    print(f"Employee Name: {kwargs.get('name', '')}")
    print(f"Employee ID: {kwargs.get('employeeId', '')}")
    print(f"Issue Description: {kwargs.get('issueDescription', '')}")
    print(f"Justification: {kwargs.get('justification', '')}")
    
    request_number = "REQ0001234"
    return {
        "Request_Number": request_number,
        "ManagersApproval": "Pending",
        "Notification sent to Manager": "Yes",
    }

async def get_request_by_number(**kwargs):
    print("Retrieving Service Request Details:")
    print(f"Caller Phone Number: <caller number to be placed>")
    
    return {
        "short_description": "Sample service request description",
        "approval_status": "Pending",
        "justification": "Sample justification for the request",
    }

async def update_request_by_sys_id(**kwargs):
    print("Updating Service Request:")
    print(f"Request Number: {kwargs.get('requestNumber', '')}")
    print(f"Issue Description: {kwargs.get('issueDescription', '')}")
    print(f"Justification: {kwargs.get('justification', '')}")
    
    return {
        "result": json.dumps({
            "status": "success",
            "message": "Request updated successfully"
        })
    }



