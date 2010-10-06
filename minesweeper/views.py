# Create your views here.
from django.shortcuts import render_to_response
from django import forms
from django import http

from minesweeper.classes.create_board import CreateBoard
from minesweeper.classes.board import Board

from pymongo import Connection

import cPickle

connection = Connection('localhost', 27017)

class EmailForm(forms.Form):
    email = forms.EmailField(required = True)

def index(request):
    if 'email' not in request.COOKIES:
        return _get_email(request)

    email = request.COOKIES['email']

    rows = 8
    columns = 8
    total_mines = 10

    db = connection.minesweeper
    query = db.minesweeper.find_one({'email':email})

    if query is None:
        create_board = CreateBoard(rows, columns, total_mines)
        board = Board(create_board)
        db.minesweeper.insert({"email": email, "board":cPickle.dumps(board)})
    else:
        board = cPickle.loads(str(query['board']))

    return render_to_response('index.html', {'board':board, 'rows':rows, 'columns':columns})


def _get_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            redirect = http.HttpResponseRedirect('/')
            redirect.set_cookie('email', form.cleaned_data['email'])
            return redirect
    else:
        form = EmailForm()

    return render_to_response('get_email.html', { 'form': form })
