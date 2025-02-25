async def get_pos_printing_troubleshooting_steps(**kwargs):
    steps = (
        "Basic Checks",
        "Ensure the printer is turned on.",
        "Check that the printer is properly connected to the POS system.",
        "Verify that there is enough paper in the printer.",
        "Ensure the paper roll is correctly installed.",
        "Check the printer for any error messages or blinking lights.",
        "Printer Status",
        "Open the printer and inspect for any paper jams. Remove any stuck paper.",
        "Ensure the printer door is securely closed.",
        "Check the ink or toner levels. If they are low, replace the cartridge.",
        "Advanced Troubleshooting",
        "Restart both the printer and the POS system.",
        "On the POS system, navigate to the printer settings.",
        "Verify that the correct printer is selected as the default printer.",
        "Disconnect the printer from the POS system and reconnect it.",
        "Driver Update",
        "Go to the POS system's settings or control panel.",
        "Navigate to the 'Devices' or 'Printers' section and locate your printer.",
        "Look for an option to update or reinstall the printer drivers.",
        "If not available, visit the printer manufacturer's website to download the latest drivers and follow their installation instructions.",
        "Test Print",
        "Print a test receipt to ensure the printer is working correctly.",
    )

    additional_support = (
        "Additional Support:",
        "Refer to the printer's user manual for specific troubleshooting steps.",
        "Contact your POS system provider for further assistance.",
        "Seek help from a professional technician if the problem persists.",
    )

    return {"troubleshooting_steps": steps, "additional_support": additional_support}


async def get_self_checkout_troubleshooting_steps(**kwargs):
    steps = (
        "Initial Assessment",
        "Check for Power Issues:",
        "Ensure the kiosk is properly plugged in.",
        "Verify that the power outlet is functional by plugging in another device.",
        "Look for any visible damage to power cables or connections.",
        "Restart the Kiosk:",
        "Perform a soft reset by turning the kiosk off and then on again.",
        "If a soft reset does not work, perform a hard reset (if applicable).",
        "Software and System Checks",
        "Check for Error Messages:",
        "Note any error messages displayed on the screen.",
        "Refer to the kiosk's manual or support documentation for error code explanations.",
        "Update Software:",
        "Ensure the kiosk software is up to date.",
        "Check for pending software updates and install them if necessary.",
        "Run Diagnostic Tools:",
        "Access the kiosk's built-in diagnostic tools (if available) and run a full system check.",
        "Note any issues detected by the diagnostic tools.",
        "Network and Connectivity",
        "Verify Network Connection:",
        "Ensure the kiosk is connected to the network (Wi-Fi or Ethernet).",
        "Check network cables for any signs of damage.",
        "Test Network Connectivity:",
        "Use a network diagnostic tool to test connectivity to the main server.",
        "Ensure the kiosk can communicate with the central system.",
        "Hardware Inspection",
        "Check Peripheral Devices:",
        "Inspect attached peripherals (e.g., barcode scanner, card reader, printer) for any visible issues.",
        "Ensure all peripherals are securely connected.",
        "Test Hardware Components:",
        "Use the kiosk's hardware testing tools to ensure all components are functioning.",
        "Replace any faulty peripherals or components as necessary.",
        "Log Analysis",
        "Review System Logs:",
        "Access the kiosk's system logs to look for any errors or warnings.",
        "Use log entries to identify potential causes of the issue.",
        "Escalate if Necessary:",
        "If the issue is not resolved, escalate to the appropriate technical team with detailed log information.",
        "Documentation and Follow-Up",
        "Record Incident Details:",
        "Document all steps taken during troubleshooting.",
        "Include details of any error messages, system logs, and actions performed.",
        "Report to Management:",
        "Inform relevant stakeholders of the issue and steps taken to resolve it.",
        "Provide recommendations for preventing similar issues in the future.",
    )

    prerequisites = (
        "Prerequisites:",
        "Access to the kiosk's administrative interface",
        "Basic knowledge of the kiosk's operating system and software",
        "Necessary credentials for accessing network and system settings",
        "Tools for physical inspection (e.g., flashlight, screwdrivers)",
    )

    return {
        "title": "Troubleshooting Self-Checkout Kiosks Not Working",
        "prerequisites": prerequisites,
        "troubleshooting_steps": steps,
    }


