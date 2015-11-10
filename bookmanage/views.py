from django.shortcuts import render_to_response
import MySQLdb
import random
# -*- coding: utf-8 -*-
#from django.views.decorators.csrf import csrf_exempt
#@csrf_exempt
# Create your views here.
def homepage(request):
    return render_to_response('home.html')
    
def Error(request):
    return render_to_response('error.html')
    
def Search(request):
    if 'author_name' in request.GET and request.GET['author_name']:
        au_name = request.GET['author_name']
        conn = MySQLdb.connect(db="bookmanage", charset="utf8")
        cur = conn.cursor()
        cur.execute("select AuthorID from bookmanage_author where Name='%s' "%au_name)
        tauid = cur.fetchall()
        if tauid:
            for ttp in tauid:
                auid=ttp
            cur2 = conn.cursor()
            cur2.execute("select * from bookmanage_book where AuthorID_id=%d" %auid)
            books = cur2.fetchall()
    
            conn.close()
            return render_to_response('books.html',{'books':books,'author':au_name})
        else:
            books = []
            return render_to_response('books.html',{'books':books})
    else:
        return render_to_response('search.html')
    
    
def Show(request):
    conn = MySQLdb.connect(host="localhost", user='root', passwd='', db="bookmanage", charset="utf8")
    cur = conn.cursor()
    cur.execute("select * from bookmanage_book")
    books = cur.fetchall()
    conn.close()
    return render_to_response('books.html',{'books':books})


def BookInf(request):
    conn = MySQLdb.connect(host="localhost", user='root', passwd='', db="bookmanage", charset="utf8")
    cur = conn.cursor()
    if request.GET["id"]:
        bookid = int(request.GET["id"])
        cur.execute("select * from bookmanage_book where ISBN=%d" %bookid)
        books = cur.fetchall()
        for book in books:
            authorid = book[2]
        cur2 = conn.cursor()
        cur2.execute("select * from bookmanage_author where AuthorID=%d" %authorid)
        authors = cur2.fetchall()
        return render_to_response('bookinf.html',{'books':books,'author':authors})


def Delete(request):
    conn = MySQLdb.connect(host="localhost", user='root', passwd='', db="bookmanage", charset="utf8")
    if request.GET["deid"]:  
        bookid = int(request.GET["deid"])
        cur2 = conn.cursor()
        cur2.execute("delete from bookmanage_book where ISBN=%d" %bookid)
        cur2.close()
        conn.commit()
        cur = conn.cursor()
        cur.execute("select * from bookmanage_book")
        books = cur.fetchall()
        conn.close()
    return render_to_response('manage.html',{'books':books})


def Update(request):    
    conn = MySQLdb.connect(host="localhost", user='root', passwd='', db="bookmanage", charset="utf8")
    if 'uid' in request.GET and request.GET["uid"]:
        bookid = int(request.GET["uid"])
        if 'tauthor_name' in request.GET and request.GET["tauthor_name"]:
            aunametmp = request.GET["tauthor_name"]
            cur = conn.cursor()
            cur.execute("select * from bookmanage_author where Name='%s'" %aunametmp)
            authors = cur.fetchall()
            if authors:
                for author in authors:
                    auid = author[0]
                    cur.close()
            else:
                cur.close()
                return render_to_response('error.html')
            cur = conn.cursor()
            cur.execute("update bookmanage_book set AuthorID_id=%d where ISBN=%d" %(auid,bookid))
            cur.close()
            conn.commit()
        if 'tpublisher' in request.GET and request.GET["tpublisher"]:
            publishertmp = request.GET["tpublisher"]
            cur = conn.cursor()
            cur.execute("update bookmanage_book set Publisher='%s' where ISBN=%d" %(publishertmp,bookid))
            cur.close()
            conn.commit()
        if 'tdate' in request.GET and request.GET["tdate"]:
            datetmp = request.GET["tdate"]
            cur = conn.cursor()
            cur.execute("update bookmanage_book set PublishDate='%s' where ISBN=%d" %(datetmp,bookid))
            cur.close()
            conn.commit()
        if 'tprice' in request.GET and request.GET["tprice"]:
            pricetmp = float(request.GET["tprice"])
            cur = conn.cursor()
            cur.execute("update bookmanage_book set Price=%f where ISBN=%d" %(pricetmp,bookid))
            cur.close()
            conn.commit()
        
        cur = conn.cursor()
        cur.execute("select * from bookmanage_book where ISBN=%d" %bookid)
        books = cur.fetchall()
        for book in books:
            authorid = book[2]
            date = book[4]
            date=date.strftime('%Y-%m-%d')
        cur2 = conn.cursor()
        cur2.execute("select * from bookmanage_author where AuthorID=%d" %authorid)
        authors = cur2.fetchall()
        for author in authors:
            authorname = author[1]       
        conn.close()
        return render_to_response('update.html',{'books':books,'author':authorname,'datetime':date})
    return render_to_response('manage.html')
    
