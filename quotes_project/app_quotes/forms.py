from django.forms import ModelForm, CharField, TextInput, DateField, Field, ModelChoiceField, Textarea, \
    ModelMultipleChoiceField
from .models import Tag, Quote, Author


class TagForm(ModelForm):
    tag = CharField(min_length=3, max_length=20, required=True, widget=TextInput())

    class Meta:
        model = Tag
        fields = ['tag']


class AuthorForm(ModelForm):
    fullname = CharField(max_length=255, required=True, widget=TextInput())
    born_date = DateField(required=True, widget=TextInput())
    born_location = CharField(max_length=255, required=True, widget=TextInput())
    description = Field(required=True, widget=TextInput())

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']


class QuoteForm(ModelForm):
    quote = CharField(max_length=1500,
                      required=True,
                      widget=Textarea())
    author = ModelChoiceField(queryset=Author.objects.all(), required=True)
    tags = ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)

    class Meta:
        model = Quote
        fields = ['quote', 'author', 'tags']

