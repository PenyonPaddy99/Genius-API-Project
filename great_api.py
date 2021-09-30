from flask import Flask, render_template, request, redirect
import requests


app = Flask(__name__, template_folder='templates')

@app.route('/')
def authentication():
    client_id = "-NTv8UOHQs-4ECLqy1rPK5WAj17twauHfV0-bSCcnV9GGBvZirKxlJs54zTuFpaV"
    redirect_uri = "http://localhost:5000/my_form"
    scope = "me"
    state = "1"


    return redirect("https://api.genius.com/oauth/authorize?client_id="+client_id+"&redirect_uri="+redirect_uri+"&scope="+scope+"&state="+state+"&response_type=code")

@app.route('/my_form')
def my_form():
    return render_template('my_form.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
    artist = request.form['artist']
    artist_input = artist.replace(" ", "-")

    base_url = "https://api.genius.com"
    client_access_token = '82y8VzudEJxL6VlJwH39Bbipu4vuO2u-Okh0zO0gVMD2BUb6lMoJ1EDpybyhUZrY'

    headers = {'Authorization': 'Bearer ' + client_access_token}
    search_url = base_url + '/search'
    data = {'q': str(artist_input)}

    response = requests.get(search_url, data=data, headers=headers)
    r = response.json()

    artist_id = r['response']['hits'][0]['result']['primary_artist']['id']
    song_list = []

    n = 0

    while n < 10:
        song_list.append(r['response']['hits'][n]['result']['title'])
        n += 1

    return render_template('result.html', artist=artist, song_list=song_list, len=len(song_list))


if __name__ == '__main__':
    app.run(debug=True)
