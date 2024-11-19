from django.forms import Form, CharField, DateField, ModelChoiceField, Textarea, ModelForm, NumberInput

from viewer.models import Country, Creator


# pozor z ceho importuji!! zde importuji z django.form!!
# formular pro tvurce pomoci teto definice se nam automaticky vygeneruje formular.html

"""
class CreatorForm(Form):
    first_name = CharField(max_length=32, required=False)
    last_name = CharField(max_length=32, required=False)
    date_of_birth = DateField(required=False)
    date_of_death = DateField(required=False)
    nationality = ModelChoiceField(queryset=Country.objects, required=False)
    biography = CharField(widget=Textarea, required=False)
"""

class CreatorForm(ModelForm):

    class Meta:
        model = Creator   # odkazuje se do models.py na class Creator(Model)
        fields = '__all__'
        #fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death', 'biography']
        #exclude = ['nationality']

        help_texts = {
            'biography': "Zde zadejte biografii tvůrce."
        }
        error_messages = {
            # TODO
        }

    # first_name = CharField(max_length=32, required=False)
    # last_name = CharField(max_length=32, required=False)
    date_of_birth = DateField(required=False, widget=NumberInput(attrs={'type': 'date'}), label='Datum narození')
    date_of_death = DateField(required=False, widget=NumberInput(attrs={'type': 'date'}), label='Datum umrtí')
    # nationality = ModelChoiceField(queryset=Country.objects, required=False)
    # biography = CharField(widget=Textarea, required=False)