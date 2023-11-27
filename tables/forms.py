from operator import itemgetter
from django import forms
from django.forms import ModelForm
from .models import Table
from .tables_details import TABLES, DURATION


class DateInput(forms.DateInput):
    input_type = "date"


class TableForm(ModelForm):
    class Meta:
        model = Table
        fields = [
            "customer_name",
            "customer_email",
            "customer_mobile",
            "table_number",
            "date",
            "time",
            "party_number",
            "dietary_requirements",
        ]
        labels = {
            "customer_name": "Name",
            "customer_email": "Email",
            "customer_mobile": "Mobile",
            "date": "Date",
            "time": "Time",
            "party_number": "Party Number",
            "dietary_requirements": "Dietary Requirements",
        }
        widgets = {
            "customer_name": forms.TextInput(
                attrs={
                    "placeholder": "Name",
                    "class": "border border-gray-700 rounded-md p-1",
                }
            ),
            "customer_email": forms.EmailInput(
                attrs={
                    "placeholder": "Email",
                    "class": "border border-gray-700 rounded-md p-1",
                }
            ),
            "customer_mobile": forms.TextInput(
                attrs={
                    "placeholder": "Mobile",
                    "class": "border border-gray-700 rounded-md p-1",
                }
            ),
            "party_number": forms.NumberInput(
                attrs={
                    "placeholder": "Party Number",
                    "class": "border border-gray-700 rounded-md p-1",
                }
            ),
            "dietary_requirements": forms.Textarea(
                attrs={
                    "placeholder": "Dietary Requirements",
                    "class": "border border-gray-700 rounded-md p-1",
                }
            ),
            "date": DateInput(attrs={"class": "border border-gray-700 rounded-md p-1"}),
            "time": forms.Select(
                attrs={"class": "border border-gray-700 rounded-md p-1"}
            ),
            "table_number": forms.HiddenInput(),
        }

    def clean_customer_mobile(self):
        customer_mobile = self.cleaned_data.get("customer_mobile")

        if len(customer_mobile) < 10 or len(customer_mobile) > 13:
            raise forms.ValidationError("Please enter a valid Irish mobile number.")

        if customer_mobile[0] == "+":
            if not customer_mobile[1:].isnumeric():
                raise forms.ValidationError("Please enter a valid Irish mobile number.")
        elif not customer_mobile.isnumeric():
            raise forms.ValidationError("Please enter a valid Irish mobile number.")

        if customer_mobile[:4] == "+353":
            customer_mobile = customer_mobile.replace("+353", "0")
        elif customer_mobile[0] == "0":
            pass
        else:
            raise forms.ValidationError("Please enter a valid Irish mobile number.")

        return customer_mobile

    def clean(self):
        cleaned_data = self.cleaned_data
        date = cleaned_data.get("date")
        time = int(cleaned_data.get("time"))
        party_number = int(cleaned_data.get("party_number"))

        available_tables = []

        for table in TABLES:
            if table["capacity"] >= party_number:
                if not Table.objects.filter(
                    date=date,
                    time__range=[time - DURATION, time + DURATION],
                    table_number=table["number"],
                ).exists():
                    available_tables.append(table)

        if len(available_tables) == 0:
            raise forms.ValidationError(
                "Sorry, there are no tables available for that date and time."
            )

        lowest_table = min(available_tables, key=itemgetter("capacity"))
        cleaned_data["table_number"] = lowest_table["number"]
        cleaned_data["time"] = time
        return cleaned_data
