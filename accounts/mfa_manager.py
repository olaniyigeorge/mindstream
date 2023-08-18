import pyotp
import qrcode 




def make_uri(name, key=pyotp.random_base32()):
    '''
    This function takes the user's email and makes an authentication 
    uri with it.
    '''

    uri = pyotp.hotp.HOTP(key).provisioning_uri(
        name = name,
        issuer_name="Mindstream Journal"
    )

    # print(uri)
    

    return (uri, key)
    

def make_qrcode_from_uri(uri, filename):
    qrcodes_save_path = "static/images/qrcodes/"
    try:
        qr= qrcode.make(uri)
        qr.save(f"{qrcodes_save_path}{filename}.png")
        return True
    except:
        #raise ValueError("Couldn't make or save qrcode")
        return False
    
    # filepath= f"{qrcodes_save_path}{filename}.png"
    # print(f"QRcode created in '{filepath}'")
    
    

def get_key_from_uri(uri):
    for x in uri:
        if x == "=":
            key= uri[(uri.index(x)+1):(uri.index(x)+33)]
            return key
        


def verify_otp(key, code, counter, error_margin=6):
    '''
    This function verifies that the otp provided is correct.
    There is a catch tho. It has a margin of error for cases where users have 
    mistakenly refreshed the generated otp.
    THIS FUCNTION WILL RETURN TRUE ONLY IF THE USER HASN'T MISTAKENLY REFRESHED AN 
    UNUSED OTP CODE MORE THAN SIX TIMES(30SEC0NDS)  '''
    hotp = pyotp.HOTP(key)
    
    
    options = []
    count = counter
    for x in range(error_margin):
        option = hotp.at(count+x)
        options.append(option)
        print(option)

    return code in options
    #return hotp.verify(code, counter=counter)




def get_otp(key, counter):

    hotp = pyotp.HOTP(key)

    otp = f"OTP at {counter}: {hotp.at(int(counter))}"
    
    return otp