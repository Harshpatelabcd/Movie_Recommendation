import login as login
import requests
from flask import Flask, render_template, request, redirect, url_for
import pickle
import numpy as np
import requests
import pandas as pd
import json

popular_df = pd.read_pickle(open('popular1.pkl', 'rb'))
users = pd.read_pickle(open('users.pkl', 'rb'))
pt = pd.read_pickle(open('pt.pkl', 'rb'))
movies = pd.read_pickle(open('movies.pkl', 'rb'))
similarity_scores = pd.read_pickle(open('similarity_scores.pkl', 'rb'))


app = Flask(__name__, template_folder='templates')


@app.route('/')
def index():
    return render_template('Homepage.html')


@app.route('/login')
def index1():
    return render_template('Login.html')



@app.route('/userhomepage')
def user_homepage():
    return render_template('Userhomepage.html',
                           original_title=list(popular_df['original_title'].values),
                           overview=list(popular_df['overview'].values),
                           avg_rating=list(popular_df['avg_rating'].values),
                           posters=list(popular_df['belongs_to_collection'].values)
                           )


@app.route('/login_user', methods=['GET', 'POST'])
def login():
    error = "Invalid Credentials"
    user_email = request.form['user_email']
    user_password = request.form['pass']

    pkl_email = list(users['email'].values)
    pkl_password = list(users['password'].values)

    if request.method == 'POST':
        if user_email in pkl_email and user_password in pkl_password:
            return redirect(url_for('user_homepage'))

        else:
            return render_template("Login.html", error=error)
    else:
        return render_template("Login.html", error=error)


@app.route('/recommendation', methods=['GET', 'POST'])
def recommend():
    movie_title = request.form.get('movie_title', False)
    try:
        index_1 = next((i for i, title in enumerate(pt.index) if title == movie_title), None)
        similar_items = sorted(list(enumerate(similarity_scores[index_1])), key=lambda x: x[1], reverse=True)[1:6]

        data = []
        for i in similar_items:
            item = []
            temp_df = movies[movies['original_title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('original_title')['original_title'].values))
            item.extend(list(temp_df.drop_duplicates('original_title')['crew'].values))
            item.extend(list(temp_df.drop_duplicates('original_title')['overview'].values))
            item.extend(list(temp_df.drop_duplicates('original_title')['belongs_to_collection'].values))

            data.append(item)

        return render_template('Recommendation.html', data=data)

    except IndexError:
        return "error"


if __name__ == '__main__':
    app.run(debug=True)
