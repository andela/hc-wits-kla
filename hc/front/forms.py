from django import forms
from hc.api.models import Channel


class NameTagsForm(forms.Form):
    name = forms.CharField(max_length=100, required=False)
    tags = forms.CharField(max_length=500, required=False)

    def clean_tags(self):
        l = []

        for part in self.cleaned_data["tags"].split(" "):
            part = part.strip()
            if part != "":
                l.append(part)

        return " ".join(l)


class TimeoutForm(forms.Form):
    """
    Sets the timeout and grace periods of a check with minimum value of 1 minute (60 seconds) and maximum value of 1
    year (31536000 seconds).
    """
    timeout = forms.IntegerField(min_value=60, max_value=31536000)
    grace = forms.IntegerField(min_value=60, max_value=31536000)


class NagIntervalForm(forms.Form):
    """
    Sets the Nag Interview of a check with minimum value of 1 minutes (60 seconds) and maximum value of 1
    year (31536000 seconds).
    """
    nagging = forms.IntegerField(min_value=60, max_value=31536000)


class AddChannelForm(forms.ModelForm):

    class Meta:
        model = Channel
        fields = ['kind', 'value']

    def clean_value(self):
        value = self.cleaned_data["value"]
        return value.strip()


class AddWebhookForm(forms.Form):
    error_css_class = "has-error"

    value_down = forms.URLField(max_length=1000, required=False)
    value_up = forms.URLField(max_length=1000, required=False)

    def get_value(self):
        return "{value_down}\n{value_up}".format(**self.cleaned_data)
