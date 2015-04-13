from django import forms
from mainSite.models import Comments

class CommentForm(forms.ModelForm):

	class Meta:
		model = Comments
		exclude = ('author','likes')
		widgets = {"content":forms.TextInput(attrs={'size':140})}

