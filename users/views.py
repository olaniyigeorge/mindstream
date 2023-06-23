from django.shortcuts import render

# Create your views here.

def profile(request):
    pass


def signup(request):
    '''

    On Get
    Serves email/password form 
    
    On Post
    if form is valid:
        create user and set is verified to false by default
        redirect to login page populate the email field 
    
    '''

    pass

def edit_mfa_layers(request):
    '''

    On Get
    Render mfa-form page
    
    On Post
    if form is valid:
        edit/set recovery_question, answer and OTP Device
        set user.is_verified to True
        redirect to login page populate the email field 
    
    '''

    pass


def login(request):
    '''

    On Get
    Serves email/password form 
    
    On post
    ....if user.email not in database:
        return render signup page and populate the email field with the provided email

    ....if not authenticate(user):
            redirect login with invalid password error

    ....if not user.is_verified:
            redirect to recovery_question and otp device form page

    ....if not user.mfa:
            login(user)
            redirect home

        else:
            authenticate(user)
            get(user_id)
            render email recovery page with user_id in session
            ...request.session['user_id'] = user_id
        
    '''

    pass


def confirm_recovery_question(request):
    '''
    if not request.session.get('user_id):
        redirect to login page with 

    userprofile =userprofile(user=user_id)
    


    ///

    On Get
    recovery_question =userprofile(user=user_id).recovery_question
    ....return render recovery question with question in context
    
    On post

    ....if request.POST[answer] = userprofile.recovery.answer
            redirect to OTP page with user_id in session
            ...request.session['user_id'] = user_id

    ....else:
            return render mfa error page with "MFA failed" message

    '''
    pass



def confirm_otp(request):
    '''
    if not request.session.get('otp_user_id):
        redirect to login page

    userprofile =userprofile(user=user_id)



    ///

    On Get
    ....Display recovery question
    ....Serve input field for form

    
    On post

    TODO How to send OTP to phone number
    
    ....if request.POST[OTP] checks out:
            login(user)
            redirect to journal home

    ....else:
            return render mfa error page with "MFA failed" message

    '''
    pass

def logout(request):
    pass