import random
import pyotp
import qrcode 



#             client = Client(account_sid, auth_token)

print(key)
# totp = pyotp.TOTP(key)

# print(totp.now())

name = input("What's your name? ")

# uri = pyotp.totp.TOTP(key).provisioning_uri(
#     name = name,
#     issuer_name="Mindstream Journal"
# )

uri = pyotp.hotp.HOTP(key).provisioning_uri(
    name = name,
    issuer_name="Mindstream Journal"

)

print(f"URI: {uri}")


qr= qrcode.make(uri).save(f"static/images/qrcodes/{name}.png")
print("")

hotp = pyotp.HOTP(key)


counter= 0

while True:
    print(f"Initial_count: {hotp.initial_count}")
    print(f"OTP at Initial_count : {hotp.at(hotp.initial_count)}")
    
    print(hotp.verify(input("Enter code: "), counter=counter))

    counter += 1

'''505144
SIGN UP
1. On sign up
2. Set recovery question and answer
3. Create uri with email
4. Save uri to profile   // string
5. Generate QR code with uri and display to user for scanning
6. Request OTP 

LOGIN 
1. On login
2. Get email and password
3. Get recovery question's answer
4. Request OTP

FORGOT PASSWORD
1. 



pip install django-storages
pip install boto3





'''