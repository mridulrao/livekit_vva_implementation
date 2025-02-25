import sys
from pathlib import Path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.extend([str(current_dir), str(parent_dir)])

from troubleshooting_functions import (
    get_pos_printing_troubleshooting_steps,
    get_sap_gui_installation,
    get_slow_computer_troubleshooting,
    get_self_checkout_troubleshooting_steps,
    handle_blue_screen_issue,
    get_google_meet_connectivity_troubleshooting,
    get_chromebook_performance_troubleshooting,
    get_google_drive_syncing_troubleshooting,
    get_chromebook_printing_setup,
    get_google_groups_management_troubleshooting,
    get_microsoft_teams_login_loop_troubleshooting,
    get_onedrive_sluggish_performance_troubleshooting,
    get_concur_expense_login_troubleshooting,
    get_okta_issues_troubleshooting_steps,
    get_printer_setup_on_laptop,
    get_distribution_list_management,
    get_shared_drive_access_troubleshooting,
    get_adobe_acrobat_signature_troubleshooting,
    get_bitlocker_recovery_key_access,
    get_bsod_troubleshooting,
    get_veeva_crm_ipad_installation,
)

import logging
logger = logging.getLogger(__name__)

# from servicenow_functions import (
#     create_ticket,
#     create_request,
#     get_request_by_number,
#     update_request_by_sys_id
# )

# from ms365_functions import (
#     create_empty_group,
#     add_users_to_group,
#     remove_users_from_group,
#     send_email_to_group,
#     schedule_meeting
# )

# from psuedo_servicenow import ServiceNow
# servicenow = ServiceNow()

# from psuedo_ms365group import MS365Group
# ms365group = MS365Group()


# function_map = {
#         'get_pos_printing_troubleshooting_steps': get_pos_printing_troubleshooting_steps,
#         'get_sap_gui_installation': get_sap_gui_installation,
#         'get_slow_computer_troubleshooting': get_slow_computer_troubleshooting,
#         'get_self_checkout_troubleshooting_steps': get_self_checkout_troubleshooting_steps,
#         'handle_blue_screen_issue': handle_blue_screen_issue,
#         'get_google_meet_connectivity_troubleshooting': get_google_meet_connectivity_troubleshooting,
#         'get_chromebook_performance_troubleshooting': get_chromebook_performance_troubleshooting,
#         'get_google_drive_syncing_troubleshooting': get_google_drive_syncing_troubleshooting,
#         'get_chromebook_printing_setup': get_chromebook_printing_setup,
#         'get_google_groups_management_troubleshooting': get_google_groups_management_troubleshooting,
#         'get_microsoft_teams_login_loop_troubleshooting': get_microsoft_teams_login_loop_troubleshooting,
#         'get_onedrive_sluggish_performance_troubleshooting': get_onedrive_sluggish_performance_troubleshooting,
#         'get_concur_expense_login_troubleshooting': get_concur_expense_login_troubleshooting,
#         'get_okta_issues_troubleshooting_steps': get_okta_issues_troubleshooting_steps,
#         'get_printer_setup_on_laptop': get_printer_setup_on_laptop,
#         'get_distribution_list_management': get_distribution_list_management,
#         'get_shared_drive_access_troubleshooting': get_shared_drive_access_troubleshooting,
#         'get_adobe_acrobat_signature_troubleshooting': get_adobe_acrobat_signature_troubleshooting,
#         'get_bitlocker_recovery_key_access': get_bitlocker_recovery_key_access,
#         'get_bsod_troubleshooting': get_bsod_troubleshooting,
#         'get_veeva_crm_ipad_installation': get_veeva_crm_ipad_installation,
#         'create_ticket': servicenow.create_ticket,
#         'create_service_request': servicenow.create_request,
#         'get_service_request': servicenow.get_request_by_number,
#         'update_service_request': servicenow.update_request_by_sys_id,
#         'create_distribution_list': ms365group.create_empty_group,
#         'add_user_to_distribution_list': ms365group.add_users_to_group,
#         'send_email_to_group': ms365group.send_email_to_group,
#         'schedule_meeting': ms365group.schedule_meeting,
#         'remove_users_from_distribution_list': ms365group.remove_users_from_group
#     }

#demo functions - 
# 'create_ticket': create_ticket,
# 'create_service_request': create_request,
# 'get_service_request': get_request_by_number,
# 'update_service_request': update_request_by_sys_id,

# 'create_distribution_list': create_empty_group,
# 'add_user_to_distribution_list': add_users_to_group,
# 'send_email_to_group': send_email_to_group,
# 'schedule_meeting': schedule_meeting,
# 'remove_users_from_distribution_list': remove_users_from_group


