# Create your views here.
from django.shortcuts import render_to_response
from django import forms
from django import http

from minesweeper.classes.create_board import CreateBoard
from minesweeper.classes.board import Board

from pymongo import Connection

import cPickle
import json
import datetime

ROWS = 8
COLUMNS = 8
TOTAL_MINES = 10

connection = Connection('localhost', 27017)

class EmailForm(forms.Form):
    email = forms.EmailField(required = True)

def index(request):
    if 'email' not in request.COOKIES:
        return _get_email(request)

    email = request.COOKIES['email']

    db = connection.minesweeper
    query = db.minesweeper.find_one({'email':email})

    if query is None:
        create_board = CreateBoard(ROWS, COLUMNS, TOTAL_MINES)
        board = Board(create_board)
        db.minesweeper.insert({"email": email, "board":cPickle.dumps(board), 'new_game':True})
    else:
        board = cPickle.loads(str(query['board']))

    return render_to_response('index.html', {'board':board, 'rows':ROWS, 'columns':COLUMNS, 'flags':json.dumps(board._flags)})

def clear(request):
    row = int(request.GET['row'])
    column = int(request.GET['column'])

    board = _get_board(request.COOKIES['email'])
    if board.is_mined(row, column):
        return http.HttpResponse(json.dumps({'lost':True}))

    num_surronding_mines = board.get_num_surronding_mines(row, column)
    if num_surronding_mines:
        return http.HttpResponse(json.dumps({'num_surronding_mines':num_surronding_mines}))

    clear_area = board.get_clear_area(row, column, [])
    return http.HttpResponse(json.dumps({'clear_area':clear_area}))

def flag(request):
    email = request.COOKIES['email']

    row = int(request.GET['row'])
    column = int(request.GET['column'])

    board = _get_board(request.COOKIES['email'])
    board.place_flag(row, column)

    update_row = {"email": email, "board":cPickle.dumps(board)}
    db = connection.minesweeper
    query = db.minesweeper.find_one({'email':email})
    if 'new_game' in query and query['new_game']:
        update_row['new_game'] = False
        update_row['time'] = datetime.datetime.now()

    db.minesweeper.update({"email": email}, update_row)
    
    response = {}
    if board.has_won():
        response = {'won':True}

    return http.HttpResponse(json.dumps(response))

def reset(request):
    email = request.COOKIES['email']
    db = connection.minesweeper
    create_board = CreateBoard(ROWS, COLUMNS, TOTAL_MINES)
    board = Board(create_board)
    db.minesweeper.update({"email": email}, {"email": email, "board":cPickle.dumps(board), 'new_game':True})
    return http.HttpResponse(json.dumps([]))

def _get_board(email):
    db = connection.minesweeper
    query = db.minesweeper.find_one({'email':email})
    return cPickle.loads(str(query['board']))

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
