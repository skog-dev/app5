#!/usr/bin/env python3
# -*- coding: utf-8 -*-


""" Ce fichier contient la classe TextAn, à utiliser pour résoudre la problématique.
    C'est un gabarit pour l'application de traitement des fréquences de mots dans les oeuvres d'auteurs divers.

    Les méthodes apparaissant dans ce fichier définissent une API qui est utilisée par l'application
    de test test_textan.py
    Les paramètres d'entrée et de sortie (Application Programming Interface, API) sont définis,
    mais le code est à écrire au complet.
    Vous pouvez ajouter toutes les méthodes et toutes les variables nécessaires au bon fonctionnement du système

    La classe TextAn est invoquée par la classe TestTextAn (contenue dans test_textan.py) :

        - Tous les arguments requis sont présents et accessibles dans args (dans le fichier test_textan.py)
        - Note : vous pouvez tester votre code en utilisant les commandes :
            + "python test_textan.py"
            + "python test_textan.py -h" (donne la liste des arguments possibles)
            + "python test_textan.py -v" (mode "verbose", qui indique les valeurs de tous les arguments)

    Copyright 2018-2023, F. Mailhot et Université de Sherbrooke
"""
import math
import string

from textan_common import TextAnCommon


class TextAn(TextAnCommon):
    """Classe à utiliser pour coder la solution à la problématique :

        - La classe héritée TextAnCommon contient certaines fonctions de base pour faciliter le travail :
            - recherche des auteurs
            - ouverture des répertoires
            - et autres (voir la classe TextAnCommon pour plus d'information)
            - La classe ParsingClassTextAn est héritée par TextAnCommon et lit la ligne de commande
        - Les interfaces du code à développer sont présentes, mais tout le code est à écrire
        - En particulier, il faut compléter les fonctions suivantes :
            - dot_product_dict (dict1, dict2)
            - dot_product_aut (auteur1, auteur2)
            - doct_product_dict_aut (dict, auteur)
            - find_author (oeuvre)
            - gen_text (auteur, taille, textname)
            - get_nth_element (auteur, n)
            - analyze()

    Copyright 2018-2023, F. Mailhot et Université de Sherbrooke
    """

    # Signes de ponctuation à retirer (compléter cette liste incomplète)
    PONC = ["!"]

    def __init__(self) -> None:
        """Initialize l'objet de type TextAn lorsqu'il est créé

        Args :
            (void) : Utilise simplement les informations fournies dans la classe TextAnCommon

        Returns :
            (void) : Ne fait qu'initialiser l'objet de type TextAn
        """

        # Initialisation des champs nécessaires aux fonctions fournies
        super().__init__()

        # Au besoin, ajouter votre code d'initialisation de l'objet de type TextAn lors de sa création

        return

    # Ajouter les structures de données et les fonctions nécessaires à l'analyse des textes,
    #   la production de textes aléatoires, la détection d'oeuvres inconnues,
    #   l'identification des n-ièmes mots les plus fréquents
    #
    # If faut coder les fonctions find_author(), gen_text(), get_nth_element() et analyse()
    # La fonction analyse() est appelée en premier par test_textan.py
    # Ensuite, selon ce qui est demandé, les fonctions find_author(), gen_text() ou get_nth_element() sont appelées

    def load_text_aut(self, auteur: str):
        for file in self.get_aut_files(auteur):
            self.mots_auteurs[auteur].update(self.load_text(file))

        self.taille_mots[auteur] = len(self.mots_auteurs[auteur])

    def load_text(self, path: str):
        with open(path, "r", encoding="utf-8") as f:
            buffer = f.read().translate(str.maketrans("", "", "!()*,.:;?«»")).split()
        f.close()

        mots = {}
        ngrams = []

        for i in range(len(buffer) - self.ngram):
            ngrams.append(tuple(buffer[i:i + self.ngram]))

        for ngram in ngrams:
            if ngram in mots:
                mots[ngram] += 1
            else:
                mots[ngram] = 1

        return mots

    @staticmethod
    def normalize_dict(vector: dict) -> dict:
        val = 0
        for key in vector.keys():
            val += vector[key] ** 2

        norm = math.sqrt(val)

        for key in vector.keys():
            vector[key] /= norm

        return vector

    @staticmethod
    def dot_product_dict(
            dict1: dict, dict2: dict, dict1_size: int, dict2_size: int
    ) -> float:
        """Calcule le produit scalaire NORMALISÉ de deux vecteurs représentés par des dictionnaires

        Args :
            dict1 (dict) : le premier vecteur
            dict2 (dict) : le deuxième vecteur

        Returns :
            dot_product (float) : Le produit scalaire normalisé de deux vecteurs

        Copyright 2023, F. Mailhot et Université de Sherbrooke
        """

        # Les lignes qui suivent ne servent qu'à éliminer un avertissement.
        # Il faut les retirer et les remplacer par du code fonctionnel

        dot_product = 0.0

        dict1 = TextAn.normalize_dict(dict1)
        dict2 = TextAn.normalize_dict(dict2)

        for key1, key2 in zip(dict1, dict2):
            dot_product += dict1[key1] * dict2[key2]

        # TODO : Implement dot_product_dict
        # dot_product = 1.0
        # print(dict1_size, dict2_size)
        # if dict1 != dict2:
        #     dot_product = 0.0

        return dot_product

    def dot_product_aut(self, auteur1: str, auteur2: str) -> float:
        """Calcule le produit scalaire normalisé entre les oeuvres de deux auteurs, en utilisant dot_product_dict()

        Args :
            auteur1 (str) : le nom du premier auteur
            auteur2 (str) : le nom du deuxième auteur

        Returns :
            dot_product (float) : Le produit scalaire normalisé des n-grammes de deux auteurs

        Copyright 2023, F. Mailhot et Université de Sherbrooke
        """

        # Les lignes qui suivent ne servent qu'à éliminer un avertissement.
        # Il faut les retirer et les remplacer par du code fonctionnel

        self.load_text_aut(auteur1)
        self.load_text_aut(auteur2)

        dot_product = self.dot_product_dict(
            self.mots_auteurs[auteur1], self.mots_auteurs[auteur2], self.taille_mots[auteur1], self.taille_mots[auteur2]
        )

        # TODO : Implement dot_product_aut
        # dot_product = 0.0
        # print(self)
        # if auteur1 == auteur2:
        #     print(auteur1, auteur2)
        #     dot_product = 1.0

        return dot_product

    def dot_product_dict_aut(self, dict_oeuvre: dict, auteur: str) -> float:
        """Calcule le produit scalaire normalisé entre une oeuvre inconnue et les oeuvres d'un auteur,
           en utilisant dot_product_dict()

        Args :
            dict_oeuvre (dict) : la liste des n-grammes d'une oeuvre inconnue
            auteur (str) : le nom d'un auteur

        Returns :
            dot_product (float) : Le produit scalaire normalisé des n-grammes de deux auteurs

        Copyright 2023, F. Mailhot et Université de Sherbrooke
        """

        # Les lignes qui suivent ne servent qu'à éliminer un avertissement.
        # Il faut les retirer et les remplacer par du code fonctionnel

        self.load_text_aut(auteur)

        dot_product = self.dot_product_dict(
            dict_oeuvre, self.mots_auteurs[auteur], len(dict_oeuvre), self.taille_mots[auteur]
        )

        # TODO : Implement dot_product_dict_aut
        # dot_product = 0.0
        # print(self)
        # if auteur in dict_oeuvre:
        #     print(dict_oeuvre)
        #     print(auteur)
        #     dot_product = 1.0

        return dot_product

    def find_author(self, oeuvre: str) -> []:
        """Après analyse des textes d'auteurs connus, retourner la liste d'auteurs
            et le niveau de proximité (un nombre entre 0 et 1) de l'oeuvre inconnue
            avec les écrits de chacun d'entre eux

        Args :
            oeuvre (str) : Nom du fichier contenant l'oeuvre d'un auteur inconnu

        Returns :
            resultats (Liste[(string, float)]) : Liste de tuples (auteurs, niveau de proximité),
            où la proximité est un nombre entre 0 et 1)
        """

        # Les lignes suivantes ne servent qu'à éliminer un avertissement.
        # Il faut les retirer lorsque le code est complété

        resultats = []

        for auteur in self.auteurs:
            resultats.append((auteur, self.dot_product_dict_aut(self.load_text(oeuvre), auteur)))

        # TODO : Implement find_author
        # print(self.auteurs, oeuvre)
        # resultats = [
        #     ("Premier_auteur", 0.1234),
        #     ("Deuxième_auteur", 0.1123),
        # ]  # Exemple du format des sorties

        # Ajouter votre code pour déterminer la proximité du fichier passé en paramètre avec chacun des auteurs
        # Retourner la liste des auteurs, chacun avec sa proximité au fichier inconnu
        # Plus la proximité est grande, plus proche l'oeuvre inconnue est des autres écrits d'un auteur
        #   Le produit scalaire entre le vecteur représentant les oeuvres d'un auteur
        #       et celui associé au texte inconnu pourrait s'avérer intéressant...
        #   Le produit scalaire devrait être normalisé avec la taille du vecteur associé au texte inconnu :
        #   proximité = (A dot product B) / (|A| |B|)   où A est le vecteur du texte inconnu et B est celui d'un auteur,
        #           "dot product" est le produit scalaire, et |X| est la norme (longueur) du vecteur X

        return resultats

    def gen_text_all(self, taille: int, textname: str) -> None:
        """Après analyse des textes d'auteurs connus, produire un texte selon des statistiques de l'ensemble des auteurs

        Args :
            taille (int) : Taille du texte à générer
            textname (str) : Nom du fichier texte à générer.

        Returns :
            void : ne retourne rien, le texte produit doit être écrit dans le fichier "textname"
        """

        # Ce print ne sert qu'à éliminer un avertissement. Il doit être retiré lorsque le code est complété
        # TODO : Implement gen_text_all
        print(self.auteurs, taille, textname)

        return

    def gen_text_auteur(self, auteur: str, taille: int, textname: str) -> None:
        """Après analyse des textes d'auteurs connus, produire un texte selon des statistiques d'un auteur

        Args :
            auteur (str) : Nom de l'auteur à utiliser
            taille (int) : Taille du texte à générer
            textname (str) : Nom du fichier texte à générer.

        Returns :
            void : ne retourne rien, le texte produit doit être écrit dans le fichier "textname"
        """

        # Ce print ne sert qu'à éliminer un avertissement. Il doit être retiré lorsque le code est complété
        # TODO : Implement gen_text_auteur
        print(self.auteurs, auteur, taille, textname)

        return

    def get_nth_element(self, auteur: str, n: int) -> [[str]]:
        """Après analyse des textes d'auteurs connus, retourner le n-ième plus fréquent n-gramme de l'auteur indiqué

        Args :
            auteur (str) : Nom de l'auteur à utiliser
            n (int) : Indice du n-gramme à retourner

        Returns :
            ngram (List[Liste[string]]) : Liste de liste de mots composant le n-gramme recherché
            (il est possible qu'il y ait plus d'un n-gramme au même rang)
        """
        # Les lignes suivantes ne servent qu'à éliminer un avertissement.
        # Il faut les retirer lorsque le code est complété

        if auteur not in self.mots_auteurs:
            self.load_text_aut(auteur)

        ngram = sorted(self.mots_auteurs[auteur].items(), key=lambda x: x[1], reverse=True)[n][0]

        # TODO : Implement get_nth_element
        # print(self.auteurs, auteur, n)
        # ngram = [["un", "roman"]]  # Exemple du format de sortie d'un bigramme

        return ngram

    def analyze(self) -> None:
        """Fait l'analyse des textes fournis, en traitant chaque oeuvre de chaque auteur

        Args :
            void : toute l'information est contenue dans l'objet TextAn

        Returns :
            void : ne retourne rien, toute l'information extraite est conservée dans des structures internes
        """

        # Ajouter votre code ici pour traiter l'ensemble des oeuvres de l'ensemble des auteurs
        # Pour l'analyse :  faire le calcul des fréquences de n-grammes pour l'ensemble des oeuvres
        #   d'un certain auteur, sans distinction des oeuvres individuelles,
        #       et recommencer ce calcul pour chacun des auteurs
        #   En procédant ainsi, les oeuvres comprenant plus de mots auront un impact plus grand sur
        #   les statistiques globales d'un auteur.
        # Il serait possible de considérer chacune des oeuvres d'un auteur comme ayant un poids identique.
        #   Pour ce faire, il faudrait faire les calculs de fréquence pour chacune des oeuvres
        #       de façon indépendante, pour ensuite les normaliser (diviser chaque vecteur par sa norme),
        #       avant de les additionner pour obtenir le vecteur complet d'un auteur
        #   De cette façon, les mots d'un court poème auraient une importance beaucoup plus grande que
        #   les mots d'une très longue oeuvre du même auteur. Ce n'est PAS ce qui vous est demandé ici.

        # Ces trois lignes ne servent qu'à éliminer un avertissement. Il faut les retirer lorsque le code est complété
        # TODO : Implement analyze

        ngram = self.get_empty_ngram(2)
        print(ngram)
        print(self.auteurs)

        return
