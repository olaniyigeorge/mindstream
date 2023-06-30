from django.shortcuts import render

from django.contrib.auth.decorators import login_required
# Create your views here.




def index(request):

    return render(request, 'journal/index.html')



@login_required(login_url="accounts/login")
def home(request):
    entries = ["This is my first entry", 
               "I'm here again for the second time to write down my thoughts",
                "This is my third entry"]
    
    return render(request, 'journal/home.html', {'entries': entries})



def day(request):
    '''
    This view returns the entries in a day, returns an error(empty) page if there is no entry 
    for the specified date and an error(invalid date format page if the date url format is invalid).
    '''
    return render(request, 'journal/daypage.html')


def archive(request, filter_on='months'):
    '''
    This view returns a calender page(filtered by months by default) where users can click on a day
    and be taken to that date's entry page.
    '''
    return render(request, 'journal/archive_filter.html')


def create_entry(request):
    '''
    On GET: This view returns the entry form page on get
    On POST: calls the validate_entry(entry), if valid, calls parse_entry(entry) then save entry.

    '''
    pass


def delete(request, entry_id):
    '''
    Get the entry with the entry_id 
    if entry exists
        check if auth'd user is the entry author
        if yes:
            delete entry
            redirect home
        if not:
            if request.user.is_auth'd:
                logout
            return MFA error page with "You are trying to delete another user's entry" message 
    '''
    pass
