# -*- coding: utf-8 -*-

import sys
import numpy as np
import sqlite3 as sq
import sys
from collections import defaultdict
import math
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity




def vectorize_recipes2(recipes):

    # Difficulty

    # Get text from recipes
    recipes_text = []
    for recipe in recipes:
        recipe_text = recipe.get_name() + " " \
            + recipe.get_ingredients().replace("|", " ") + " " \
            + recipe.get_instructions()

        recipes_text.append(recipe_text)

    # Vectorization using sklearn feature_extraction (text)
    vectorizer = TfidfVectorizer(recipes_text)
    recipes_term_document = vectorizer.fit_transform(recipes_text)

    # Get Difficulty
    difficulty_feats = ["Facile", "Très facile", "Moyennement difficile","Difficile"]
    cost_feats = ["Moyen", "Bon marché", "Assez cher"]
    guests_number_feats = [2, 4, 6, 8, 10]


    v_recipes = []
    for i, recipe in enumerate(recipes_term_document.toarray()):

        feats = []
        for feat in difficulty_feats:
            if recipes[i].get_difficulty() == feat:
                feats.append(1)
            else:
                feats.append(0)

        for feat in cost_feats:
            if recipes[i].get_cost() == feat:
                feats.append(1)
            else:
                feats.append(0)

        # Preparation_time
        if int(recipes[i].get_preparation_time()) <=20:
            feats.append(1)
        else:
            feats.append(0)

        if int(recipes[i].get_preparation_time()) > 20 and  int(recipes[i].get_preparation_time()) <= 45:
            feats.append(1)
        else:
            feats.append(0)

        if int(recipes[i].get_preparation_time()) > 45:
            feats.append(1)
        else:
            feats.append(0)

        # cook_time
        if int(recipes[i].get_cook_time()) <=20:
            feats.append(1)
        else:
            feats.append(0)

        if int(recipes[i].get_cook_time()) > 20 and  int(recipes[i].get_preparation_time()) <= 45:
            feats.append(1)
        else:
            feats.append(0)

        if int(recipes[i].get_cook_time()) > 45:
            feats.append(1)
        else:
            feats.append(0)


        # Guests number
        for nb in guests_number_feats:
            if int(recipes[i].get_guests_number()) == nb:
                feats.append(1)
            else:
                feats.append(0)
        if int(recipes[i].get_guests_number()) > 10:
            feats.append(1)
        else:
            feats.append(0)

        new_recipe = np.append(recipe, feats)
        v_recipes.append(new_recipe)

    return v_recipes


def weight_recipe_with_score(v_recipe, score):

    return v_recipe*score

def get_best_k(v_liked_recipes) :

    best_sim = 0
    best_k = 0
    for i in range(2,10):
        kmeans = KMeans(n_clusters=i).fit(v_liked_recipes)
        centers =[x for x in kmeans.cluster_centers_]
        scores = []

        for recipe in v_liked_recipes:
            matrix = centers + recipe
            cos_matrix = cosine_similarity(matrix)
            score_best_sim = max(cos_matrix[0][1:])
            scores.append(score_best_sim)

        global_sim = sum(scores)
        if global_sim > best_sim:
            best_sim = global_sim
            best_k = i

    return best_k