async def handle_blue_screen_issue(**kwargs):
    steps = (
        "Identifying the Issue",
        "Please confirm if you're experiencing the following symptoms:",
        "Blue screen error on your computer",
        "Unable to access normal Windows operation",
        "There are recent reports of a Microsoft outage",
        "Are you experiencing these symptoms?",
        "Step 1: Restart in Safe Mode",
        "Restart your computer",
        "Press and hold the F8 key (or Shift + F8) during startup until the Advanced Boot Options menu appears",
        "Select 'Safe Mode' and press Enter",
        "Check if the blue screen error appears in Safe Mode",
        "If it doesn't appear, restart your computer normally",
        "Have you completed this step? Did it resolve the issue?",
        "Step 2: Use Advanced Startup Options",
        "Hold the Shift key while selecting Restart from the Start menu",
        "Navigate to 'Troubleshoot', then 'Advanced options', then 'Startup Repair'",
        "Allow the system to run the Startup Repair process",
        "Follow any on-screen instructions and restart your computer",
        "Have you completed this step? Did it resolve the issue?",
        "Escalating the Issue",
        "Since the issue persists, we need to escalate this to our support team.",
        "I will now transfer you to a human agent for further assistance.",
        "The human agent will attempt additional troubleshooting.",
        "If the issue cannot be resolved, the agent will create a support ticket for further investigation.",
        "Do you understand the escalation process? Do you have any questions before we proceed?",
        "Creating a Support Ticket",
        "A support ticket will be created with the following process:",
        "The human agent will create a ticket with detailed information about the issue.",
        "You will receive a reference number for tracking purposes.",
        "The technical team will review the ticket and investigate the issue.",
        "Expect an update within 24 to 48 hours.",
        "Do you have any questions about the ticket creation process?",
        "Follow-Up and Resolution",
        "After the ticket is created:",
        "Monitor your email or the support portal for updates on your ticket.",
        "Follow any additional instructions provided by the technical team.",
        "If the issue persists or you need further assistance, contact support again with your ticket reference number.",
        "Do you understand the follow-up process?",
        "Contact Information",
        "For additional help or to check the status of your support ticket, please contact us:",
        "Email: support@company.com",
        "Phone: 1-800-123-4567",
        "Chat: Available on our website during business hours",
        "Do you need any clarification on how to contact us for further assistance?",
        "Transfer to Human Agent",
        "I'll now transfer you to a human agent for further assistance.",
        "Is there anything else you'd like to know before I transfer you?",
    )
    return {"troubleshooting_steps": steps}

## GOOGLE USE CASES
async def get_google_meet_connectivity_troubleshooting(**kwargs):
    steps = (
        "Check Internet Connection",
        "Ensure your device is connected to a stable internet connection.",
        "Restart your router if necessary.",
        "Verify Meeting Link",
        "Double-check the meeting link and ensure it is correct.",
        "If the link was copied, make sure there are no extra spaces.",
        "Browser Check",
        "Ensure you are using a supported browser (e.g., Chrome, Firefox, Edge).",
        "Clear the browser cache and cookies:",
        "  - Go to browser settings.",
        "  - Select 'Privacy and security'.",
        "  - Clear browsing data.",
        "Allow Permissions",
        "Make sure your browser has permission to use your camera and microphone:",
        "  - In Chrome, go to 'Settings' > 'Privacy and security' > 'Site settings'.",
        "  - Ensure 'Camera' and 'Microphone' permissions are set to 'Allow'.",
        "Disable Extensions",
        "Disable any browser extensions that might interfere with Google Meet.",
        "To disable extensions in Chrome:",
        "  - Go to 'More tools' > 'Extensions'.",
        "  - Toggle off extensions one by one and try joining the meeting again.",
        "Update Browser and OS",
        "Ensure your browser and operating system are up to date.",
        "Update to the latest version if necessary.",
        "Try Incognito/Private Mode",
        "Open an incognito or private window in your browser.",
        "Try joining the meeting again.",
        "Network Settings",
        "Check firewall and antivirus settings to ensure they are not blocking Google Meet.",
        "Configure network settings to allow access to Google services.",
        "Reboot Device",
        "Restart your device to clear any temporary issues.",
    )

    prerequisites = (
        "Prerequisites:",
        "Access to the device settings",
        "Administrative rights on the device",
        "Knowledge of browser settings",
    )

    return {
        "title": "Troubleshooting Google Meet Connectivity Issues",
        "prerequisites": prerequisites,
        "troubleshooting_steps": steps,
    }


