# LoginOTP

Login implementation made using Django. For verifying users, OTP is sent to their phone numbers at the time of registeration. Since a free version of Twilio API is used, only phone numbers manually added in the Twilio Dashboard have the capability to recieve OTP.


Make sure to replace ACCOUNT SID, AUTH TOKEN and PHONE NUMBER in views.py with your Twilio details when running the code.
