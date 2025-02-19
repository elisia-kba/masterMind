from flask import Flask, redirect, render_template, request, session, url_for
from mastermind import Mastermind

app = Flask(__name__)
app.secret_key = "mastermind_secret_key"  # Clé secrète pour gérer la session

jeu = Mastermind()

# Dictionnaire de traduction des couleurs
COULEURS_FR = {
    "red": "rouge",
    "yellow": "jaune",
    "blue": "bleu",
    "orange": "orange",
    "green": "vert",
    "black": "noir",
    "purple": "violet",
    "pink": "rose"
}

@app.route("/", methods=["GET", "POST"])
def index():
    if "solution" not in session or "essais" not in session:
        session["solution"] = jeu.generate_solution()  # On génère une nouvelle solution
        session["essais"] = []  # Liste des essais
    
    solution = session["solution"]
    essais = session["essais"]
    
    # On supprime le message stocké
   

    if request.method == "POST":
        proposition = request.form.getlist("colors[]")
        if proposition:
            # Vérifie si l'entrée est valide
            if len(proposition) != 4 or not all(c in jeu.couleurs for c in proposition):
                session["message"] = "Erreur : Veuillez entrer exactement 4 couleurs valides parmi : rouge, jaune, bleu, orange, vert, noir, violet, rose"
            elif len(set(proposition)) != 4:
                session["message"] = "Erreur : Les couleurs doivent être différentes"
            else:
                correction = jeu.correction(solution, proposition)
                essais.append({"proposition": proposition, "correction": correction})
                session["essais"] = essais

                if correction == ["O", "O", "O", "O"]:
                    session["message"] = "Bravo ! Vous avez trouvé la combinaison secrète 🎉"
                    session.pop("solution", None)  # On réinitialise la partie
                elif len(essais) >= 10:
                    #On traduit les couleurs de la solution avant de les afficher
                    solution_fr = [COULEURS_FR[couleur] for couleur in solution]
                    session["message"] = f"Dommage, vous avez perdu ! La solution était : {', '.join(solution_fr)}."
                    session.pop("solution", None)  #On rénitialise la partie

    message = session.pop("message", "")
    return render_template("index.html", essais=essais, couleurs=jeu.couleurs, message=message)

@app.route("/reset", methods=["POST"])
def reset():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
