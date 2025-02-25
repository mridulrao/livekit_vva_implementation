troubleshooting_functions - Contains all the functions which do not require any manipulations. 

psuedo_servicenow - Contains all the functions which rely on service now 
Currently hard-coded credentials of Mridul 

psuedo_ms365group - Contains all the functions which rely on ms365 

function_tool_vva - It passes the functions available to the Livekit agent - S2S/TTS agent and send an execute command to run the function
**kwargs 
Function params are passed using **kwargs, agent ask for user inputs. 
PhoneNumber is a default **kwargs - always present even if no param is used by function(troubleshooting functions)

function_handelling - It is used by function_tool_vva to get the result of the function called 

function_def_prompt - Contains all the JSON definition of the functions which is passed in Livekit agent - S2S/TTS agnets

service_instances - It ensures that servicenow and MS365 instances are initialized only once, its connected with prewarm function 
of the agents which ensures that one agent is initialized, prewarm function is called before and executed

instructions.py - Contains instructions/prompt-gaurdrails for the agents


Agents - 
Agents only requires to file access -
1) function_tool_vva - to define and run the functions
2) function_def_prompt - JSON functions definitions 

Note - Before initializing the Functions, we pass phone number in **kwargs


All the function_name are exactly the same passed in prompt and called in backend, except few
Service Now - 
'create_ticket': create_ticket,
'create_service_request': create_request,
'get_service_request': get_request_by_number,
'update_service_request': update_request_by_sys_id,

MS365 Group - 
'create_distribution_list': create_empty_group,
'add_user_to_distribution_list': add_users_to_group,
'send_email_to_group': send_email_to_group,
'schedule_meeting': schedule_meeting,
'remove_users_from_distribution_list': remove_users_from_group