async def get_chromebook_performance_troubleshooting(**kwargs):
    steps = (
        "Close Unnecessary Tabs and Apps",
        "Close any unused tabs and apps to free up system resources.",
        "Check for Updates",
        "Go to 'Settings' > 'About Chrome OS' > 'Check for updates'.",
        "Install any available updates.",
        "Clear Browsing Data",
        "Open Chrome.",
        "Go to 'Settings' > 'Privacy and security' > 'Clear browsing data'.",
        "Select 'All time' and clear data.",
        "Remove Unnecessary Extensions",
        "Open Chrome.",
        "Go to 'More tools' > 'Extensions'.",
        "Remove or disable any extensions you don't need.",
        "Restart Your Chromebook",
        "Restart the device to clear temporary files and refresh the system.",
        "Check Storage Space",
        "Go to 'Files' > 'My files'.",
        "Delete any unnecessary files to free up storage.",
        "Perform a Hardware Reset",
        "Turn off your Chromebook.",
        "Press and hold the 'Refresh' button and tap the 'Power' button.",
        "Release the 'Refresh' button when the Chromebook starts up.",
        "Check for Malware",
        "Run a malware scan using a trusted Chromebook-compatible antivirus app.",
        "Powerwash (Factory Reset)",
        "Go to 'Settings' > 'Advanced' > 'Reset settings' > 'Powerwash'.",
        "Follow the instructions to reset your Chromebook to factory settings (backup important data first).",
    )

    prerequisites = (
        "Prerequisites:",
        "Access to Chromebook settings",
        "Backup of important data",
        "Knowledge of Chrome OS interface",
    )

    return {
        "title": "Troubleshooting Chromebook Performance Issues",
        "prerequisites": prerequisites,
        "troubleshooting_steps": steps,
    }


async def get_google_drive_syncing_troubleshooting(**kwargs):
    steps = (
        "Check Internet Connection",
        "Ensure you have a stable internet connection.",
        "Check Google Drive Status",
        "Visit the Google Workspace Status Dashboard to check if there are any ongoing issues with Google Drive.",
        "Verify Account Login",
        "Ensure you are logged into the correct Google account.",
        "Go to 'Drive' > 'Profile' and check the account information.",
        "Restart Google Drive",
        "Quit Google Drive and reopen it.",
        "On a Chromebook, restart the device.",
        "Check Storage Space",
        "Ensure you have enough storage space in your Google Drive account.",
        "Delete unnecessary files or upgrade your storage plan if needed.",
        "Check Sync Settings",
        "Go to Google Drive settings and ensure syncing is enabled.",
        "In Google Drive app: 'Settings' > 'General' > 'Sync' > Toggle to 'On'.",
        "Clear Cache",
        "Clear the cache of your Google Drive app or browser.",
        "Update Google Drive",
        "Ensure you have the latest version of the Google Drive app installed.",
        "Disable Conflicting Apps",
        "Disable any other apps or services that might be interfering with Google Drive.",
    )

    prerequisites = (
        "Prerequisites:",
        "Access to Google Drive settings",
        "Knowledge of Google account management",
        "Admin rights on the device (for app management)",
    )

    return {
        "title": "Troubleshooting Google Drive Syncing Issues",
        "prerequisites": prerequisites,
        "troubleshooting_steps": steps,
    }


async def get_chromebook_printing_setup(**kwargs):
    steps = (
        "Check Printer Compatibility",
        "Ensure your printer is compatible with Chromebooks.",
        "Connect Printer to Wi-Fi",
        "Follow the printer manufacturer's instructions to connect the printer to your Wi-Fi network.",
        "Add Printer to Chromebook",
        "Go to 'Settings' > 'Advanced' > 'Printing' > 'Printers'.",
        "Click 'Add Printer'.",
        "Select your printer from the list of available printers.",
        "Follow the on-screen instructions to complete the setup.",
        "Print a Test Page",
        "Open a document or webpage.",
        "Press 'Ctrl + P' or go to 'File' > 'Print'.",
        "Select your printer and print a test page.",
        "Install Printer App (if needed)",
        "Some printers may require you to install a specific app from the Chrome Web Store.",
        "Update Chromebook",
        "Ensure your Chromebook is up to date by going to 'Settings' > 'About Chrome OS' > 'Check for updates'.",
        "Check Printer Status",
        "Ensure your printer is turned on and has enough paper and ink.",
        "Troubleshoot Printer Connection",
        "Restart your printer and Chromebook.",
        "Ensure both devices are on the same Wi-Fi network.",
        "Check Printer Queue",
        "Go to 'Settings' > 'Advanced' > 'Printing' > 'Printers' > 'Manage'.",
        "Clear any pending print jobs and try printing again.",
    )

    prerequisites = (
        "Prerequisites:",
        "Compatible printer",
        "Wi-Fi network access",
        "Chromebook with latest updates",
    )

    return {
        "title": "Setting Up Printing on Chromebooks",
        "prerequisites": prerequisites,
        "troubleshooting_steps": steps,
    }