# async def function_handler(name, kwargs):
#     print(name, kwargs)
#     function = function_map.get(name)
    
#     if function is None:
#         return f"Error: Function '{name}' not found"
    
#     try:
#         if kwargs:
#             result = await function(**kwargs)
#         else:
#             result = await function()
#         return result
#     except Exception as e:
#         return f"Error executing function '{name}': {str(e)}"



class FunctionMapper:
    def __init__(self, servicenow=None, ms365group=None):
        self.servicenow = servicenow
        self.ms365group = ms365group
        self._init_function_map()

    def _init_function_map(self):
        self.function_map = {
            # Keep all troubleshooting functions as is
            'get_pos_printing_troubleshooting_steps': get_pos_printing_troubleshooting_steps,
            'get_sap_gui_installation': get_sap_gui_installation,
            'get_pos_printing_troubleshooting_steps': get_pos_printing_troubleshooting_steps,
            'get_sap_gui_installation': get_sap_gui_installation,
            'get_slow_computer_troubleshooting': get_slow_computer_troubleshooting,
            'get_self_checkout_troubleshooting_steps': get_self_checkout_troubleshooting_steps,
            'handle_blue_screen_issue': handle_blue_screen_issue,
            'get_google_meet_connectivity_troubleshooting': get_google_meet_connectivity_troubleshooting,
            'get_chromebook_performance_troubleshooting': get_chromebook_performance_troubleshooting,
            'get_google_drive_syncing_troubleshooting': get_google_drive_syncing_troubleshooting,
            'get_chromebook_printing_setup': get_chromebook_printing_setup,
            'get_google_groups_management_troubleshooting': get_google_groups_management_troubleshooting,
            'get_microsoft_teams_login_loop_troubleshooting': get_microsoft_teams_login_loop_troubleshooting,
            'get_onedrive_sluggish_performance_troubleshooting': get_onedrive_sluggish_performance_troubleshooting,
            'get_concur_expense_login_troubleshooting': get_concur_expense_login_troubleshooting,
            'get_okta_issues_troubleshooting_steps': get_okta_issues_troubleshooting_steps,
            'get_printer_setup_on_laptop': get_printer_setup_on_laptop,
            'get_distribution_list_management': get_distribution_list_management,
            'get_shared_drive_access_troubleshooting': get_shared_drive_access_troubleshooting,
            'get_adobe_acrobat_signature_troubleshooting': get_adobe_acrobat_signature_troubleshooting,
            'get_bitlocker_recovery_key_access': get_bitlocker_recovery_key_access,
            'get_bsod_troubleshooting': get_bsod_troubleshooting,
            'get_veeva_crm_ipad_installation': get_veeva_crm_ipad_installation,

            'create_ticket': self.servicenow.create_ticket if self.servicenow else None,
            'create_service_request': self.servicenow.create_request if self.servicenow else None,
            'get_service_request': self.servicenow.get_request_by_number if self.servicenow else None,
            'update_service_request': self.servicenow.update_request_by_sys_id if self.servicenow else None,
            'verify_employee': self.servicenow.verify_employee if self.servicenow else None,
            
            'create_distribution_list': self.ms365group.create_empty_group if self.ms365group else None,
            'add_user_to_distribution_list': self.ms365group.add_users_to_group if self.ms365group else None,
            'send_email_to_group': self.ms365group.send_email_to_group if self.ms365group else None,
            'schedule_meeting': self.ms365group.schedule_meeting if self.ms365group else None,
            'remove_users_from_distribution_list': self.ms365group.remove_users_from_group if self.ms365group else None
        }

    async def handle_function(self, name, kwargs):
        logger.debug(f"Handling function: {name} with args: {kwargs}")
        function = self.function_map.get(name)
        
        if function is None:
            logger.error(f"Function '{name}' not found or service not initialized")
            return f"Error: Function '{name}' not found or service not initialized"
        
        try:
            if kwargs:
                result = await function(**kwargs)
            else:
                result = await function()
            return result
        except Exception as e:
            logger.error(f"Error executing function '{name}': {str(e)}")
            return f"Error executing function '{name}': {str(e)}"
        
# Update the function_handler to use FunctionMapper
_function_mapper = None

def init_function_handler(servicenow=None, ms365group=None):
    global _function_mapper
    _function_mapper = FunctionMapper(servicenow, ms365group)

async def function_handler(name, kwargs):
    if _function_mapper is None:
        logger.error("Function handler not initialized")
        return "Error: Function handler not initialized"
    return await _function_mapper.handle_function(name, kwargs)