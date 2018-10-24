
Step1

menuselection:`[Odoo] --> [All Apps]`

- Search and Install "SaBRO Communications" module
- Click on install to get started with SaBRO Communications

.. image:: /sabro_communications/static/src/img/install.png
   :align: center
   :width: 700


Step2

- Enter the following information:

	1. Company Name

	2. The Admin Name

	3. Login Email (to access SaBRO Node)

	4. Country

	5. Mobile/Phone Number (For Verification)

	6. Sub-domain (URL for SaBRO Node)

- Click on "Save" button after providing valid information

.. image:: /sabro_communications/static/src/img/provideDetails.png
   :align: center
   :width: 700
   
Note: 

1. Installing SaBRO will create new sub-menu as “SaBRO Setup”. 
2. SaBRO setup is required to enable the communications features. 


Step3

- Click on Verify OTP button to initiate the verification process. 
- SaBRO Cloud will place a call on entered mobile number with 6-digit one time password (OTP).

.. image:: /sabro_communications/static/src/img/otp.png
   :align: center
   :width: 700

Note: Review all the filled information's before verifying the Mobile/Phone number.

Step4

- Enter the one time password received on provided mobile via call and click on “SAVE” button.
- In case, you do not receive any call or missed the call, you can request new OTP by clicking on “Call Again”.

.. image:: /sabro_communications/static/src/img/enterCode.png
   :align: center
   :width: 700

Note: You can place maximum 3 calls.

Step5

- Click on “SAVE” button will initialize the SaBRO Communication  provisioning.
- After successful provision, an email will be sent to Login Email for SaBRO Login.

.. image:: /sabro_communications/static/src/img/provisioning.png
   :align: center
   :width: 700


Step6

- Once the provisioning is completed, user will be redirected to the App page.
- To access the Communication HUB, user needs to have SaBRO permission.
- Go to user > SaBRO Services > SaBRO Access > Enable SaBRO Communications to give permissions.
- After refreshing the web page, Communications HUB icon will appear on header.
 
.. image:: /sabro_communications/static/src/img/userPermission.png
   :align: center
   :width: 700


Step7

- Communication HUB can be opened on click call icon available on header and ready to receive and make calls.

.. image:: /sabro_communications/static/src/img/CommunicationsHub.png
   :align: center
   :width: 700

What will I get on Odoo?
-----------------------------------------------------------

1. Receive incoming calls
2. Make outgoing calls
3. Make extension calls
4. Check and listen to voicemails
5. See recent calls

What can I do on SaBRO Cloud?
-----------------------------------------------------------
Advanced Communications Features (Links for SaBRO user/admin guide)

Enable communications for Odoo users
-----------------------------------------------------------

Enable communications for existing user on Odoo

- Go to user > SaBRO Services > Enable SaBRO Communications

Enable communications for existing user on SaBRO

- Go to user > SaBRO Services > Enable SaBRO Communications > SAVE
- SaBRO User > Select user from dropdown list > SAVE

Enable communications for new user created on Odoo

- Create an Odoo user
- Go to user > SaBRO Services > Enable SaBRO Communications > SAVE

Communications settings for Odoo users
-----------------------------------------------------------

- When SaBRO Services are enabled for an Odoo user, a button "Manage User at SaBRO" is available  to login to the SaBRO Cloud.
- User will be redirected to the SaBRO user page.
- Communications setting can be managed under "communications" tab.

Known Limitations
===============================

1. Communications settings are not visible or accessible directly on Odoo.
2. 2FA, the account security feature will not work for login to SaBRO Nodes from Odoo.
3. Module uninstallation is required if the signup gets interrupted.
4. Users created on SaBRO will appear on Odoo for user mapping after each 24hrs.