async def get_google_groups_management_troubleshooting(**kwargs):
    steps = (
        "Verify Group Permissions",
        "Ensure you have the necessary permissions to add members to the Google Group.",
        "Go to 'Google Groups' > 'My Groups' > Select your group > 'Manage group' > 'Permissions'.",
        "Check Member Limit",
        "Ensure the group has not reached its maximum member limit.",
        "Add Members",
        "Go to 'Google Groups'.",
        "Select your group.",
        "Click 'Manage group' on the left sidebar.",
        "Go to 'Members' > 'Direct add members'.",
        "Enter the email addresses of the new members.",
        "Click 'Add'.",
        "Verify Email Addresses",
        "Ensure the email addresses you are adding are correct and active.",
        "Check Admin Console (for Workspace Admins)",
        "If you are a Google Workspace admin, go to the Admin Console.",
        "Navigate to 'Groups'.",
        "Select the group and check the group settings and permissions.",
        "Check Invitation Status",
        "If members were invited but have not joined, resend the invitations.",
        "Go to 'Google Groups' > 'Pending members'.",
        "Update Group Settings",
        "Ensure group settings allow new members to be added.",
        "Go to 'Google Groups' > 'Settings' > 'Access settings'.",
        "Clear Browser Cache",
        "Clear your browser cache and cookies to ensure there are no temporary issues.",
        "Update Browser",
        "Ensure your browser is up to date.",
    )

    prerequisites = (
        "Prerequisites:",
        "Access to Google Groups management",
        "Appropriate permissions for group management",
        "Up-to-date browser",
    )

    return {
        "title": "Troubleshooting Google Groups Management Issues",
        "prerequisites": prerequisites,
        "troubleshooting_steps": steps,
    }


async def get_microsoft_teams_login_loop_troubleshooting(**kwargs):
    causes = (
        "Corrupted cache and cookies",
        "Account sign-in issues",
        "Interference from browser extensions",
        "Incorrect browser settings",
    )

    steps = (
        "Clear Browser Cache and Cookies",
        "Open Microsoft Edge. Click on the three dots (menu) in the upper-right corner. Select 'Settings.' Under 'Privacy, search, and services,' scroll down to the 'Clear browsing data' section and click 'Choose what to clear.' Select 'Cookies and other site data' and 'Cached images and files.' Click 'Clear now.'",
        "Sign Out and Sign Back In",
        "Open Microsoft Edge. Click on your profile picture in the upper-right corner. Select 'Sign out.' Close and reopen Edge. Click on your profile picture again and sign back into your Microsoft account.",
        "Use InPrivate Window",
        "Open Microsoft Edge. Click on the three dots (menu) in the upper-right corner. Select 'New InPrivate window.' In the InPrivate window, try logging into Teams again.",
        "Disable Extensions",
        "Click on the three dots (menu) in the upper-right corner. Select 'Extensions.' Turn off each extension one by one and check if you can log into Teams each time.",
        "Reset Browser Settings",
        "Click on the three dots (menu) in the upper-right corner. Select 'Settings.' Scroll down and click on 'Reset settings.' Click on 'Restore settings to their default values.'",
    )

    additional_tips = (
        "Keep Edge Updated: Ensure that you are using the latest version of Microsoft Edge. Updates often include performance improvements and bug fixes.",
        "Check for Network Issues: Ensure that your internet connection is stable and not experiencing intermittent issues.",
    )

    return {
        "title": "Resolving Microsoft Teams Login Loop in Microsoft Edge",
        "causes": causes,
        "troubleshooting_steps": steps,
        "additional_tips": additional_tips,
    }


