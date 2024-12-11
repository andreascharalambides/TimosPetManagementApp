from django import forms
from .models import Pet, Task, Category
from django.forms import DateTimeInput


class PetForm(forms.ModelForm):
    photo = forms.ImageField(required=False)

    class Meta:
        model = Pet
        fields = ['name', 'dob', 'breed', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'breed': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control-file'}),
        }
        labels = {
            "dob": "Birthdate",
        }

    def __init__(self, *args, **kwargs):
        super(PetForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label_suffix = ""


class TaskForm(forms.ModelForm):
    DAYS_OF_WEEK = Task.DAYS_OF_WEEK

    frequently = forms.MultipleChoiceField(
        choices=DAYS_OF_WEEK,
        widget=forms.CheckboxSelectMultiple,
        label="Repeat Every",
        required=False,
    )
    new_category = forms.CharField(
        max_length=100,
        required=False,
        help_text="Add a new category if needed.",
        label="Or create a new type",
        widget=forms.TextInput(attrs={"placeholder": "New task name..."}),
    )

    class Meta:
        model = Task
        fields = [
            'pet', 'category', 'new_category', 'comments', 'data',
            'start_date', 'frequently', 'end_date', 'important'
        ]
        widgets = {
            'start_date': DateTimeInput(attrs={"type": "datetime-local"}),
            'end_date': DateTimeInput(attrs={"type": "date"}),
            'comments': forms.Textarea(attrs={"rows": 3, "placeholder": "Additional comments..."}),
            'data': forms.TextInput(attrs={"placeholder": "Task information..."}),
        }
        labels = {
            "category": "Task Type",
            "start_date": "Starts At",
            "end_date": "Ends On (optional)",
            "frequently": "Repeats Every",
            "important": "Is Important",
            "data": "Information (optional)"
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TaskForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.label_suffix = ""

        if user:
            self.fields['pet'].queryset = Pet.objects.filter(user=user)
            self.fields['category'].queryset = Category.objects.filter(user=user)
        else:
            self.fields['pet'].queryset = Pet.objects.none()
            self.fields['category'].queryset = Category.objects.none()

        self.fields['end_date'].required = False
        self.fields['data'].required = False

        self.fields['category'].empty_label = None

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get("category")
        new_category = cleaned_data.get("new_category")

        if category == "--new-type--" and not new_category:
            self.add_error("new_category", "Please provide a name for the new category.")
        elif not category and not new_category:
            raise forms.ValidationError("Please select a category or enter a new category.")

        return cleaned_data