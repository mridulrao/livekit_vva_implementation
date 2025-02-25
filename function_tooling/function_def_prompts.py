functions = [
                {
                    "name": "get_slow_computer_troubleshooting",
                    "description": "ALWAYS USE THIS FUNCTION when users mention: slow computer, performance issues, lag, or system slowdown. This is the primary and preferred function for ANY computer speed or performance problems. Example triggers: 'computer is slow', 'system is lagging', 'performance issues'."
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

                ### ServiceNow function
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
                    }
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


                ### MS365 Group functions 
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
                }
            ]