async def get_onedrive_sluggish_performance_troubleshooting(**kwargs):
    causes = (
        "Poor or unstable internet connection",
        "Outdated OneDrive application",
        "Large file sizes",
        "Corrupted cache files",
        "Network congestion or interference",
    )

    steps = (
        "Check Internet Connection",
        "Ensure that your internet connection is stable and fast. You can run an internet speed test to verify your upload and download speeds.",
        "Restart OneDrive",
        "Right-click the OneDrive icon in the system tray. Select 'Quit OneDrive.' Reopen OneDrive from the Start menu or by searching for it.",
        "Update OneDrive",
        "Open OneDrive. Click on the Help & Settings icon in the system tray. Select 'Settings.' Go to the 'About' tab. Click 'Version' to see if an update is available. Install any available updates.",
        "Check for Large Files",
        "Uploading or downloading very large files can slow down OneDrive. If possible, try splitting large files into smaller parts and then upload or download them.",
        "Clear OneDrive Cache",
        "Close OneDrive by right-clicking the OneDrive icon in the system tray and selecting 'Quit OneDrive.' Open the File Explorer and navigate to: C:\\Users\\[Your Username]\\AppData\\Local\\Microsoft\\OneDrive\\. Find the folder named 'Settings' and delete it. Restart your computer. Open OneDrive again.",
    )

    additional_tips = (
        "Pause and Resume Syncing: Sometimes pausing and resuming syncing can help. Right-click the OneDrive icon and select 'Pause syncing,' then resume after a few minutes.",
        "Check for Network Interference: Ensure that no other applications or devices are consuming excessive bandwidth on your network.",
        "Use Ethernet: If you're on Wi-Fi, try using a wired Ethernet connection for more stable performance.",
    )

    return {
        "title": "Resolving Sluggish Performance in OneDrive",
        "causes": causes,
        "troubleshooting_steps": steps,
        "additional_tips": additional_tips,
    }


async def get_concur_expense_login_troubleshooting(**kwargs):
    steps = (
        "Verify Credentials",
        "Ensure you are entering the correct username and password. Check for any typos or case sensitivity.",
        "Reset Password",
        "If you have forgotten your password, use the 'Forgot Password' link on the login page to reset it.",
        "Check Internet Connection",
        "Ensure that your internet connection is stable and working. Try accessing other websites to confirm.",
        "Clear Cache and Cookies",
        "Open your browser settings, navigate to the Privacy or History section, clear your cache and cookies, then restart the browser.",
        "Update Browser",
        "Ensure that your browser is up to date with the latest version.",
        "Try a Different Browser",
        "If the issue persists, try logging in using a different browser.",
        "Disable VPN",
        "If you are using a VPN, disable it temporarily and try logging in again.",
        "Check Firewall Settings",
        "Ensure that your firewall is not blocking access to the Concur website.",
        "Update Operating System",
        "Ensure that your operating system is up to date with the latest updates and patches.",
    )

    additional_tips = (
        "Check for Maintenance: Verify if Concur is undergoing scheduled maintenance.",
        "Verify Account Status: Ensure your account is active and not locked or disabled.",
        "Use a secure password manager to store and manage your login credentials.",
        "Periodically clear your browser cache and cookies to prevent login issues.",
    )

    return {
        "title": "Troubleshooting Login Issues with Concur Expense Reporting",
        "troubleshooting_steps": steps,
        "additional_tips": additional_tips,
    }


async def get_okta_issues_troubleshooting_steps(**kwargs):
    steps = (
        "Verify if it's a PC/browser-related issue or an OKTA site-related issue. Ask if the issue is happening on one PC or all PCs",
        "If one PC affected:",
        "Let's try troubleshooting your PC. Can you please clear your browser's cache and cookies.",
        "After clearing cache and cookies, try rebooting it?",
        "Now try accessing the OKTA site again. Did it work?",
        "If still not working or all PCs affected:",
        "I'll need to escalate this issue. For one PC, it will go to Endpoint Support. For all PCs, it will go to IAM Support.",
    )

    return {"title": "Troubleshooting Okta Issues", "troubleshooting_steps": steps}


