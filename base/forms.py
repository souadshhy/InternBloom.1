from django import forms
from .models import Apps, Position

class AppsForm(forms.ModelForm):
    class Meta:
        model = Apps
        fields = ['student', 'company', 'position', 'appStatus']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 1) start with an EMPTY queryset for positions
        #    (the user hasn't chosen a company yet)
        self.fields['position'].queryset = Position.objects.none()

        # 2) nice placeholder for the empty select
        self.fields['position'].empty_label = "---------"

        # 3) render Position and AppStatus as disabled on first paint.
        #    (we will enable them with JS after a company is selected)
        self.fields['position'].widget.attrs['disabled'] = True
        self.fields['appStatus'].widget.attrs['disabled'] = True

    def clean(self):
        """
        Cross-field validation so nobody can submit a position that
        doesn't belong to the selected company (security!).
        """
        cleaned = super().clean()
        company = cleaned.get('company')
        position = cleaned.get('position')

        if company and position and position.company_id != company.id:
            self.add_error('position', 'Selected position does not belong to the chosen company.')
        return cleaned
