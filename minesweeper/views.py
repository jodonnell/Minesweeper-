# Create your views here.
from django.shortcuts import render_to_response
from django import forms
from django import http

from minesweeper.classes.create_board import CreateBoard
from minesweeper.classes.board import Board

from pymongo import Connection, DESCENDING

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

    create_board = CreateBoard(ROWS, COLUMNS, TOTAL_MINES)
    board = Board(create_board)

    if query is None:
        db.minesweeper.insert({"email": email, "board":cPickle.dumps(board), 'new_game':True})
    else:
        db.minesweeper.update({"email": email}, {"email": email, "board":cPickle.dumps(board), 'new_game':True})

        return render_to_response('index.html', {'num_flags':TOTAL_MINES, 'rows':ROWS, 'columns':COLUMNS})

def clear(request):
    row = int(request.GET['row'])
    column = int(request.GET['column'])
    email = request.COOKIES['email']

    board = _get_board(email)

    update_board(email, board)

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

    update_board(email, board)
    
    response = {}
    if board.has_won():
        high_score = check_high_score(email)
        response = {'won':True, 'high_score': high_score}

    return http.HttpResponse(json.dumps(response))

def update_board(email, board):
    update_row = {"email": email, "board":cPickle.dumps(board), "new_game":False}
    db = connection.minesweeper
    query = db.minesweeper.find_one({'email':email})
    if 'new_game' in query and query['new_game']:
        update_row['time'] = datetime.datetime.now()
    else:
        update_row['time'] = query['time']

    db.minesweeper.update({"email": email}, update_row)


def check_high_score(email):
    db = connection.minesweeper
    game = db.minesweeper.find_one({'email':email})

    high_scores_query = db.high_scores.find()
    high_scores_query.sort('time', DESCENDING)

    time_diff = datetime.datetime.now() - game['time']
    game_time = float(str(time_diff.seconds) + '.' + str(time_diff.microseconds))

    high_score = False
    if high_scores_query.count() >= 10 and game_time < high_scores_query[0]['time']:
        db.high_scores.remove(high_scores_query[0]['_id'])
        db.high_scores.insert({'email':game['email'], 'time':game_time})
        high_score = True
    elif high_scores_query.count() < 10:
        db.high_scores.insert({'email':game['email'], 'time':game_time})
        high_score = True

    if high_score:
        return game_time
    return 0

def reset(request):
    email = request.COOKIES['email']
    db = connection.minesweeper
    create_board = CreateBoard(ROWS, COLUMNS, TOTAL_MINES)
    board = Board(create_board)
    db.minesweeper.update({"email": email}, {"email": email, "board":cPickle.dumps(board), 'new_game':True})
    return http.HttpResponse(json.dumps([]))

def view_high_scores(request):
    db = connection.minesweeper
    high_scores_query = db.high_scores.find()
    high_scores_query.sort('time', DESCENDING)

    return render_to_response('view_high_scores.html', { 'high_scores': high_scores_query })
    

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