def Add_author(request):
    if request.GET:
        if 'aucountry' in request.GET:
            auname = request.GET['auname']
            auage = int(request.GET['auage'])
            aucountry = request.GET['aucountry']
            conn = MySQLdb.connect(host="localhost", user='root', passwd='', db="bookmanage", charset="utf8")
            cur = conn.cursor()
            while True:
                a = random.randint(1,100)
                cur.close()
                cur = conn.cursor()
                try:
                    cur.execute("selcet * from bookmanage_author where AuthorID=%d" %a)
                except:
                    cur.close()
                    break;  
                else:
                    pass
            auid = a
            cur = conn.cursor()
            cur.execute("insert into bookmanage_author values (%d,'%s',%d,'%s')" %(auid,auname,auage,aucountry))
            cur.close()
            conn.commit()
            conn.close()
    return render_to_response('add_author.html')    
    
    
def Add(request):
    conn = MySQLdb.connect(host="localhost", user='root', passwd='', db="bookmanage", charset="utf8")
    cur = conn.cursor()
    if request.GET:
        if ('tauthor_name' in request.GET and request.GET["tauthor_name"]) and \
        ('ttitle' in request.GET and request.GET["ttitle"]) and \
        ('tpublisher' in request.GET and request.GET["tpublisher"]) and \
        ('tdate' in request.GET and request.GET["tdate"]) and \
        ('tprice' in request.GET and request.GET["tprice"]) and \
        ('tisbn' in request.GET and request.GET["tisbn"]):
            isbn = request.GET["tisbn"]
            name = request.GET["tauthor_name"]
            title = request.GET["ttitle"]
            publisher = request.GET["tpublisher"]
            date = request.GET["tdate"]
            price = float(request.GET["tprice"])
            cur.execute("select AuthorID from bookmanage_author where Name='%s'" %name)
            auids = cur.fetchall()
            if auids:
                for tauid in auids:
                    auid = tauid[0]
                cur.close()
            else:
                cur.close()
                return render_to_response('error.html')
            cur = conn.cursor()  
            cur.execute("insert into bookmanage_book values ('%s','%s',%d,'%s','%s',%f)"\
            %(isbn,title,auid,publisher,date,price))
            cur.close()
            conn.commit()
            cur = conn.cursor()
            cur.execute("select * from bookmanage_book")
            books = cur.fetchall()
            conn.close()
            return render_to_response('manage.html',{'books':books})
        return render_to_response('add_book.html')
    else:
        return render_to_response('add_book.html')
        
        
def Manage(request):
    conn = MySQLdb.connect(host="localhost", user='root', passwd='', db="bookmanage", charset="utf8")
    cur = conn.cursor()
    cur.execute("select * from bookmanage_book")
    books = cur.fetchall()
    conn.close()
    return render_to_response('manage.html',{'books':books})