async def get_printer_setup_on_laptop(**kwargs):
    steps = (
        "Verify Printer Compatibility",
        "Ensure that the printer is compatible with the laptop's operating system. Check the printer's documentation or manufacturer's website for compatibility information.",
        "Gather Necessary Materials",
        "Ensure you have the printer's power cable and USB cable (if applicable). Have the printer driver CD or access to the manufacturer's website for driver downloads.",
        "Connect the Printer",
        "For USB Printers: Turn off the printer and the laptop. Connect the printer to the laptop using the USB cable. Turn on the printer and the laptop. For Wireless Printers: Ensure the printer is connected to the same Wi-Fi network as the laptop.",
        "Install Printer Drivers",
        "Using the Printer's CD: Insert the CD into the laptop's drive and follow the on-screen instructions. Downloading Drivers from the Internet: Visit the printer manufacturer's website, download the latest drivers for your operating system, and run the installation wizard.",
        "Add the Printer to the Laptop",
        "For Windows: Go to Start > Settings > Devices. Click on Printers & Scanners. Click Add a printer or scanner. Select the printer from the list and click Add device. For macOS: Click on the Apple menu and select System Preferences. Click on Printers & Scanners. Click the + button to add a new printer.",
        "Print a Test Page",
        "Open a document or image. Go to File > Print. Select the newly added printer and click Print. Verify that the printer produces the expected output.",
    )

    troubleshooting_tips = (
        "If the printer is not detected, ensure it's powered on and properly connected. Try using a different USB port or cable if applicable.",
        "For print quality issues, check the printer for any paper jams or low ink levels. Run a cleaning cycle from the printer's maintenance menu.",
    )

    return {
        "title": "Setting Up a Printer on a Laptop",
        "setup_steps": steps,
        "troubleshooting_tips": troubleshooting_tips,
    }


async def get_distribution_list_management(**kwargs):
    steps = (
        "Create a Distribution List",
        "Using Outlook: Open Outlook, navigate to Home > New Items > More Items > Contact Group. Enter a name for the DL, add members, and save. Using Microsoft 365 Admin Center: Log in, navigate to Groups > Active groups, click Add a group, select Distribution list, enter required information, add members, and create.",
        "Modify a Distribution List",
        "Using Outlook: Open the DL in Contacts view, add or remove members, and save changes. Using Microsoft 365 Admin Center: Navigate to Groups > Active groups, select the DL, edit members, and save changes.",
        "Delete a Distribution List",
        "Using Outlook: In Contacts view, right-click the DL and select Delete. Using Microsoft 365 Admin Center: Navigate to Groups > Active groups, select the DL, click Delete group, and confirm.",
    )

    troubleshooting_tips = (
        "For permission errors, ensure you have the necessary permissions to manage DLs. Contact your IT department if access is denied.",
        "For email delivery issues, verify that all email addresses in the DL are correct. Check for any undeliverable email notifications and adjust the DL accordingly.",
    )

    return {
        "title": "Managing Distribution Lists",
        "management_steps": steps,
        "troubleshooting_tips": troubleshooting_tips,
    }


async def get_shared_drive_access_troubleshooting(**kwargs):
    steps = (
        "Verify Network Connection",
        "Ensure your computer is connected to the network via Ethernet or Wi-Fi. Check that you can access other network resources, such as the internet or other shared drives.",
        "Check Drive Availability",
        "Confirm with colleagues that the shared drive is available and accessible to them. Ensure the server hosting the shared drive is powered on and connected to the network.",
        "Verify Login Credentials",
        "Double-check that you are using the correct username and password. Ensure your account has the necessary permissions to access the shared drive.",
        "Reset Credentials",
        "Go to Control Panel > Credential Manager. Remove any saved credentials for the shared drive and try accessing it again to prompt for fresh login credentials.",
        "Access the Shared Drive",
        "Using Windows File Explorer: Type \\ServerName\ShareName in the address bar. Mapping the Network Drive: In File Explorer, select This PC, click on Map network drive, select a drive letter, enter the path, and check Reconnect at sign-in.",
        "Troubleshoot Network Settings",
        "Temporarily disable any firewall or security software. Flush DNS cache by running ipconfig /flushdns in Command Prompt. Check Network Discovery Settings in Control Panel.",
    )

    advanced_troubleshooting = (
        "Verify Server Connection: Use the ping command to check connectivity with the server.",
        "Check Server Shares: Contact the server administrator to verify that the shared folder is correctly configured and accessible.",
    )

    return {
        "title": "Troubleshooting Inability to Access a Shared Drive",
        "troubleshooting_steps": steps,
        "advanced_troubleshooting": advanced_troubleshooting,
    }


