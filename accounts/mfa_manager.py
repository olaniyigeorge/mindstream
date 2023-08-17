import pyotp
import random
import qrcode 

#TODO Rewrite to use Class CustomThreeLayerMFA() which takes in a user, saves the layer reached 
# and when last MFA was tried, is_valid to verify if user has passed the three layers and the 
#various layers as methods


class CustomeThreeLayerMFA():

    def is_valid(self):
        pass

    def recovery_question_layer(self):
        pass

    def OTP_layer(self):
        pass





def make_uri(name, key=pyotp.random_base32()):
    '''
    This function takes the user's email and makes an authentication 
    uri with it.
    '''

    uri = pyotp.hotp.HOTP(key).provisioning_uri(
        name = name,
        issuer_name="Mindstream Journal"
    )

    print(uri)
    

    return (uri, key)
    

def make_qrcode_from_uri(uri, filename):
    qrcodes_save_path = "static/images/qrcodes/"
    try:
        qr= qrcode.make(uri)
        qr.save(f"{qrcodes_save_path}{filename}.png")
        status = True
    except:
        #raise ValueError("Couldn't make or save qrcode")
        status = False
    
    filepath= f"{qrcodes_save_path}{filename}.png"
    print(f"QRcode created in '{filepath}'")
    
    return (status, filepath)


def get_key_from_uri(uri):
    for x in uri:
        if x == "=":
            key= uri[(uri.index(x)+1):(uri.index(x)+33)]
            return key
        


def verify_otp(key, code, counter):
    hotp = pyotp.HOTP(key)
    
    return hotp.verify(code, counter=counter)




def get_otp(key, counter):

    hotp = pyotp.HOTP(key)

    otp = print(f"OTP at {counter}: {hotp.at(int(counter))}")
    
    return otp