# Mindstream 

[mindstream-journal.onrender.com](https://mindstream-journal.onrender.com)

Mindstream is a journal web app that allows users to securely document their thoughts, and create meory stamps(Tags) that allow easy and faster recollection of their train of thought.


### **Features**
Mindstream includes features like;
- user authentication: This allows user to securely gain acces to their journal
- entry creation and deletion: This allows users to create timestamped entries at anytime and delete entries they want to.
- Multi Factor Authentication: This further secures user account and data from data leakage and bad actors by utilising the three factors of authentication; possession, knowledge and inherent factors.

### **MFA Security**
Built with the Django web framework, Mindstream also uses a 3-layer Multi Factor Authentication system built in to ensure user account security and prevent data leakage. This method utilizes the three factors of authentication; possession(OTP), knowledge(password) and inherent factors(recovery question).

- Password Layer(knowledge factor): Users are required to input their password every time they attempt logging into their journal.
- Recovery Question Layer(inherent factor): After passing the first layer, users are redirected to this layer to provide the answer to a recovery question they picked upon registeration.
- One Time Password(OTP) Layer(Possession Factor): Upon passing the second layer, an OTP code is sent to the user's mobile number(which they must have provided on signup). Users are required to input the exact code to finally gain access into their account.

This security system is to demostrate the use of a MFA security system to avoid data leakage, the importance/strengths of this system in securing sensitive data(in this case personal information) and of course, its weaknesses. 



## How to run locally/contribute

1. Clone the repo using `git clone https://github.com/olaniyigeorge/mindstream.git`
2. Create a virtual environment in the cloned repo's directory with `python -m venv env`
3. Activate the virtual environment `env\Scripts\activate`
4. Install the dependencies `pip install -r requirements.txt`
5. Run `python manage.py makemigrations` then `python manage.py migrate` to setup the database
6. Run the server from the command line(in the project directory) with `python manage.py runserver`
7. Lastly, navigate to `http://127.0.0.1:8000/` in your web browser 