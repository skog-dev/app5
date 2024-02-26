#!/usr/bin/env python3
# -*- coding: utf-8 -*-


""" Ce fichier contient la classe TextAnCommon, utilisée pour la résolution de la problématique.
    Ce code ne devrait pas être modifié, il contient des méthodes utiles qui sont utilisées dans le gabarit de solution

    Les méthodes apparaissant dans ce fichier définissent des fonctionnalités de base qui sont utilisées dans
    la classe TextAn.

    La classe TextAn est invoquée par la classe TestTextAn (contenue dans test_textan.py) :

        - Tous les arguments requis sont présents et accessibles dans args (dans le fichier test_textan.py)
        - Note : vous pouvez tester votre code en utilisant les commandes :
            + "python test_textan.py"
            + "python test_textan.py -h" (donne la liste des arguments possibles)
            + "python test_textan.py -v" (mode "verbose", qui indique les valeurs de tous les arguments)

    Copyright 2018-2023, F. Mailhot et Université de Sherbrooke
"""

import os
import glob
import ntpath


class TextAnCommon:
    # Le code qui suit est fourni pour vous faciliter la vie.  Il n'a pas à être modifié
    # Signes de ponctuation à retirer (compléter la liste qui ne comprend que "!" au départ)
    # Modifier cette liste dans votre code (textan_FORA1819_LEGM1303.py)
    PONC = ["!"]

    def set_ponc(self, value):
        """Détermine si les signes de ponctuation sont conservés (True) ou éliminés (False)

        Args :
            value (boolean) : Conserve la ponctuation (Vrai) ou élimine la ponctuation (Faux)

        Returns :
            void : ne fait qu'assigner la valeur du champ keep_ponc

        Copyright 2018-2023, F. Mailhot et Université de Sherbrooke
        """
        self.keep_ponc = value
        return

    def print_ponc(self):
        """Imprime la liste des signes de ponctuation considérés

        Args :
            None

        Returns :
            void : ne fait qu'imprimer la liste des signes de ponctuation

        Copyright 2018-2023, F. Mailhot et Université de Sherbrooke
        """
        print("Signes de ponctuation à retirer: ", self.PONC)
        return

    @staticmethod
    def get_empty_ngram(size):
        """Retourne un ngramme vide de la taille indiquée (liste contenant des chaînes de caractères vides)

        Args :
            size (int) : le nombre de mots vides dans la liste ngramme

        Returns :
            ngram (liste) : La liste de mots vides

        Copyright 2023, F. Mailhot et Université de Sherbrooke
        """
        ngram = [""] * size
        return ngram

    def set_auteurs(self):
        """Obtient la liste des auteurs, à partir du répertoire qui les contient tous

        Note : le champ self.rep_aut doit être prédéfini :
            - Par défaut, il contient le répertoire d'exécution du script
            - Peut être redéfini par la méthode set_aut_dir

        Returns :
            void : ne fait qu'obtenir la liste des répertoires d'auteurs et modifier la liste self.auteurs

        Copyright 2018-2023, F. Mailhot et Université de Sherbrooke
        """
        files = self.rep_aut + "/*"
        full_path_auteurs = glob.glob(files)
        self.mots_auteurs = {}
        for auteur_path in full_path_auteurs:
            auteur = ntpath.basename(auteur_path)
            self.auteurs.append(auteur)
            self.mots_auteurs[auteur] = {}
            self.taille_mots[auteur] = 0
        return

    def set_aut_dir(self, aut_dir):
        """Définit le nom du répertoire qui contient l'ensemble des répertoires d'auteurs

        Note : L'appel à cette méthode extrait la liste des répertoires d'auteurs et les ajoute à self.auteurs

        Args :
            aut_dir (string) : Nom du répertoire (peut être absolu ou bien relatif au répertoire d'exécution)

        Returns :
            void : ne fait que définir le nom du répertoire qui contient les répertoires d'auteurs

        Copyright 2018-2023, F. Mailhot et Université de Sherbrooke
        """
        cwd = os.getcwd()
        if os.path.isabs(aut_dir):
            self.rep_aut = aut_dir
        else:
            self.rep_aut = os.path.join(cwd, aut_dir)

        self.rep_aut = os.path.normpath(self.rep_aut)
        self.set_auteurs()

        return

    def get_aut_files(self, auteur):
        """Obtient la liste des fichiers (avec le chemin complet) des oeuvres d'un auteur

        Args :
            auteur (string) : le nom de l'auteur dont on veut obtenir la liste des oeuvres

        Returns :
            oeuvres (Liste[string]) : liste des oeuvres (avec le chemin complet pour y accéder)

        Copyright 2018-2023, F. Mailhot et Université de Sherbrooke
        """
        auteur_dir = self.rep_aut + "/" + auteur + "/*"
        oeuvres = glob.glob(auteur_dir)
        return oeuvres

    def set_ngram(self, ngram):
        """Indique que l'analyse et la génération de texte se fera avec des n-grammes de taille ngram

        Args :
            ngram (int) : Indique la taille des n-grammes (1, 2, 3, ...)

        Returns :
            void : ne fait que mettre à jour le champ ngram

        Copyright 2018-2023, F. Mailhot et Université de Sherbrooke
        """
        self.ngram = ngram
        return

    def set_remove_word_1(self, remove_word_1):
        """Indique que l'analyse et la génération de texte n'utilisera pas les mots de 1 seule lettre

        Args :
            remove_word_1 (bool) : Vrai : retrait des mots de 1 lettre

        Returns :
            void : ne fait que mettre à jour le champ remove_word_1

        Copyright 2018-2023, F. Mailhot et Université de Sherbrooke
        """
        self.remove_word_1 = remove_word_1
        return

    def set_remove_word_2(self, remove_word_2):
        """Indique que l'analyse et la génération de texte n'utilisera pas les mots de 2 lettres

        Args :
            remove_word_2 (bool) : Vrai : retrait des mots de 2 lettres

        Returns :
            void : ne fait que mettre à jour le champ remove_word_2

        Copyright 2018-2023, F. Mailhot et Université de Sherbrooke
        """
        self.remove_word_2 = remove_word_2
        return

    def __init__(self):
        """Initialize l'objet de type TextAn lorsqu'il est créé

        Args :
            void : Utilise simplement les informations fournies dans l'objet Textan_config

        Returns :
            void : ne fait qu'initialiser l'objet de type TextAn

        Copyright 2018-2023, F. Mailhot et Université de Sherbrooke
        """

        # Initialisation des champs nécessaires aux fonctions fournies
        self.keep_ponc = True
        self.remove_word_1 = False
        self.remove_word_2 = False
        self.rep_aut = os.getcwd()
        self.auteurs = []
        self.ngram = 1
        self.mots_auteurs = {}
        self.taille_mots = {}
        return
