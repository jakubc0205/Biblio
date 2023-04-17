from flask_wtf import FlaskForm 
from flask import flash
from wtforms import StringField, IntegerField, SubmitField, DateField
from wtforms.validators import DataRequired,ValidationError
from datetime import datetime, date   


def validate_date(form, field): 
    if not isinstance(field.data, date) :
        raise ValidationError("Blad" and flash("Podaj date w formacie: RRRR-MM-DD"))   
  

class SearchForm(FlaskForm):
   search = StringField('Tytul', [DataRequired()]) 
   search1 = StringField('Autor', [DataRequired()]) 
   search2 = StringField('Jezyk', [DataRequired()]) 
   search3 = DateField('Data Publikacji od roku :', [DataRequired()])  
   search4 = DateField('Data Publikacji do roku :', [DataRequired()]) 
   submit = SubmitField('Znajdz', render_kw={'class': 'btn btn-success btn-block'})


class AddForm(FlaskForm):

    tytul = StringField('Tytul') 
    autor = StringField('Autor')   
    data_pub = DateField('Data publikacji',validators=[DataRequired(),validate_date])             
    ISBN_num = IntegerField('ISBN:')  
    liczba_stron = IntegerField('Liczba stron :')  
    okladka = StringField('link do okladki :')  
    jezyk = StringField('Jezyk :')  
    submit = SubmitField('Dodaj', render_kw={'class': 'btn btn-success btn-block'})   
  
class ChangeForm(FlaskForm):
     
    id1 = IntegerField('Podaj ID ksiazki do zmiany') 
    tytul = StringField('Tytul') 
    autor = StringField('Autor') 
    data_pub = DateField('Data publikacji') 
    ISBN_num = IntegerField('ISBN:')  
    liczba_stron = IntegerField('Liczba stron :')   
    okladka = StringField('Podaj link do okladki :')  
    jezyk = StringField('Jezyk :')  
    submit = SubmitField('Edytuj', render_kw={'class': 'btn btn-success btn-block'})  


class DelForm(FlaskForm):

    id = IntegerField('Podaj ID ksiazki do usuniecia:')
    submit = SubmitField('Usun', render_kw={'class': 'btn btn-success btn-block'})
 
class ImportForm(FlaskForm):
     
    tytul = StringField('Tytul') 
    autor = StringField('Autor')  
    api = StringField('Podaj swoj klucz API, aby importowac ksiazke',[DataRequired()])
    submit = SubmitField('Dodaj', render_kw={'class': 'btn btn-success btn-block'})