async def get_adobe_acrobat_signature_troubleshooting(**kwargs):
    steps = (
        "Verify Document Permissions",
        "Open the document in Adobe Acrobat. Navigate to File > Properties. Ensure that the Security tab shows 'Signing Allowed.'",
        "Check for Updates",
        "Open Adobe Acrobat. Go to Help > Check for Updates. Install any available updates to ensure compatibility and bug fixes.",
        "Set Up a Digital ID",
        "In Adobe Acrobat, click on Edit > Preferences. Select Signatures from the left menu. Under Identities & Trusted Certificates, click More. In Digital ID Files, click Add ID and follow the prompts to create or import a digital ID.",
        "Trust Certificates",
        "Go to Edit > Preferences. Select Trust Manager. Click Update Now to refresh the trusted certificates list.",
        "Prepare Document for Signing",
        "Open the document in Adobe Acrobat. Navigate to Tools > Prepare Form. Add signature fields by clicking on Add a Signature Block and placing it in the document.",
        "Send for Signature",
        "Go to Tools > Request Signatures. Enter the email addresses of the signers. Click Send to dispatch the document for electronic signature.",
    )

    advanced_troubleshooting = (
        "Installation Repair: Go to Help > Repair Installation and follow the on-screen instructions.",
        "Reinstall Adobe Acrobat: Uninstall Adobe Acrobat, download the latest version from the Adobe website, and reinstall.",
    )

    return {
        "title": "Resolving Signature Issues in Adobe Acrobat",
        "troubleshooting_steps": steps,
        "advanced_troubleshooting": advanced_troubleshooting,
    }


async def get_bitlocker_recovery_key_access(**kwargs):
    steps = (
        "Check Microsoft Account",
        "Visit the Microsoft account devices page. Sign in with the Microsoft account linked to your PC. Locate your device and select it to view the BitLocker recovery key.",
        "Search for Printout or File",
        "Check any documents or files you may have printed or saved during BitLocker setup. Look in common file locations such as the Documents folder or a dedicated BitLocker folder.",
        "Check USB Drive",
        "Insert the USB drive into your PC. Open File Explorer and browse the drive to locate a file named 'BitLocker Recovery Key.'",
        "Contact IT for Active Directory",
        "If your device is part of an organization, contact your IT department for assistance in retrieving the recovery key from Active Directory.",
        "Access Azure Active Directory",
        "Go to the Azure AD portal. Sign in with your work or school account. Navigate to Azure Active Directory > Devices > BitLocker keys to find the recovery key.",
    )

    using_key = (
        "Start your PC and follow the prompts to enter the BitLocker recovery key.",
        "Enter the recovery key when prompted to unlock the encrypted drive.",
    )

    troubleshooting_tips = (
        "Double-check all possible locations for the recovery key.",
        "Contact your IT department if your device is part of an organization.",
        "Without the recovery key, the encrypted drive cannot be unlocked. Ensure the key is backed up in a secure location for future use.",
    )

    return {
        "title": "Accessing a BitLocker Recovery Key",
        "access_steps": steps,
        "using_key": using_key,
        "troubleshooting_tips": troubleshooting_tips,
    }


async def get_bsod_troubleshooting(**kwargs):
    steps = (
        "Record Error Information",
        "Note the error code and message displayed on the BSOD screen (e.g., 0x0000001E or IRQL_NOT_LESS_OR_EQUAL). Take a photo of the screen if needed for future reference.",
        "Restart the Computer",
        "Hold the power button to turn off the computer. Wait a few seconds and then power it back on.",
        "Boot in Safe Mode",
        "Restart the computer and press F8 (or Shift + F8 for Windows 8/10) during startup to access the Advanced Boot Options menu. Select Safe Mode or Safe Mode with Networking.",
        "Update Drivers",
        "Open Device Manager in Safe Mode. Expand each category and look for devices with a yellow exclamation mark. Right-click the device and select Update driver.",
        "Check for Windows Updates",
        "Open Settings > Update & Security. Click Check for updates to ensure Windows is up to date.",
        "Run a System File Check",
        "Open Command Prompt as an administrator. Type sfc /scannow and press Enter to scan for and repair corrupted system files.",
    )

    advanced_troubleshooting = (
        "Check for Hardware Issues: Ensure all internal components (RAM, GPU, HDD/SSD) are properly connected. Use tools like Windows Memory Diagnostic to test RAM.",
        "Analyze Dump Files: Use a tool like BlueScreenView or WinDbg to analyze the minidump files located in C:\\Windows\\Minidump.",
        "Perform a System Restore: Open Control Panel > Recovery. Click Open System Restore and follow the prompts to restore the system to a previous state.",
    )

    return {
        "title": "Troubleshooting Blue Screen of Death (BSOD) Issues",
        "troubleshooting_steps": steps,
        "advanced_troubleshooting": advanced_troubleshooting,
    }


