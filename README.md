================================================================================

                                 WhatsBlaster

================================================================================



A lightweight Python automation tool designed to streamline bulk candidate and 

client outreach via WhatsApp Web. WhatsBlaster reads structured data from CSV 

files, generates personalized messages, handles invalid contact modals, and uses 

computer vision template matching to visually verify sent status (single/double 

ticks) before exporting a comprehensive delivery audit.



--------------------------------------------------------------------------------

FEATURES

--------------------------------------------------------------------------------



- Dynamic Data Ingestion:

  Parses contacts directly from CSV (name, id, no) with automatic phone number 

  normalization.



- Fast Input Automation:

  Uses clipboard memory injection (pyperclip + pyautogui) to handle multi-line 

  templates instantly without character lag.



- Visual Delivery Auditing:

  Scans specific on-screen UI bounds to detect WhatsApp delivery ticks 

  (sent.png, sent_receved.png, sent_receved_viewed.png).



- Modal & Error Handling:

  Detects and handles "Phone number shared via url is invalid" dialogs 

  automatically.



- Audit Log Export:

  Exports full campaign execution results to delivery_status_report.csv.



--------------------------------------------------------------------------------

PROJECT STRUCTURE

--------------------------------------------------------------------------------



WhatsBlaster/

|-- whatsblaster.py              # Main execution script

|-- whatsapp_automation.csv      # Contact input list

|-- delivery_status_report.csv   # Auto-generated export log

`-- assets/                      # Reference icons for template matching

    |-- invalid_popup.png

    |-- sent.png

    |-- sent_receved.png

    `-- sent_receved_viewed.png



--------------------------------------------------------------------------------

PREREQUISITES

--------------------------------------------------------------------------------



1. Python 3.8+

2. Logged-in WhatsApp Web Session:

   Ensure your default web browser has WhatsApp Web pre-authenticated and kept 

   open/ready.

3. Reference Screenshots:

   Save crop references of WhatsApp icons into your project root directory:

   - invalid_popup.png      : "Phone number shared via url is invalid" popup/OK

   - sent.png               : Single grey tick

   - sent_receved.png       : Double grey ticks

   - sent_receved_viewed.png: Double blue ticks



--------------------------------------------------------------------------------

INSTALLATION

--------------------------------------------------------------------------------



1. Clone or download the repository:

   git clone https://github.com/your-username/WhatsBlaster.git

   cd WhatsBlaster



2. Install dependencies:

   pip install pandas pyautogui pyperclip pillow opencv-python



--------------------------------------------------------------------------------

INPUT FILE FORMAT (whatsapp_automation.csv)

--------------------------------------------------------------------------------



Place a file named "whatsapp_automation.csv" in the root directory:



name,id,no

Alex Mercer,EMP101,9876543210

Jane Doe,EMP102,+91 91234-56789



Note: The script normalizes phone numbers by stripping spaces/hyphens and 

prepending country code '91' to the last 10 digits. Adjust the country prefix 

in the script if operating outside India.



--------------------------------------------------------------------------------

USAGE

--------------------------------------------------------------------------------



1. Open your primary web browser and log into WhatsApp Web (https://web.whatsapp.com).

2. Keep your browser window maximized on your main monitor.

3. Run the script:

   python whatsblaster.py

4. Hands-off Execution:

   You have a 5-second buffer before the script begins. Do not touch your mouse 

   or keyboard while the program runs to prevent input interruptions.



--------------------------------------------------------------------------------

DELIVERY LOG OUTPUT (delivery_status_report.csv)

--------------------------------------------------------------------------------



Once execution completes, "delivery_status_report.csv" is created:



name,id,phone,status

Alex Mercer,EMP101,919876543210,Sent

Jane Doe,EMP102,919123456789,Not on WhatsApp / Failed



--------------------------------------------------------------------------------

DISCLAIMER

--------------------------------------------------------------------------------



This software is for operational automation and personal productivity purposes. 

Use responsibly and adhere to WhatsApp's Terms of Service. Avoid mass unsolicited 

messaging to minimize the risk of temporary or permanent account restrictions.

================================================================================
