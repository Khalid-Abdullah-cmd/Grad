from django.forms import inlineformset_factory
from .models import Program, Job

JobFormSet = inlineformset_factory(
    Program,
    Job,
    fields=['name'],
    extra=3,  # Show 3 blank job forms by default for flexibility
    can_delete=True  # Allow deleting jobs in both create and update views
)