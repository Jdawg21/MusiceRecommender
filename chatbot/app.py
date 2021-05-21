from flask import Flask, render_template, jsonify, request
from regex._regex_core import Info

import processor
import SongRecommendation
import GenreSearch
import ArtistSearch
from dash.dependencies import Input, Output

app = Flask(__name__)

app.config['SECRET_KEY'] = 'enter-a-very-secretive-key-3479373'


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('/dist/index.html', **locals())

songs = 0
artist = 0
genre = 0
text = 0
track = 0
option = 0
mood = ""
userinput = ""
sentiment = ""
flag = 0


@app.route('/chatbot', methods=["GET", "POST"])
def chatbotResponse():
    global songs
    global artist
    global genre
    global text
    global track
    global mood
    global option
    global flag
    response = ""
    if request.method == 'POST':
        postData = request.form

        if request.form.getlist('reload'):
            songs = 0
            artist = 0
            genre = 0
            text = 0
            track = 0
            option = 0
        else:
            the_question = request.form['chatbox']
            # if track == 1:
            if flag == 1:
                if the_question == "Y" or the_question == "y":
                    songs = 1
                    flag = 0
                else:
                    track = 0
                    songs = 0

            if the_question.lower() == "search artist":
                artist = 1
                response = "Enter artist name"
            elif the_question.lower() == "search similar songs":
                songs = 1
                response = "How are you feeling today?"
            elif the_question.lower() == "search genre":
                genre = 1
                response = GenreSearch.genresearch()
            elif artist == 1:
                artist = 0
                response = ArtistSearch.getArtist(the_question)
                if response.find("No result :(") > -1:
                    option = 0
                else:
                    option = 1
            elif option == 1:
                option = 0
                response = ArtistSearch.artistsearch(the_question)
            elif genre == 1:
                genre = 0
                response = GenreSearch.genre_recommend(the_question)

            elif songs == 1:
                songs = 0
                mood = the_question
                response = "Enter the song you want recommendations for"
                text = 1

            elif text == 1:
                text = 0
                global userinput
                userinput = the_question
                track = 1
                global sentiment
                response, sentiment = SongRecommendation.getSong(mood, userinput)
                if response.find("Sorry!! We couldnt get any results for") > -1:
                    track = 0
            elif track == 1:
                response = SongRecommendation.songrecommender(the_question, userinput, sentiment)
                response += "<div class=\"alert alert-info\"><strong>Enter 'Y' to get recommendations for another song.</strong>"
                track = 0
                flag = 1
            else:
                # print(the_question)
                response = processor.chatbot_response(the_question)
            # print(response)

    return jsonify({"response": response})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8888', debug=True)
