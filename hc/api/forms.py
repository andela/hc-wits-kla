from django import forms


class TeamMemberForm(forms.Form):
    member_id = forms.IntegerField(required=True)