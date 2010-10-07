# Create your views here.
from django.shortcuts import render_to_response
from django import forms
from django import http

from minesweeper.classes.create_board import CreateBoard
from minesweeper.classes.board import Board

from pymongo import Connection, DESCENDING, ASCENDING

import cPickle
import json
import datetime

ROWS = 8
COLUMNS = 8
TOTAL_MINES = 10

connection = Connection('localhost', 27017)

class EmailForm(forms.Form):
    email = forms.EmailField(required = True)

def _get_minesweeper_db():
    return connection.minesweeper

def index(request):
    if 'email' not in request.COOKIES:
        return _get_email(request)

    email = request.COOKIES['email']

    db = _get_minesweeper_db()
    game_query = db.minesweeper.find_one({'email':email})

    board = _create_new_board()

    new_record = {"email": email, "board":cPickle.dumps(board), 'new_game':True}
    if game_query is None:
        db.minesweeper.insert(new_record)
    else:
        db.minesweeper.update({"email": email}, new_record)

        return render_to_response('index.html', {'num_flags':TOTAL_MINES, 'rows':ROWS, 'columns':COLUMNS})

def clear(request):
    "User is attempting to clear a square"
    row, column, email = _get_row_column_email_params(request)

    board = _get_board(email)
    _update_board(email, board)

    if board.is_mined(row, column):
        return http.HttpResponse(json.dumps({'lost':True}))

    num_surronding_mines = board.get_num_surronding_mines(row, column)
    if num_surronding_mines:
        return http.HttpResponse(json.dumps({'num_surronding_mines':num_surronding_mines}))

    clear_area = board.get_clear_area(row, column, [])
    return http.HttpResponse(json.dumps({'clear_area':clear_area}))

def _update_board(email, board):
    update_row = {"email": email, "board":cPickle.dumps(board), "new_game":False}
    db = _get_minesweeper_db()
    query = db.minesweeper.find_one({'email':email})
    if 'new_game' in query and query['new_game']:
        update_row['time'] = datetime.datetime.now()
    else:
        update_row['time'] = query['time']

    db.minesweeper.update({"email": email}, update_row)

def flag(request):
    row, column, email = _get_row_column_email_params(request)

    board = _get_board(email)
    board.place_flag(row, column)

    _update_board(email, board)
    
    response = {}
    if board.has_won():
        high_score = _check_high_score(email)
        response = {'won':True, 'high_score': high_score}

    return http.HttpResponse(json.dumps(response))

def _get_row_column_email_params(request):
    row = int(request.GET['row'])
    column = int(request.GET['column'])
    email = request.COOKIES['email']
    return (row, column, email)

def _check_high_score(email):
    db = _get_minesweeper_db()
    game = db.minesweeper.find_one({'email':email})

    high_scores_query = db.high_scores.find()
    high_scores_query.sort('time', DESCENDING)

    time_diff = datetime.datetime.now() - game['time']
    game_time = float(str(time_diff.seconds) + '.' + str(time_diff.microseconds))

    high_score = 0
    if high_scores_query.count() >= 10 and game_time < high_scores_query[0]['time']:
        db.high_scores.remove(high_scores_query[0]['_id'])
        db.high_scores.insert({'email':game['email'], 'time':game_time})
        high_score = game_time
    elif high_scores_query.count() < 10:
        db.high_scores.insert({'email':game['email'], 'time':game_time})
        high_score = game_time

    return high_score

def reset(request):
    email = request.COOKIES['email']
    board = _create_new_board()
    db = _get_minesweeper_db()
    db.minesweeper.update({"email": email}, {"email": email, "board":cPickle.dumps(board), 'new_game':True})
    return http.HttpResponse(json.dumps([]))

def _create_new_board():
    create_board = CreateBoard(ROWS, COLUMNS, TOTAL_MINES)
    return Board(create_board)

def view_high_scores(request):
    db = _get_minesweeper_db()
    high_scores_query = db.high_scores.find()
    high_scores_query.sort('time', ASCENDING)

    return render_to_response('view_high_scores.html', { 'high_scores': high_scores_query })
    
def _get_board(email):
    db = _get_minesweeper_db()
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

