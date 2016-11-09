=================================================
All-IP Two-Factor SMS & Call Authentication (2FA)
=================================================

App Installation on Odoo:
=========================

:menuselection:`[Odoo] --> [All Apps]`
--------------------------------------

-  Search and Install "All-IP Two-Factor" module

.. image:: https://web-resource.allip.io/github/allip_digits_2f_authentication/media/DigitsAuthenticationEndUser2.jpg
   :align: center
   :width: 700

App Configuration on Odoo:
==========================

:menuselection:`[All Apps] --> Settings -->All-IP Settings`
-----------------------------------------------------------

-  Go to All-IP settings
-  Select '2FA Configuration'

.. image:: https://web-resource.allip.io/github/allip_digits_2f_authentication/media/DigitsAuthenticationEndUser6.jpg
   :align: center
   :width: 700

|
-  Enter CONSUMER KEY (If already available)
- In order to get CONSUMER KEY (API KEY), please raise a request by clicking on "Request Digits Consumer Key".

.. image:: https://web-resource.allip.io/github/allip_digits_2f_authentication/media/DigitsAuthenticationEndUser8.jpg
   :align: center
   :width: 700

|
-  Submit Consumer key request form after providing valid information

.. image:: https://web-resource.allip.io/github/allip_digits_2f_authentication/media/consumer_key_form.png
   :align: center
   :width: 700

|
-  Enter the "Consumer key" received in Email.

.. image:: https://web-resource.allip.io/github/allip_digits_2f_authentication/media/DigitsAuthenticationEndUser9.jpg
   :align: center
   :width: 700

2FA Settings:
=============

:menuselection:`Admin Priviledge`
---------------------------------

-  Select User from Users List
-  Go to "Preferences" tab
-  Enable 2FA login 

.. image:: https://web-resource.allip.io/github/allip_digits_2f_authentication/media/userlist.png
   :align: center  
    :width: 700
  
|

.. image:: https://web-resource.allip.io/github/allip_digits_2f_authentication/media/user_2fa_setting.png
   :align: center  
   :width: 700

|
-  NOTE: User needs to have their mobile number present in their [All apps] -> Contacts -> [Contact] page.


:menuselection:`User Priviledge`
--------------------------------

-  Go to "Preferences" from top right user menu.

.. image:: https://web-resource.allip.io/github/allip_digits_2f_authentication/media/user_preferences.png
   :align: center
   :width: 700

|
-  Enable 2FA Login

.. image:: https://web-resource.allip.io/github/allip_digits_2f_authentication/media/user_preferences_settings.png
   :align: center
   :width: 700

|
-  NOTE: User needs to have their mobile number present in their [All apps] -> Contacts -> [Contact] page.

.. image:: https://web-resource.allip.io/github/allip_digits_2f_authentication/media/DigitsAuthenticationEndUser12.jpg
   :align: center
   :width: 700

|

Login Steps for Users:
======================

:menuselection:`Login Steps`
----------------------------

-  Provide a valid login and password

.. image:: https://web-resource.allip.io/github/allip_digits_2f_authentication/media/odoo_login.png
   :align: center
   :width: 700

|

-  Verify mobile number and click on "Send Confirmation Code"

.. image:: https://web-resource.allip.io/github/allip_digits_2f_authentication/media/digit_confirm_code.png
   :align: center
   :width: 700

|

-  User will get a Confirmation code on registered mobile number

.. image:: https://web-resource.allip.io/github/allip_digits_2f_authentication/media/digit_code_on_mobile.jpg
   :align: center
    :width: 700
  
|
   
-  Enter code and click continue

.. image:: https://web-resource.allip.io/github/allip_digits_2f_authentication/media/digit_code.png
   :align: center
   :width: 700

|