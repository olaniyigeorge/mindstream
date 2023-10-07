import random
from twilio.rest import Client

# class Sup():

#     def save(self, *args, **kwargs):
#             account_sid = 'AC605add792b30fbb291ce5699e84854d7'
#             auth_token = '45b66a19ccf83ff52aec6a3bceee06a6'

#             client = Client(account_sid, auth_token)

#             validation_request = client.validation_requests \
#                             .create(
#                                     friendly_name=f'User{self.owner.pk}',
#                                     phone_number=f"{self.owner.profile.phone_number}"
#                                 )

#             print(validation_request.friendly_name)

#             message = client.messages.create(
#                 body= f"MINDSTREAM: Verification code for {self.owner.email} your journal {self.code}",
#                 from_="+12187182316",
#                 to= f"{self.owner.profile.phone_number}"
#             )

#             print(message.sid)

#             return super().save(*args, **kwargs)





# account_sid = 'AC605add792b30fbb291ce5699e84854d7'
# auth_token = '45b66a19ccf83ff52aec6a3bceee06a6'

# client = Client(account_sid, auth_token)

# code = random.randint(100000, 999999)
# email = "olaniyigeorge77@gmail.com"
# phone_number = "+2348051410673"


# message = client.messages.create(
#     body= f"MINDSTREAM: Verification code for {email} your journal {code}",
#     from_="+12187182316",
#     to= phone_number
# )

# print(message)
# print(message.sid)