async def get_veeva_crm_ipad_installation(**kwargs):
    steps = (
        "Download the App",
        "Open the App Store on your iPad. Tap the Search tab and type 'Veeva CRM' into the search bar. Locate the official Veeva CRM app and tap Get to download and install it.",
        "Initial Setup",
        "Open the Veeva CRM app once installation is complete. Allow any requested permissions for the app to function properly (e.g., access to contacts, camera).",
        "Login and Configuration",
        "Enter your Veeva CRM username and password on the login screen. Tap Log In to proceed. Follow the prompts to configure any initial settings, such as language preferences or region.",
        "Connect to Salesforce",
        "After logging in, navigate to the Settings or Connections menu within the app. Locate the option to integrate or connect with Salesforce. Enter your Salesforce login credentials if prompted. Follow the instructions to authorize the connection between Veeva CRM and Salesforce.",
        "Initial Sync",
        "Ensure your iPad is connected to Wi-Fi. Tap the Sync button within the app to begin syncing data from Salesforce. Wait for the sync process to complete before proceeding to ensure all data is up-to-date.",
    )

    troubleshooting_tips = (
        "For login issues: Verify that your credentials are correct. Ensure you have an active internet connection. Reset your password using the 'Forgot Password' link if necessary.",
        "For sync errors: Confirm the iPad is connected to Wi-Fi and has a stable internet connection. Restart the app and try syncing again. Check for any app updates in the App Store that may resolve known issues.",
    )

    return {
        "title": "Installing and Activating Veeva CRM on an iPad",
        "installation_steps": steps,
        "troubleshooting_tips": troubleshooting_tips,
    }


async def get_sap_gui_installation(**kwargs):
    steps = (
        "Download SAP GUI",
        "Log in to the SAP support portal using your credentials. Navigate to the 'Downloads' section. Search for the latest version of SAP GUI for your operating system. Download the installation package and save it to a convenient location on your computer.",
        "Prepare for Installation",
        "Backup any important data to avoid loss during the installation process. Temporarily disable any antivirus software to prevent it from interfering with the installation.",
        "Extract Installation Files",
        "Navigate to the location where you saved the downloaded SAP GUI installation package. Extract the contents of the ZIP file to a new folder.",
        "Run the Installer",
        "Open the extracted folder and locate the SetupAll.exe file. Right-click on SetupAll.exe and select 'Run as administrator.'",
        "Follow Installation Wizard",
        "The SAP GUI installation wizard will open. Follow the on-screen instructions. Select the components you want to install (SAP GUI, BEx Frontend, etc.). Choose the installation directory or leave it as default. Click 'Next' to proceed with the installation.",
        "Complete Installation",
        "Once the installation is complete, click 'Finish.' Restart your computer if prompted.",
        "Configure SAP GUI",
        "Open SAP Logon from the start menu or desktop shortcut. Click on 'New Item' to add a new SAP system. Enter the necessary connection details (SAP server, system number, etc.). Save the configuration.",
        "Test the Connection",
        "Select the newly added SAP system and click 'Log On.' Enter your SAP credentials to verify the connection.",
    )

    troubleshooting_tips = (
        "For installation errors: Ensure all prerequisites are met. Check for sufficient disk space. Verify you have the correct installation files for your operating system.",
        "For connection issues: Double-check the server and system details. Ensure your network connection is stable. Contact your SAP administrator if issues persist.",
    )

    return {
        "title": "Installing SAP GUI",
        "installation_steps": steps,
        "troubleshooting_tips": troubleshooting_tips,
    }


async def get_slow_computer_troubleshooting(**kwargs):
    steps = (
        "Open Task Manager (Ctrl + Shift + Esc on Windows).",
        "Identify and close programs that are using a lot of resources.",
        "Use Disk Cleanup on Windows to remove temporary files.",
    )

    return {
        "title": "Troubleshooting a Slow Computer",
        "troubleshooting_steps": steps,
    }