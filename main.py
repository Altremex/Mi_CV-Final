from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
import os
from forms import ContactForm, is_valid_email
from flask_mail import Mail, Message
from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth


app=Flask(__name__)

load_dotenv()
app.secret_key = 'SECRET_KEY'


app.config["RECAPTCHA_PUBLIC_KEY"]= os.getenv("RECAPTCHA_PUBLIC_KEY")
app.config["RECAPTCHA_PRIVATE_KEY"]=os.getenv("RECAPTCHA_PRIVATE_KEY")

# Configuración de las credenciales de Spotify
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")


#Configuracion de Flask-Mail
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)





@app.route("/")
def home():
    return render_template("index.html")

@app.route("/spotify", methods=["GET", "POST"])
def spotify():
    song_uris = []  # Lista para almacenar las URI de las canciones
    playlist_url=None
    if request.method == "POST":
        # Obtener la fecha ingresada por el usuario
        date = request.form.get("date")
        # Scraping de Billboard Hot 100
        header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}
        billboard_url = f"https://www.billboard.com/charts/hot-100/{date}"
        response = requests.get(url=billboard_url, headers=header)

        soup = BeautifulSoup(response.text, 'html.parser')
        song_names_spans = soup.select("li ul li h3")
        song_names = [song.getText().strip() for song in song_names_spans]

        # Autenticación de Spotify
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-private", redirect_uri=REDIRECT_URI,
                                                        client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                                                        show_dialog=True, cache_path="tokens/token.txt"))
        user_id = sp.current_user()["id"]

        # Buscar canciones en Spotify
        year = date.split("-")[0]
        for song in song_names:
            result = sp.search(q=f"track:{song} year:{year}", type="track", limit=1)
            try:
                uri = result["tracks"]["items"][0]["uri"]
                song_uris.append(uri)
            except IndexError:
                flash(f"{song} doesn't exist in Spotify. Skipped.")

        # Crear la lista de reproducción privada
        playlist = sp.user_playlist_create(user=user_id, name=f"({date}) The 100 That Raised Me", public=False)
        sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

        playlist_url= playlist["external_urls"]["spotify"]

    return render_template("spotify.html", song_uris=song_uris, playlist_url=playlist_url)
    


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form=ContactForm()

    if form.validate_on_submit():
        name=request.form["name"]
        email=request.form["email"]
        message=request.form["message"]


        # Validar el correo antes de continuar
        if not is_valid_email(email):
            flash("Por favor, introduce un correo electrónico válido.")
            return redirect(url_for("contact"))

        #Creal el mensaje de correo
        msg=Message(
            subject=f"Tienes un mensaje de {name}",
            sender=app.config["MAIL_USERNAME"],
            recipients=[app.config["MAIL_USERNAME"]],
            reply_to=email,
            body=f"Mensaje:\n{message}"
        )
        

        try:
            mail.send(msg)
            flash("Gracias por tu mensaje. Hemos enviado una confirmación a tu correo.")
        except Exception as e:
            print(f"Error al enviar correo: {e}")  # Imprime el error en la consola
            flash(f"Error al enviar el correo: {e}")


        return redirect(url_for("contact"))


    return render_template("contact.html", form=form)


if __name__=='__main__':
    app.run(debug=False)


