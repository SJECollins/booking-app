from django.db import models


BOOKING_TIME = (
    (300, "3:00 PM"),
    (330, "3:30 PM"),
    (400, "4:00 PM"),
    (430, "4:30 PM"),
    (500, "5:00 PM"),
    (530, "5:30 PM"),
    (600, "6:00 PM"),
    (630, "6:30 PM"),
    (700, "7:00 PM"),
    (730, "7:30 PM"),
    (800, "8:00 PM"),
    (830, "8:30 PM"),
    (900, "9:00 PM"),
    (930, "9:30 PM"),
)

class Table(models.Model):
    customer_name = models.CharField(max_length=50)
    customer_email = models.EmailField()
    customer_mobile = models.CharField(max_length=20)
    table_number = models.CharField(max_length=10, blank=True, null=True)
    date = models.DateField()
    time = models.IntegerField(choices=BOOKING_TIME)
    party_number = models.PositiveIntegerField()
    dietary_requirements = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.customer_name + " table: " + str(self.table_number) + " on " + str(self.date) + " at " + str(self.get_time_display()) + " for " + str(self.party_number)