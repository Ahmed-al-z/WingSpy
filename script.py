import paho.mqtt.client as mqtt
import os
from git import Repo

# MQTT settings
BROKER = "192.168.1.40"  
TOPIC = "camera/picture"
SAVE_PATH = "/home/alz/Desktop/votre-depot/im.jpg"  # Chemin dans le dépôt cloné
REPO_PATH = "/home/alz/Desktop/votre-depot"         # Chemin vers le dépôt Git cloné

def upload_to_github(file_path, repo_path):
    try:
        repo = Repo(repo_path)  # Ouvrir le dépôt local
        repo.git.add(file_path)  # Ajouter le fichier
        repo.index.commit("New image uploaded")  # Commit avec un message
        origin = repo.remote(name="origin")  # Récupérer le dépôt distant
        origin.push()  # Pousser les modifications
        print("Image pushed to GitHub successfully!")
    except Exception as e:
        print(f"Failed to upload image: {e}")

def on_message(client, userdata, message):
    print("Image received. Saving...")
    with open(SAVE_PATH, "wb") as image_file:
        image_file.write(message.payload)
    print(f"Image saved at {SAVE_PATH}")

    # Upload the image to GitHub
    upload_to_github(SAVE_PATH, REPO_PATH)

def main():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(BROKER, 1883)
    client.subscribe(TOPIC)

    print("Waiting for images...")
    client.loop_forever()

if __name__ == "__main__":
    main()

