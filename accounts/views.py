from django.shortcuts import render

from .models import User, UserProfile, OTPCode
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .forms import SignUpForm, SetUpMFAForm
import random

# Create your views here.


def profile(request):
    '''  Returns the authenticated user's profile page  '''

    return render(request, "accounts/profile.html")

def signup(request):
    '''
    Serve the signup form then get redirected to setmfa 
    page to fill in the details required to set up MFA
    '''
    if request.method == 'POST':
        # Get the values of the SignUp form in order
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            #Do stuff if the form is valid
            
            # Saves a new user object from the  form's data 
            user = form.save()

            # Save user  --- THIS LINE CREATES A USER, WHICH TRRIGGERS THE SIGNAL TO CREATE A
            #                USERPROFILE(with all fields set to the default value) FOR THE USER
            user.save()

            # Try(in a case where fr some reason the user isnt created) to get the user ID
            try:
                submitted_email = form.cleaned_data.get('email')
                thisuser = User.objects.get(email = submitted_email)
            except:
                raise ValueError("Couldn't get user")
            

            # Save user id in session with key 'tupk(this user primary key)'
            request.session['tupk'] = thisuser.pk

            # Redirect to mfaform page to fill in the mfa details(question, answer and phone number)
            return HttpResponseRedirect(reverse("accounts:setmfa"))

        else:
            return render(request, "accounts/signup.html", {
                                    'form': form,
                                    'message': 'Form not valid'})

    # Serve the specially build signup form in forms.py
    signupform = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': signupform})

def setmfa(request):
    """
    Serves the setmfa form to get the details needed to setup MFA. 
    On POST, sets up MFA after verifying the provided details(especially phone numner) 
    by saving this details in the user profile
    """
    pk = request.session['tupk']

    if request.method == "POST":
        # Bind the submitted data to a SetUPMFAForm instance by populating 
        ## it with the data. This is done for validation purposes
        setupmfaform = SetUpMFAForm(request.POST)

        if setupmfaform.is_valid():
            # Get user
            user = User.objects.get(pk=pk)
            # Get UserPofile
            profile = UserProfile.objects.get(user=user)

            # Get the MFA data from the submitted form data
            question = setupmfaform.cleaned_data['recovery_question']
            answer = setupmfaform.cleaned_data['recovery_answer']
            phone_number = setupmfaform.cleaned_data['phone_number']

            # Set these data for the user
            profile.recovery_question = question
            profile.recovery_answer = answer

            # Save profile
            profile.save()


            # Save phone_number and user_id in sessions
            request.session['phone_number'] = str(phone_number)
            request.session['tupk'] = pk
            

            # Redirect to verify phone number page
            return HttpResponseRedirect(reverse("accounts:verify-phonenumber"))
        
        else:
            # Users are redirected back to restart the MFA setup process
            # TODO For now, the above is the normal behavior. But in a situation where the user doesn't 
            # TODO ...... the save primary key in their session (anymore), what should happen? 
            
            return HttpResponseRedirect(reverse("accounts:setmfa"))
        

    # GET: Serves the setmfa form
    setupmfaform = SetUpMFAForm()
    return render(request, 'accounts/setmfa.html', {'form':setupmfaform})

def verify_phonenumber(request):
    '''
    Users get this view to verify the phonenumber they submitted 
    upon setting up mfa after signup.
    '''
    # Get the user_id and phonenumber for the session
    user_pk = request.session["tupk"]
    phone_number = request.session["phone_number"]
    
    if request.method == "POST":
        # Get submitted OTP
        otp_code = request.POST['otp']
        
        # Get user
        user = User.objects.get(pk=user_pk)

        # Check if there exists an OTPcode in the database with this code and this user
        if OTPCode.objects.filter(code=otp_code, owner=user).exists():
            '''
            If the code exists for this user...
            Clean up pk from session, delete otpcode from db 
            then log user in
            '''
            # Get User's Profile
            userprofile = UserProfile.objects.get(user=user)

            # Set phone number and phone_number_verified to True
            userprofile.phone_number = phone_number
            userprofile.phone_number_verified = True

            userprofile.save()

            # Delete pk and phone_number from sessions
            if request.session['tupk']:
                del request.session['tupk']
            if request.session['phone_number']:
                del request.session['phone_number']


            # Delete OTPCode from db
            used_code = OTPCode.objects.get(code=otp_code, owner=user)    
            used_code.delete()

            # Log user in
            login(request, user)

            #Redirect to home page
            return HttpResponseRedirect(reverse("journal:home"))


    code = random.randint(100000, 999999)
    
    user = User.objects.get(pk=user_pk)

    # Create a OTPcode with this user as the user as the owner and save in database
    otpcode = OTPCode.objects.create(code=code, owner=user)
    otpcode.save()
    
    # Send OTP code 
    #TODO Send to phone_number
    print(phone_number)
    print(otpcode)

    return render(request, "accounts/verifyphonenumber.html")


def login_view(request):
    # Redirects to mfa view passing in 1 as an argument to 
    # route it to the first level of the MFA system
    return HttpResponseRedirect(reverse("accounts:mfa", args=(1,),))

