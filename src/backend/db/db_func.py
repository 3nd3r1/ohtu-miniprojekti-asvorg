import sys
sys.path.append("..")
from pymongo import MongoClient, errors
from pymongo.server_api import ServerApi
from backend.article_func import generate_cite_key, read_user_input_article, to_bibtex_article



def add_article_to_db(user, article):
    '''Add an article to the database'''
    uri = "mongodb+srv://testiuser:testisalasana123@ohtuminiprojekti-bibtex.19oezdh.mongodb.net/test?retryWrites=true&w=majority"

    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client["bibtex"]
    collection = db["articles"]
    article_dict = splice_article(article)
    cite_key = generate_cite_key(article_dict["author"], article_dict["year"])
    #add to database
    article_dict["user"] = user
    article_dict["cite_key"] = cite_key
    collection.insert_one(article_dict)


def splice_article(article): #article in bibtex format
    '''Splice the article to a dictionary'''
    article = article.split("\n")
    article = article[1:-1]
    #remove curly brackets
    for i in range(len(article)):
        article[i] = article[i].replace("{", "")
        article[i] = article[i].replace("}", "")
        article[i] = article[i].replace(",", "")
    article_dict = {}
    for i in article:
        i = i.split(" = ")
        article_dict[i[0].strip()] = i[1].strip()
    return article_dict


def get_article_from_db_by_user(user):

    uri = "mongodb+srv://testiuser:testisalasana123@ohtuminiprojekti-bibtex.19oezdh.mongodb.net/test?retryWrites=true&w=majority"

    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client["bibtex"]
    collection = db["articles"]
    for article in collection.find({"user":user}):
        return article

def get_article_from_db_by_cite_key(user, cite_key):
    uri = "mongodb+srv://testiuser:testisalasana123@ohtuminiprojekti-bibtex.19oezdh.mongodb.net/test?retryWrites=true&w=majority"

    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client["bibtex"]
    collection = db["articles"]
    for article in collection.find({"user": user, "cite_key": cite_key}):
        return article
    
def get_article_from_db_by_author(user, author):
    uri = "mongodb+srv://testiuser:testisalasana123@ohtuminiprojekti-bibtex.19oezdh.mongodb.net/test?retryWrites=true&w=majority"

    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client["bibtex"]
    collection = db["articles"]
    for article in collection.find({"user": user, "author": author}):
        return article

def get_article_from_db_by_year(user, year):
    uri = "mongodb+srv://testiuser:testisalasana123@ohtuminiprojekti-bibtex.19oezdh.mongodb.net/test?retryWrites=true&w=majority"

    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client["bibtex"]
    collection = db["articles"]
    for article in collection.find({"user": user, "year": year}):
        return article

def delete_article_by_cite_key(user,cite_key):
    '''Delete an article from the database'''
    uri = "mongodb+srv://testiuser:testisalasana123@ohtuminiprojekti-bibtex.19oezdh.mongodb.net/test?retryWrites=true&w=majority"

    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client["bibtex"]
    collection = db["articles"]
    
    collection.delete_one({"user": user, "cite_key": cite_key})

author = "Matti Meikäläinen"
title = "Tämä on otsikko2"
journal = "Journal of Journals"
year = 2020
volume = 1
number = 2
pages = 3
month = 4
note = "Tämä on huomautus"
author, title, journal, year, volume, number, pages, month, note = read_user_input_article(author, title, journal, year, volume, number, pages)
article = to_bibtex_article(author, title, journal, year, volume, number, pages, month, note)
add_article_to_db("testiuser", article)