#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  Programme python pour l'évaluation du code de détection des auteurs et de génération de textes
#
#
#  Copyright 2018-2023 F. Mailhot et Université de Sherbrooke
#

import argparse
import copy
import importlib
import os.path
import sys
import timeit
from tabulate import tabulate
import debug_handler_common


class ParsingClassTextAn:
    def parse_cli(self) -> None:
        """Utilise le module argparse pour :
            - Enregistrer les commandes à reconnaître
            - Lire la ligne de commande et créer le champ self.args qui récupère la structure produite

        Returns :
            void : Au retour, toutes les commandes reconnues sont comprises dans self.args
        """
        parser = argparse.ArgumentParser(prog="textan_FORA1819_LEGM1303.py")

        parser.add_argument(
            "-d",
            default="TextesPourEtudiants",
            help="Répertoire contenant les sous-repertoires des auteurs \
                            (TextesPourEtudiants par défaut)",
        )
        parser.add_argument(
            "-a", help="Résultats à produire pour cet auteur spécifique"
        )
        parser.add_argument(
            "-f", help="Fichier inconnu pour lequel on recherche un auteur"
        )
        parser.add_argument(
            "-m",
            default=1,
            type=int,
            choices=range(1, 20),
            help="Mode (1 ou 2 ou 3 ou ... 20) - unigrammes ou digrammes ou trigrammes ou ...",
        )
        parser.add_argument(
            "-F",
            type=int,
            help="Indication du rang (en fréquence) du mot (ou n-gramme) a imprimer",
        )
        parser.add_argument(
            "-G",
            default=0,
            action="store_true",
            help="Génération de texte avec les statistiques de tous les auteurs",
        )
        parser.add_argument(
            "-Ga", help="Génération de texte avec les statistiques de cet auteur"
        )
        parser.add_argument(
            "-g_size", default=500, type=int, help="Taille du texte à générer"
        )
        parser.add_argument(
            "-g_base",
            default="Gen_text",
            help="Nom de base du fichier de texte à générer",
        )
        parser.add_argument(
            "-g_ext",
            default=".txt",
            help="Extension utilisée pour le fichier généré, .txt par défaut",
        )
        parser.add_argument(
            "-g_nocip",
            action="store_true",
            help="Ne pas utiliser les CIPs dans le nom du fichier généré",
        )
        parser.add_argument(
            "-g_noaut",
            action="store_true",
            help="Ne pas utiliser le nom de l'auteur dans le nom du fichier généré",
        )
        parser.add_argument(
            "-g_sep",
            default="_",
            help="Utiliser cette chaine de caractères comme séparateur dans le nom de fichier généré",
        )
        parser.add_argument(
            "-g_reformat",
            help="Indique que le reformattage doit être utilisé dans le texte généré",
        )

        parser.add_argument("-v", action="store_true", help="Mode verbose")
        parser.add_argument(
            "-noPonc", action="store_true", help="Retirer la ponctuation"
        )
        parser.add_argument(
            "-rep_code",
            default=".",
            help="Répertoire contenant la liste des CIPs et le code textan_FORA1819_LEGM1303.py",
        )
        parser.add_argument(
            "-recursion", help="Récursion maximale permise (par défaut, 1000)"
        )
        parser.add_argument("-r1", help="Retrait des mots de 1 caractère")
        parser.add_argument("-r2", help="Retrait des mots de 2 caractères")
        parser.add_argument(
            "-golden",
            help="Compare les résultats avec la version 'golden' indiquée par ce paramètre",
        )
        parser.add_argument(
            "-fichier_res", help="Tous les prints seront faits dans ce fichier"
        )
        parser.add_argument(
            "-dir_res",
            help="Tous les résultats seront ajoutés dans ce répertoire (sous le répertoire courant)",
        )
        parser.add_argument(
            "-timeout", help="Temps maximum (secondes) pour l'exécution du système"
        )
        parser.add_argument(
            "-compare_auteurs",
            action="store_true",
            help="Indique les proximités des textes des différents auteurs",
        )

        self.parser = parser
        self.args = parser.parse_args()
        return

    def setup_after_parse(self) -> None:
        """Utilise le champ args pour :
            - Définir tous les champs modifiables par la ligne de commande
            - Ouvrir un fichier de résultats (si demandé) et y rediriger stdout

        Returns :
            void : Au retour, toutes les commandes reconnues sont comprises dans self.args
        """
        if self.args.d:
            self.dir = self.args.d
        if self.args.noPonc:
            self.keep_punc = False
        if self.args.m:
            self.ngram = self.args.m
        if (self.args.G or self.args.Ga) and self.args.g_size > 0:
            self.gen_size = self.args.g_size
            self.gen_basename = self.args.g_base
            # if self.gen_size > 0:
            #     self.gen_text = True
            #     if self.args.g:
            #         self.gen_basename = self.args.g
            if self.args.g_ext:
                self.g_ext = self.args.g_ext
            if self.args.g_nocip:
                self.g_cip = False
            if self.args.g_noaut:
                self.g_aut = False
            if self.args.g_sep:
                self.g_sep = self.args.g_sep
            if self.args.Ga:
                self.auteur = self.args.Ga
                self.gen_text = True
            if self.args.G:
                self.gen_text_all = True

        if self.args.a:
            self.auteur = self.args.a
        if self.args.rep_code:
            self.rep_code = self.args.rep_code

        if self.args.f:
            self.oeuvre = self.args.f
            self.find_author = True
        if self.args.F:
            self.do_get_nth_ngram = True
            self.nth_ngram = self.args.F
        if self.args.r1:
            self.remove_word_1 = True
        if self.args.r2:
            self.remove_word_2 = True
        if self.args.timeout:
            self.timeout = int(self.args.timeout)
        if self.args.fichier_res:
            # https://stackoverflow.com/questions/5104957/how-do-i-create-a-file-at-a-specific-path
            cur_path = os.path.dirname(__file__)
            if self.args.dir_res:
                dir_res_path = os.path.relpath(self.args.dir_res, cur_path)
                try:  # https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-directory
                    os.mkdir(dir_res_path)
                except FileExistsError:
                    pass
            else:
                dir_res_path = cur_path
            output_file_path = os.path.join(dir_res_path, self.args.fichier_res)
            # Voir: https://stackoverflow.com/questions/4675728/redirect-stdout-to-a-file-in-python
            # et: https://stackoverflow.com/questions/3597480/how-to-make-python-3-print-utf8
            sys.stdout = open(output_file_path, "w", encoding="UTF-8", buffering=1)
        if self.args.recursion:
            sys.setrecursionlimit(int(self.args.recursion))
        if self.oeuvre:
            try:
                # https://docs.python.org/3/library/os.path.html#os.path.realpath
                # https://www.tutorialspoint.com/python/os_readlink.htm
                if not os.path.isfile(os.path.realpath(self.oeuvre)):
                    raise FileNotFoundError()
                else:
                    self.oeuvre = os.path.realpath(self.oeuvre)

            except FileNotFoundError:
                print("L'oeuvre ", self.oeuvre, " n'est pas accessible")
                self.debug_handler.print_debug_info()
                sys.exit(1)

        if self.args.compare_auteurs:
            self.do_check_auteur_distance = True
        return

    def setup_and_parse_cli(self) -> None:
        """Initialise l'objet en interprétant la ligne de commande :
            - Lit la ligne de commande
            - Modifie tous les champs qui y sont définis

        Returns :
            (void) : Au retour, toutes les commandes reconnues sont comprises dans self.args
        """
        self.parse_cli()
        self.setup_after_parse()
        return

    def __init__(self) -> None:
        """Constructeur pour la classe TestTextAn.  Initialisation de l'ensemble des éléments requis

        Args :
            (void) : Le constructeur lit la ligne de commande et ajuste l'état de l'objet TestTextAn en conséquence

        Returns :
            (void) : Au retour, la nouvelle instance de test est prête à être utilisée
        """
        self.parser: argparse.ArgumentParser = None
        self.args: argparse.Namespace = None

        self.dir = "."
        self.ngram = 1
        self.keep_punc = True
        self.gen_text = False
        self.gen_text_all = False
        self.gen_size = 0
        self.gen_basename = "Gen_text"
        self.cip = ""
        self.textan_module = ""
        self.golden_module = ""
        self.g_ext = ".txt"
        self.g_cip = True
        self.g_aut = True
        self.g_sep = "_"
        self.rep_code = "."
        self.auteur = ""
        self.oeuvre = ""
        self.find_author = False
        self.tests = []
        self.do_analyze = False
        self.do_get_nth_ngram = False
        self.remove_word_1 = False
        self.remove_word_2 = False
        self.analysis_result = {}
        self.nth_ngram = ""
        self.auteurs = []
        self.textan = None
        self.timeout = -1
        self.do_check_auteur_distance = False

        self.start_time = timeit.default_timer()
        self.debug_handler = debug_handler_common.DebugHandler()

        self.setup_and_parse_cli()
        self.check_and_setup_golden()
        self.debug_handler.timeout = self.timeout

        self.cips = []
        self.get_cips()

        self.add_cwd_to_sys_path()
        self.init_modules = {}

        self.check_something_to_do()
        return