def mfa(request, level):
    '''
    Implementation for the three levels of authentication.
    
    LEVEL 1: User is served the Email/Password form
    LEVEL 2: User is served the Recovery question to provide an answer
    LEVEL 3: User is served a simple form to provide the OTP sent to their phone number upon passing level
    
    '''

    if request.method == "POST":
        # Check current MFA security level
        level = request.POST['level']

        if level == "1":
            # Get returned email and password
            email = request.POST["email"]
            password = request.POST["password"]

            # Check returned email and password
            user = authenticate(request, email=email, password=password)

            # If the user email and password checks out
            if user:
                # Get user and save the user's id in session 
                user = User.objects.get(email = email)
                request.session['tupk'] = user.pk

                # Redirect to the second level of mfa
                return HttpResponseRedirect(reverse("accounts:mfa", args=(2,),))
            else:
                # If password  doesn't check out, redirect to login view which restarts the MFA process
                # TODO Delete pk from sessions first
                return HttpResponseRedirect(reverse("accounts:login_view"))
        
        if level == "2":
            '''
            Check if the recovery answer is correct  ---> 
            if correct, redirect to the third level
            '''
            # Get returned recovery question's answer 
            answer = request.POST["recovery_answer"]
            
            # Get user_id from session
            pk = request.session['tupk']

            # Use pk to get user, userprofile and user's recovery answer in extension
            user = User.objects.get(pk=pk)
            userprofile = UserProfile.objects.get(user=user)

            # Check if provided answer from form matches the user's recovery answer
            if userprofile.recovery_answer == answer:
                request.session['tupk'] = user.pk

                # Redirect to the third/last level of mfa
                return HttpResponseRedirect(reverse("accounts:mfa", args=(3,)))
            
            # If answer doesn't checkout, redirect to login view which restarts the MFA process
            else:
                # TODO Delete pk from sessions first
                return HttpResponseRedirect(reverse("accounts:login_view"))
            
        if level == "3":
            '''
            Check if the OTP is correct  ---> if correct, 
            log user in and redirect to journal's home page
            '''
            # Get returned recovery question's answer 
            otp_code = request.POST["otp"]
            
            # Get user_id from session and user it to get user
            pk = request.session['tupk']
            user = User.objects.get(pk=pk)

            # Check if there exists an OTPcode in the database with this code and this user
            if OTPCode.objects.filter(code=otp_code, owner=user).exists():
                '''
                If the code exists for this user...
                Clean up pk from session, delete otpcode from db 
                then log user in
                '''

                #TODO Delete pk from sessions
                if request.session['tupk']:
                    del request.session['tupk']

                # Delete OTPCode from db
                used_code = OTPCode.objects.get(code=otp_code, owner=user)    
                used_code.delete()


                # Log user in
                login(request, user)

                #Redirect to home page
                return HttpResponseRedirect(reverse("journal:home"))

            else:
                # If the code provided doesn't checkout(isn't in the database)

                #TODO Delete pk from 

                # Redirect user to the login_view to restart the MFA 
                # process from level one
                return HttpResponseRedirect(reverse("accounts:login_view"))

            

    if level == 1:
        # Serve the Email/Password form
        return render(request, "accounts/mfaone.html")
    if level == 2:
        '''
        Serve the Recovery question form 
        '''
        # Get user's profile from primary key in session
        pk = request.session["tupk"] 
        user = User.objects.get(pk=pk)
        profile = UserProfile.objects.get(user=user)
        # Get the user's recovery question 
        recovery_question = profile.recovery_question

        # Serve the form to get the answer passing in the question
        return render(request, "accounts/mfatwo.html", {'question': recovery_question}) 
    if level == 3:
        ''' 
        Send an OTP to the user's phone number then serve 
        a simple form to get the OTP back
        '''
        
        # Generate a random 6 digit code 
        code = random.randint(100000, 999999)

        # Get the user for the session
        user_id = request.session['tupk']
        user = User.objects.get(pk=user_id)

        # Create a OTPcode with this user as the user as the owner and save in database
        otpcode = OTPCode.objects.create(code=code, owner=user)
        otpcode.save()

        # TODO Send OTPcode to user's phone number
        # For now(before integrating Twillo we'll print the code
        print(code)


        # Serve form to get the OTPcode from the user 
        return render(request, "accounts/mfathree.html")


def logout_view(request):
    '''
    Log authenticated user out and redirect to journal index page
    '''
    # Log user out
    #TODO Read up on how the logout function works
    
    logout(request)

    # Redirect to journal index page
    return HttpResponseRedirect(reverse("journal:index"))




""" def editprofile(request):
    '''
    Serve the editprofile form on GET 
    Updates the user profile on POST
    '''
    
    # Try to get pk for session. redirect to login page 
    try:
        pk = request.session['pk']
    except:
        raise ValueError("You can't be on this page")
        # TODO return HttpResponseRedirect(reverse('accounts:login'))

    # if request.session[pk] is true, render the editprofile button

    if pk:
        return render(request, 'accounts/editprofile.html', {pk})

 """

