from django.shortcuts import render

from .models import Entry
from accounts.models import User, UserProfile
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import AddEntryForm
import datetime

# Create your views here.

months = ['January', 'February', 'March', 'April',
          'May', 'June', 'July',
          'August', 'September', 'October',
          'November', 'December']




def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("journal:home"))

    now = datetime.datetime.now()
    day= now.day
    month = months[now.month - 1] 
    year = now.year

    return render(request, 'journal/index.html', {'day': day, 'month': month, 'year':year})

def filter_entries(author=None, date=None, query=None) -> list:
    '''
    This function takes an entry author and a date and returns 
    a list of entries by that author on that date
    '''
    try:
        authors_entries = Entry.objects.filter(author=author)
    except:
        TypeError("Couldn't filter entries. Author probably not valid")
    
    # Filter with query
    if query is not None:
        search_result = []
        for entry in authors_entries:
            #print(query.lower(), '--', entry.text.lower() )
            if query.lower() in entry.text.lower():
                #print("passed")
                search_result.append(entry)
                #print(entry.text)
        return search_result
        
    # Filter with date
    if date is not None:
        this_days_entries =[]
        for entry in authors_entries:
            if str(entry.created_at.date())== str(date):
                this_days_entries.append(entry)

        return this_days_entries



@login_required(login_url="accounts/login")
def home(request):
    """entries = ["This is my first entry", 
               "I'm here again for the second time to write down my thoughts",
                "This is my third entry"]"""
    
    #TODO Change timezone (+1)
    today_datetime = datetime.datetime.today()

    # Get auth'd user and their profile
    userprofile = UserProfile.objects.get(user=request.user)


    #TODO How django represent dates in db.sqlite3
    #TODO How to filter a model by date 

    # Filter out today's entries
    todays_entries = filter_entries(userprofile, today_datetime.date())
    
    return render(request, 'journal/home.html', {'entries': todays_entries, "today_datetime": today_datetime})

def create_entry(request):
    '''
    On GET: This view returns the entry form page on get
    On POST: calls the validate_entry(entry), if valid, calls parse_entry(entry) then save entry.

    '''
    if request.method == "POST":
        # Get authenticated user
        user = request.user

        # Get user's profile
        userprofile = UserProfile.objects.get(user=user)

        # Get submited entry text
        entry_text = request.POST['entry_text']

        # Create new entry instance
        new_entry = Entry.objects.create(author=userprofile, text=entry_text)

        # Save new entry instance
        new_entry.save()

        # Redirect back home
        return HttpResponseRedirect(reverse("journal:home"))

        '''
        submitted_form = AddEntryForm(request.POST)

        if submitted_form.is_valid():
            # Get authenticated user
            user = request.user

            # Create and save entry
            entry_text = submitted_form.cleaned_data["entry_text"]

            # Create entry. Not specifiying the date with make the date datetime.datetime.now() so far t
            new_entry = Entry.objects.create(author=user, text=entry_text)

            # Redirect back to home
        else:
            # If form sn't valid, redirect back to the create entry page and 
            # prepopulate the form with the invalid entry
            return HttpResponseRedirect(reverse("journal:create_entry"))
        
        pass
        '''
    
    add_entry_form = AddEntryForm()
    return render(request, "journal/create_entry.html", {'form': add_entry_form})


def day_view(request, year, month, day):
    '''
    This view returns the entries in a day, (TODO returns an empty page message if 
    there is no entry for the specified date and an error(invalid date format 
    page if the date url format is invalid).
    '''

    # Get entries for this day
    #days_entries = Entry.objects.filter(created_at.date=)

    # Check/validate date
    try:
        date = datetime.date(year,month,day)
    except:
        ValueError("Invalid date format")

    # Get auth'd user and their profile
    userprofile = UserProfile.objects.get(user=request.user)

    # Filter entries by author and date
    days_entries = filter_entries(userprofile, date)

    
    # Render daypage populated with entries for the specified date
    return render(request, 'journal/daypage.html', 
                                                    {"daysentries": days_entries, 
                                                    "day": day, 
                                                    "month":month, 
                                                    "year":year})

def search_archive(request):
    '''
    This view is used to collect date from users, check that it is 
    in the right format and redirect to the date's page
    #TODO Customize this funtion to work for text search too
    '''
    if request.method == "POST":
        if request.POST['query']:
            # Get query
            query = request.POST['query']
            # Get auth'd user and their profile
            userprofile = UserProfile.objects.get(user=request.user)
            # Filter entries by author and date
            entries = filter_entries(author=userprofile, query=query)

            return render(request, "journal/search-results.html", {"results":entries, "query": query})

            
        # Get submitted date
        date = request.POST['date']
        print(date)

        # Get today's date and Redirect home if the searched date is today
        today = datetime.date.today()
        if date == str(today):
            return HttpResponseRedirect(reverse("journal:index"))
        
        # Split date into year,month and day
        year, month, day = date.split('-')
        
        #TODO Rewrite to redirect to the date_page with the args in the right order
        return day_view(request, int(year), int(month), int(day))
        #HttpResponseRedirect(reverse("journal:day_view", args={f"{int(year)}/{int(month)}/{int(day)}"}))


def archive(request, filter_on='months'):
    '''
    This view returns a calender page(filtered by months by default) where users can click on a day
    and be taken to that date's entry page.
    '''
    return render(request, 'journal/archive_filter.html')



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
