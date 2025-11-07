from django import forms
from .models import MarketingJob, Proposal, Category


class JobForm(forms.ModelForm):
    class Meta:
        model = MarketingJob
        fields = [
            'title', 'description', 'category', 'budget_min', 'budget_max',
            'tags', 'location', 'status'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'm-input', 'placeholder': 'e.g. Social media ad campaign'}),
            'description': forms.Textarea(attrs={'class': 'm-textarea', 'rows': 6, 'placeholder': 'Describe the work…'}),
            'category': forms.Select(attrs={'class': 'm-select'}),
            'budget_min': forms.NumberInput(attrs={'class': 'm-input', 'step': '0.01'}),
            'budget_max': forms.NumberInput(attrs={'class': 'm-input', 'step': '0.01'}),
            'tags': forms.TextInput(attrs={'class': 'm-input', 'placeholder': 'web, seo, logo'}),
            'location': forms.TextInput(attrs={'class': 'm-input', 'placeholder': 'Remote / City'}),
            'status': forms.Select(attrs={'class': 'm-select'}),
        }


class ProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = ['message', 'price', 'eta_days']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'm-textarea', 'rows': 4, 'placeholder': 'Why are you a good fit?'}),
            'price': forms.NumberInput(attrs={'class': 'm-input', 'step': '0.01'}),
            'eta_days': forms.NumberInput(attrs={'class': 'm-input', 'min': 1}),
        }


