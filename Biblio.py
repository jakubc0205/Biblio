import datetime
import json
import os
import unittest
from unittest import result

import pandas as pd
import requests
from dateutil.parser import parse
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_migrate import Migrate
from flask_msearch import Search
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import update

from forms import AddForm, ChangeForm, DelForm, ImportForm, SearchForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

basedir = os.path.abspath(os.path.dirname(__file__)) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  
app.config['MSEARCH_INDEX_NAME'] = 'msearch' 
app.config['MSEARCH_PRIMARY_KEY'] = 'id'   
app.config['MSEARCH_ENABLE'] = True


db = SQLAlchemy(app)
Migrate(app,db) 

search = Search(db=db)
search.init_app(app) 

class Ksiazka(db.Model):

    __tablename__ = 'Ksiazka' 
    id = db.Column(db.Integer,primary_key = True)
    tytul = db.Column(db.Text, nullable=True) 
    autor = db.Column(db.Text, nullable=True) 
    data_pub = db.Column(db.Date, nullable=True) 
    ISBN_num = db.Column(db.Integer, nullable=True)
    liczba_stron = db.Column(db.Integer, nullable=True)  
    okladka = db.Column(db.Text, nullable=True)  
    jezyk = db.Column(db.Text, nullable=True)  

    def __init__(self,tytul,autor,data_pub,ISBN_num,liczba_stron,okladka,jezyk):  
        self.tytul = tytul  
        self.autor = autor 
        self.data_pub = data_pub 
        self.ISBN_num = ISBN_num 
        self.liczba_stron = liczba_stron 
        self.okladka = okladka 
        self.jezyk = jezyk

@app.route('/')
def index():
    return render_template('home.html')   
         
@app.route('/add', methods=['GET', 'POST'])
def add(): 

    form = AddForm()
    if form.validate_on_submit():
        tytul = form.tytul.data
        autor = form.autor.data  
        data_pub = form.data_pub.data 
        ISBN_num = form.ISBN_num.data
        liczba_stron = form.liczba_stron.data
        okladka = form.okladka.data
        jezyk = form.jezyk.data 
        new_book = Ksiazka(tytul,autor,data_pub,ISBN_num,liczba_stron,okladka,jezyk)
        db.session.add(new_book)
        db.session.commit()     
              
        return redirect(url_for('list_and_search'))  
    elif not form.validate_on_submit() :   
        flash("Podaj date w formacie: RRRR-MM-DD; Numer ISDB oraz liczbe stron jako liczbe calkowita")

    return render_template('add.html',form=form) 
    
@app.route('/edytuj', methods=['GET', 'POST'])
def edytuj():

    form = ChangeForm()  
    id2 = form.id1.data
    edited_book = Ksiazka.query.get(id2)  
    if form.validate_on_submit():   
        
        edited_book.tytul = form.tytul.data
        edited_book.autor = form.autor.data  
        edited_book.data_pub = form.data_pub.data 
        edited_book.ISBN_num = form.ISBN_num.data
        edited_book.liczba_stron = form.liczba_stron.data
        edited_book.okladka = form.okladka.data
        edited_book.jezyk = form.jezyk.data 
        db.session.commit()     

        return redirect(url_for('list_and_search'))  
    elif not form.validate_on_submit() :   
        flash("Podaj date w formacie: RRRR-MM-DD; Numer ISDB oraz liczbe stron jako liczbe calkowita")       

    return render_template('edytuj.html',form=form) 


@app.route('/search_list_combined', methods=['GET', 'POST']) 
def list_and_search(): 

    form = SearchForm() 

    if form.validate_on_submit(): 
        tag = form.search.data  
        tag1 = form.search1.data 
        tag2 = form.search2.data 
        tag3 = form.search3.data 
        tag4 = form.search4.data
        search_term = "%{}%".format(tag) 
        search_term1 = "%{}%".format(tag1)  
        search_term2 = "%{}%".format(tag2) 
        search_term3 = "%{}%".format(tag3)  
        search_term4 = "%{}%".format(tag4)
        results = Ksiazka.query.filter(Ksiazka.tytul.like(search_term)|Ksiazka.autor.like(search_term1)|Ksiazka.jezyk.like(search_term2)|Ksiazka.data_pub.between(tag3, tag4)).all()
        return render_template('search_list_combined.html', form=form, results=results)  
    else:    
        ksiazki = Ksiazka.query.all()
        return render_template('search_list_combined.html', ksiazki=ksiazki, form=form)  

@app.route('/import1', methods=['GET', 'POST'])
def import1(): 

    form = ImportForm()  

    if form.validate_on_submit():
        my_api_key = form.api.data
        intitle = form.tytul.data
        inauthor = form.autor.data
        url = 'https://www.googleapis.com/books/v1/volumes'
        query = f"intitle:{intitle} inauthor:{inauthor}"
        params = {
                    'q': query,
                    'key': my_api_key,
                }
        res = requests.get(url, params = params)
        data =  json.loads(res.content)
        data1= pd.DataFrame(data["items"])["volumeInfo"].head(1) 
        for x in data1: 
            tytul = str(x["title"])
            autor = str(x["authors"][0])
            data_pub = parse(x["publishedDate"], default=datetime.datetime(2011, 1, 1))
            ISBN_num = int(x["industryIdentifiers"][1]["identifier"])
            liczba_stron = int(x["pageCount"])
            okladka = str(x["imageLinks"]["smallThumbnail"])
            jezyk = str(x["language"])
        new_book = Ksiazka(tytul,autor,data_pub,ISBN_num,liczba_stron,okladka,jezyk)
        db.session.add(new_book)
        db.session.commit()        
        return redirect(url_for('list_and_search'))
    return render_template('import1.html',form=form)   

    

@app.route('/delete', methods=['GET', 'POST'])
def del_pup():

    form = DelForm() 
    
    if form.validate_on_submit():    
        id5 = form.id.data
        Ksiazka.query.filter(Ksiazka.id == id5).delete()
        db.session.commit()

        return redirect(url_for('list_and_search'))
    return render_template('delete.html',form=form) 

if __name__ == '__main__':
    app.run(debug=True) 

unittest.main()

 