from django.db import models

from accounts.models import UserProfile
# Create your models here.



class Entry(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="user_entries" )
    text = models.TextField()
    created_at = models.DateTimeField(null=True,auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.text[:10]}..."
    
    def get_date(self):
        # Return the entry date in the format "June 22nd, 2023"
        return f"{str(self.created_at.date)}"

    def get_time(self):
        # Return the entry time in the format "20:25:54"
        return f"{str(self.created_at.time)}"
    
    


class Tag(models.Model):
    text = models.CharField(max_length=30)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name='entry_tags')

    def __str__(self) -> str:
        return f"{self.title}"
    

    def get_entries(self) -> list:
        '''
        Returns a list of entries that have this tag on 
        '''
        entries = []
        for entry in self.entries:
            entries.append(entry)

        return entries