class TestTextAn(ParsingClassTextAn):
    """Classe à utiliser pour valider la résolution de la problématique :

        - Contient tout le nécessaire pour tester la problématique.

    Pour valider la solution de la problématique, effectuer :
        - python test_textan.py -help
            + Indique tous les arguments et options disponibles

    Copyright 2018-2023, F. Mailhot et Université de Sherbrooke
    """

    @staticmethod
    def add_cwd_to_sys_path() -> None:
        """Ajoute le répertoire d'exécution local aux chemins utilisés par le système.
           Sinon, si test_textan.py est un lien symbolique, les fichiers textan_FORA1819_LEGM1303.py ne sont pas trouvés

        Args :
            (void) : Utilisation des informations système

        Returns :
            (void) : Au retour, le répertoire d'exécution est ajouté au chemin système
        """
        sys.path.append(os.getcwd())
        return

    @staticmethod
    def sort_author_distance(author_res: [str, float]) -> float:
        """Retourne le deuxième élément du vecteur (auteur, proximité) (utilisé pour le tri de la liste des auteurs)

        Args :
            ([str, float]) : Liste des auteurs et valeur de proximité avec le texte inconnu (résultat du produit scalaire)
            pour chacun des auteurs

        Returns :
            (float) : Valeur de la proximité de l'auteur avec le texte inconnu
        """
        return author_res[1]

    # Si mode verbose, refléter les valeurs des paramètres passés sur la ligne de commande
    def print_params(self) -> None:
        """Mode verbose, imprime l'ensemble des paramètres utilisés pour ce test :
            - Valeur des paramètres par défaut s'ils n'ont pas été modifiés sur la ligne de commande
            - Ensemble des tests demandés

        Returns :
            (void) : Ne fait qu'imprimer les valeurs contenues dans self
        """
        if not self.args.v:
            return

        print("Mode verbose: ", self.cip)

        if self.args.f:
            print("\tFichier inconnu à étudier: " + self.args.f)
        if self.oeuvre:
            print(f"\tChemin complet de l'oeuvre inconnue: {self.oeuvre}")

        print("\tCalcul avec des " + str(self.args.m) + "-grammes")

        if self.args.F:
            if self.args.F == 1:
                print("\tLe premier ngramme le plus fréquent sera trouvé")
            else:
                print(
                    "\tLe "
                    + str(self.args.F)
                    + "e ngramme le plus fréquent sera trouvé"
                )

        if self.args.a:
            print("\tAuteur étudié: " + self.args.a)

        if self.args.noPonc:
            print("\tRetrait des signes de ponctuation")
        else:
            print("\tConservation des signes de ponctuation")
        if self.remove_word_1:
            print("\tRetrait des mots de 1 lettre")
        else:
            print("\tConservation des mots de 1 lettre")
        if self.remove_word_2:
            print("\tRetrait des mots de 2 lettres")
        else:
            print("\tConservation des mots de 2 lettres")

        if self.args.G:
            print(
                "\tGénération d'un texte de "
                + str(self.args.G)
                + " mots, pour l'auteur: ",
                self.auteur,
            )
            print("\tLe nom du fichier généré sera: " + self.get_gen_file_name())

        if self.args.recursion:
            print("\tRécursion maximale: ", sys.getrecursionlimit())
        print("\tTemps d'exécution maximal: ", self.timeout, " secondes")

        print("\tCalcul avec les auteurs du répertoire: " + self.args.d)
        print("\tListe des auteurs: ", end="")
        self.auteurs.sort()
        for a in self.auteurs:
            aut = a.split("/")
            print("    " + aut[-1], end=" ")
        print("")
        if self.args.compare_auteurs:
            print("\tLa proximité des textes de l'ensemble des auteurs sera calculée")

        return

    def setup_instance_param(self) -> None:
        """Définit les paramètres de l'instance (étudiante) à tester

        Returns :
            (void) : Rien n'est retourné
        """
        # Ajout de l'information nécessaire dans l'instance à tester de la classe TextAn sous étude :
        #   Utilisation de la ponctuation (ou non), taille des n-grammes, répertoire des auteurs
        if self.args.noPonc:
            self.textan.set_ponc(False)
        else:
            self.textan.set_ponc(True)

        self.textan.set_ngram(self.ngram)
        self.textan.set_aut_dir(self.dir)
        self.textan.set_remove_word_1(self.remove_word_1)
        self.textan.set_remove_word_2(self.remove_word_2)

        self.auteurs = self.textan.auteurs
        self.print_params()  # Imprime l'état de l'instance (si le mode verbose a été utilisé sur la ligne de commande)
        return

    def get_gen_file_name(self) -> str:
        """Définit le nom du fichier à générer

        Returns :
            str : Nom du fichier à générer
        """
        name = self.gen_basename
        if self.g_cip:
            name = name + self.g_sep + self.cip
        if self.g_aut:
            name = name + self.g_sep + self.auteur
        if self.g_ext:
            name = name + self.g_ext
        return name

    def get_cips(self) -> None:
        """Lit le fichier etudiants.txt, trouve les CIPs, et retourne la liste
           Le CIP est obtenu du fichier etudiants.txt, dans le répertoire courant
            ou tel qu'indiqué en paramètre (option -rep_code)

        Returns :
            (void) : Au retour, tous les cips sont inclus dans la liste self.cips
        """
        cip_file = self.rep_code + "/etudiants.txt"
        cip_list = open(cip_file, "r")
        lines = cip_list.readlines()
        for line in lines:
            if "#" in line:
                continue
            if "%" in line:
                continue
            for student_cip in line.split():
                self.cips.append(student_cip)

        return

    def import_textan_cip(self, import_cip: str) -> None:
        """Importe le fichier textan_FORA1819_LEGM1303.py, où "CIP1_CIP2" est passé dans le paramètre import_cip

        Args :
            import_cip (str) : Contient "CIP1_CIP2", les cips pour le code à tester

        Returns :
            (void) : Au retour, le module textan_CIP1_CIP2 est importé et remplace le précédent
        """

        if "init_module" in self.init_modules:
            # Deuxième appel (ou subséquents) : enlever tous les modules supplémentaires
            for m in sys.modules.keys():
                if m not in self.init_modules:
                    del sys.modules[m]
        else:
            # Premier appel : identifier tous les modules déjà présents
            self.init_modules = sys.modules.keys()

        self.cip = import_cip
        textan_name = "textan_" + import_cip
        self.textan_module = importlib.import_module(textan_name)
        return

    def check_and_setup_golden(self) -> None:
        """Vérifie si une version "golden" doit être conservée

        Args :
            (void) : Le nom de la version "golden" est disponible dans le champ self.args

        Returns :
            (void) : Au retour, le champ golden_module est initialisé (si nécessaire)
        """

        if self.args.golden:
            self.golden_module = importlib.import_module(self.args.golden)
        else:
            self.golden_module = None
        return

    def check_something_to_do(self) -> None:
        """Vérifie que les paramètres d'entrée indiquent quelque chose à faire

        Args :
            (void) : Toute l'information nécessaire est présente dans l'objet

        Returns :
            (void) : Au retour, le champ something_to_do indique le statut.  S'il n'y a rien à faire, sortie
        """

        something_to_do = (
            self.gen_text_all | self.gen_text | self.find_author | self.do_get_nth_ngram
        )

        if not something_to_do:
            print("Aucune action à effectuer. Utiliser un paramètre pour:")
            print("\t - Générer un texte aléatoire")
            print("\t - Trouver l'auteur d'un texte inconnu")
            print("\t - Trouver le k-ième n-gramme le plus fréquent d'un auteur")
            print("")
            self.parser.print_help()
            exit()
        return

    def load_cip_code(self, student_cip: str) -> None:
        """Charge le code étudiant en mémoire, initialise l'instance, initialise le débogage

        Args :
            student_cip (str) : Cips de l'ensemble des membres de l'équipe d'APP
        Returns :
            (void) : Rien n'est retourné : au retour, le code étudiant a été chargé en mémoire
        """
        self.import_textan_cip(
            student_cip
        )  # Chargement du code des étudiants identifiés par cip
        self.textan = self.textan_module.TextAn()
        self.setup_instance_param()
        self.debug_handler.start_execution_timing()  # Permet de mesurer le temps d'exécution du code étudiant
        self.debug_handler.set_student_cip(
            student_cip
        )  # Indique le cip courant au gestionnaire de débogage
        return

    def analyze(self) -> None:
        """Effectue l'analyse des textes fournis (calcul des fréquences pour chacun des auteurs) avec le code étudiant

        Returns :
            (void) : Rien n'est retourné : au retour, les textes des auteurs ont été analysés
        """
        self.textan.analyze()
        return

    def generate(self) -> None:
        """Effectue la génération d'un texte aléatoire suivant les statistiques d'un certain auteur (code étudiant)

        Returns :
            (void) : Rien n'est retourné : au retour, un texte aléatoire a été généré, basé sur les statistiques
                        d'un seul auteur, ou de l'ensemble des auteurs
        """
        if self.gen_text:
            filename = self.get_gen_file_name()
            self.textan.gen_text_auteur(self.auteur, self.gen_size, filename)
        elif self.gen_text_all:
            filename = self.get_gen_file_name()
            self.textan.gen_text_all(self.gen_size, filename)
        return

    def find(self) -> None:
        """Calcule la proximité d'un certain texte inconnu avec le "style" de chacun des auteurs avec le code étudiant

        Returns :
            (void) : Rien n'est retourné : au retour, le texte inconnu a été comparé aux textes des auteurs
        """
        if self.find_author:
            self.analysis_result = self.textan.find_author(self.oeuvre)

            self.analysis_result.sort(key=self.sort_author_distance, reverse=True)
            print("")
            print(f'\tcip: {self.cip} - Fréquences pour l\'oeuvre "{self.oeuvre}": ')
            print("\t\t--> ", end="")
            # https://stackoverflow.com/questions/493386/how-to-print-without-a-newline-or-space
            for item in self.analysis_result:
                print(f"{item[0]}:{item[1]:.4f} ", end="")
            print("")
        return

    def get_nth_ngram(self) -> None:
        """Obtient le n-ième plus fréquent n-gramme d'un certain auteur avec le code étudiant

        Returns :
            (void) : Rien n'est retourné : au retour, le n-ième n-gramme le plus fréquent a été imprimé
        """
        if self.do_get_nth_ngram:
            if self.auteur == "":
                print(
                    "\tPas d'auteur indiqué: impossible de donner le n-ième n-gramme.  Utiliser -a nom_de_l_auteur"
                )
                return
            nth_ngram = self.textan.get_nth_element(self.auteur, self.nth_ngram)
            print(f"\tcip: {self.cip} - Auteur: {self.auteur}:")
            print(
                f'\t\t{self.nth_ngram}e n-gramme de {self.ngram} mot{"s"[:self.ngram > 1]}: {nth_ngram}'
            )
        return

    def check_auteur_distance(self) -> None:
        """Calcule et imprime la proximité entre chacun des auteurs (nombre entre 0 et 1)

        Returns :
            void : Rien n'est retourné : au retour, la distance entre les différents auteurs a été imprimée
        """
        if (
            not self.do_check_auteur_distance
        ):  # Par défaut de calcul n'est pas fait.  Utiliser -compare_auteurs
            return

        res_table = []
        auteur_list = []
        res_table.append(
            auteur_list
        )  # La première ligne du tableau de résultats contiendra la liste des auteurs
        auteur_list.append("")
        res_buffer = (
            {}
        )  # Tampon pour conserver les valeurs de proximité d'auteurs déjà calculées
        for auteur1 in self.auteurs:
            auteur_res = []
            res_table.append(auteur_res)
            auteur_list.append(auteur1)
            auteur_res.append(auteur1)
            for auteur2 in self.auteurs:
                auteurs_key = tuple(
                    sorted((auteur1, auteur2))
                )  # Conserver la valeur pour éviter de refaire le calcul
                if auteurs_key in res_buffer:
                    distance = res_buffer[auteurs_key]
                else:
                    distance = self.textan.dot_product_aut(auteur1, auteur2)
                    res_buffer[auteurs_key] = distance
                auteur_res.append(distance)

        print("\n Comparaison des auteurs:")
        # https://learnpython.com/blog/print-table-in-python/
        print(tabulate(res_table, headers="firstrow", tablefmt="fancy_grid"))
        return

    def __init__(self) -> None:
        """Constructeur pour la classe TestTextAn.  Initialisation de l'ensemble des éléments requis

        Args :
            (void) : Le constructeur lit la ligne de commande et ajuste l'état de l'objet TestTextAn en conséquence

        Returns :
            (void) : Au retour, la nouvelle instance de test est prête à être utilisée
        """

        super().__init__()

        return


