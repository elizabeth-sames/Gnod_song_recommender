{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "4a8a6843",
   "metadata": {},
   "outputs": [],
   "source": [
    "#!/usr/bin/env python"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "ce7191e8",
   "metadata": {},
   "outputs": [],
   "source": [
    "import spotipy\n",
    "from spotipy.oauth2 import SpotifyClientCredentials\n",
    "import pandas as pd\n",
    "from random import randint\n",
    "from time import sleep\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "from sklearn import cluster, datasets\n",
    "from sklearn.preprocessing import StandardScaler\n",
    "from matplotlib.lines import Line2D\n",
    "from sklearn.cluster import KMeans\n",
    "from sklearn.metrics import silhouette_score\n",
    "from sklearn.cluster import DBSCAN\n",
    "import pickle"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "d9e04fa6",
   "metadata": {},
   "outputs": [],
   "source": [
    "secrets_file = open(\"secrets.txt\",\"r\")\n",
    "string = secrets_file.read()\n",
    "string.split('\\n')\n",
    "secrets_dict={}\n",
    "for line in string.split('\\n'):\n",
    "    if len(line) > 0:\n",
    "        secrets_dict[line.split(':')[0]]=line.split(':')[1]\n",
    "        \n",
    "        \n",
    "sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=secrets_dict['cid'],\n",
    "                                                           client_secret=secrets_dict['csecret']))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "c6d49998",
   "metadata": {},
   "outputs": [],
   "source": [
    "#load song datasets\n",
    "hot_songs = pd.read_csv('hot_songs.csv', index_col=0)\n",
    "songs = pd.read_csv('clustered_songs.csv', index_col=0)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "98fccbb5",
   "metadata": {},
   "outputs": [],
   "source": [
    "#load scaler and model\n",
    "ss = pickle.load(open('gnod_scaler.sav', 'rb'))\n",
    "kmeans = pickle.load(open('gnod_kmeans_model.sav', 'rb'))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "3546afaf",
   "metadata": {},
   "outputs": [],
   "source": [
    "def song_recommender():\n",
    "    song_input=input('Enter a song: ')\n",
    "    if song_input in hot_songs.title.values:\n",
    "        n = random.randint(0,len(hot_songs))\n",
    "        reco_song_title = hot_songs.title[n]\n",
    "        reco_song_artist = hot_songs.artist[n]\n",
    "        return f\"We recommend {reco_song_title} by {reco_song_artist}.\"\n",
    "    \n",
    "    else:\n",
    "        #get uri\n",
    "        results = sp.search(q= song_input, limit=1, type='track')\n",
    "        if results['tracks']['total'] != 0:\n",
    "            uri = results['tracks']['items'][-1]['uri']\n",
    "        else: \n",
    "            return f\"{song_input} not found on Spotify\"\n",
    "\n",
    "        #get audio features using uri\n",
    "        song_details = sp.audio_features(uri)\n",
    "        song_features = song_details[0]\n",
    "        audio_features = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', \n",
    "            'liveness', 'valence', 'tempo', 'time_signature']\n",
    "        song_af = {f:song_features[f] for f in audio_features}\n",
    "        af = pd.DataFrame(song_af, index=[0])\n",
    "        \n",
    "        #scale audio features\n",
    "        af=ss.transform(af)\n",
    "        \n",
    "        #find cluster\n",
    "        pred_cluster = kmeans.predict(af)\n",
    "        \n",
    "        #suggest song from that cluster\n",
    "        cluster_songs = songs[songs['kmeans_cluster'] == pred_cluster[0]]\n",
    "        cluster_songs.reset_index(inplace=True, drop=True)\n",
    "        n = randint(0,len(cluster_songs))\n",
    "        reco_song_title = cluster_songs.iloc[n].title\n",
    "        reco_song_artist = cluster_songs.iloc[n].artist\n",
    "        return f\"We recommend '{reco_song_title}' by {reco_song_artist}.\""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "8be3a7ef",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Enter a song: Let it Be\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "\"We recommend 'Banana Boat (Day-O)' by Harry Belafonte.\""
      ]
     },
     "execution_count": 7,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "song_recommender()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "48d21d32",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