def main() -> None:
    """Démarrage de l'exécution du code de la problématique, pour l'ensemble des équipes :
        - Initialise une instance de test
        - Pour chaque équipe (séquence de cips) :
            - Lire le code fourni par l'équipe
            - Invoquer la méthode d'analyse de texte de l'équipe
            - Invoquer la méthode de génération de texte aléatoire
            - Calculer la proximité d'un texte aléatoire avec les textes des auteurs fournis
            - Trouver le n-ième ngramme le plus fréquent pour un certain auteur
            - Trouver la distance entre les oeuvres des différents auteurs
        - Si le code est trop long à s'exécuter (par défaut, 2 minutes), interrompre l'exécution
        - Attrape toutes les exceptions non-traitées dans le code étudiant

    Args :
        (void) : Tout ce qui est nécessaire est défini à l'intérieur de la méthode

    Returns :
        (void) : Au retour, l'exécution est terminée
    """
    golden_tta = TestTextAn()  # Initialisation de l'instance de test

    for (
        cip
    ) in (
        golden_tta.cips
    ):  # Permet de tester le code d'une ou plusieurs équipes, à tour de rôle
        tta = copy.deepcopy(
            golden_tta
        )  # Copie fraiche de l'objet, pour isoler les instances des étudiants

        try:
            tta.load_cip_code(cip)  # Chargement et configuration du code étudiant
            tta.textan.analyze()  # Analyse des textes des auteurs (code étudiant)
            tta.generate()  # Produit un texte aléatoire avec les mêmes statistiques que l'auteur choisi (code étudiant)
            tta.find()  # Calcul de proximité entre un texte inconnu et l'ensemble des auteurs (code étudiant)
            tta.get_nth_ngram()  # Trouve le n-ième n-gramme le plus fréquent d'un certain auteur (code étudiant)
            tta.check_auteur_distance()

        # Si le code étudiant est trop lent (120 secondes par défaut), interrompre
        except debug_handler_common.DebugHandlerTimeOutException:
            tta.debug_handler.print_timeout_exception()

        # Mauvaise pratique (attraper toutes les exceptions), mais nécessaire ici, pour du code étudiant inconnu
        except Exception as e:
            tta.debug_handler.print_general_exception()

        tta.debug_handler.stop_execution_timing()  # Mesure le temps d'exécution du code étudiant

    if (
        golden_tta.args.fichier_res
    ):  # stdout a été redirigé vers un fichier ; le fermer pour ne rien perdre
        sys.stdout.close()

    return


if __name__ == "__main__":
    main()
