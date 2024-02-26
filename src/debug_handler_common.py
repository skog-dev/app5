#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  Programme python pour l'évaluation du code de détection des auteurs et de génération de textes
#
#
#  Copyright 2018-2024 F. Mailhot et Université de Sherbrooke
#

import sys
import traceback
import signal
import timeit


class DebugHandlerTimeOutException(Exception):
    """Cette classe définit un nouveau type d'exception, utilisé pour capturer les problèmes d'exécution trop longue
    dans le code étudiant

    Copyright 2024, F. Mailhot et Université de Sherbrooke
    """

    pass


class DebugHandler:
    """Classe à utiliser pour détecter et gérer les exceptions dans le code étudiant :

    Copyright 2024, F. Mailhot et Université de Sherbrooke
    """

    def __init__(self) -> None:
        self.student_cip = ""
        self.start_time: float = timeit.default_timer()
        self.timeout = 0
        return

    @staticmethod
    def print_debug_info() -> None:
        """Méthode statique pour indiquer où a eu lieu une exception :
            - Accède au "stack trace"
            - Imprime le type d'exception, la valeur, la ligne de code et une portion du "stack trace"

        Returns :
            void : Rien n'est retourné
        """
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print("Exception:", exc_type, ", Valeur:", exc_value, ", Trace:", exc_traceback)
        print("Ligne:", exc_traceback.tb_lineno)
        traceback.print_tb(exc_traceback, limit=5, file=sys.stdout)
        print("")
        return

    def set_student_cip(self, student_cip: str) -> None:
        """Méthode qui permet d'associer le(s) cip(s) au débogage du code courant

        Args :
            student_cip (str) : cip associé au code étudiant qui sera exécuté

        Returns :
            void : Rien n'est retourné
        """
        self.student_cip = student_cip
        return

    def set_start_time(self) -> None:
        """Temps de début de l'exécution du code étudiant.  Permet de mesurer approximativement la performance

        Args :
            void : Ne fait que mémoriser le temps courant

        Returns :
            void : Rien n'est retourné
        """
        self.start_time = (
            timeit.default_timer()
        )  # Permet de mesurer (approximativement) le temps d'exécution
        return

    def start_execution_timing(self) -> None:
        """Démarre le chronomètre pour identifier une exécution trop longue, conserve le temps de départ

        Args :
            void : Tout est compris dans l'objet

        Returns :
            void : Rien n'est retourné
        """
        if self.timeout > 0:
            self.start_timeout(
                self.timeout
            )  # Limite le temps d'exécution (le code de certains étudiants ne se termine pas
        self.set_start_time()
        return

    def stop_execution_timing(self) -> None:
        """Calcule le temps total d'exécution

        Args :
            void : L'objet est utilisé pour conserver le temps courant

        Returns :
            void : Rien n'est retourné
        """
        end_time = timeit.default_timer()
        print(
            f"\tcip: {self.student_cip} - Temps d'exécution: {end_time - self.start_time:.2f} secondes"
        )
        print("")
        return

    def timeout_handler(self, signum, frame) -> None:
        # https://www.programiz.com/python-programming/user-defined-exception
        raise DebugHandlerTimeOutException("Temps d'exécution trop long!")

    def print_timeout_exception(self) -> None:
        """Méthode pour imprimer l'info d'une exception de temps d'exécution trop grand

        Args :
            void : Tout est compris dans l'objet

        Returns :
            void : Rien n'est retourné
        """
        print(">=" * 75)
        print(
            f"\tcip:{self.student_cip} ===>>> TEMPS DE CALCUL TROP GRAND: plus de {self.timeout} secondes"
        )
        self.print_debug_info()
        print("<=" * 75)
        return

    def print_general_exception(self) -> None:
        """Méthode pour indiquer (imprimer) qu'une exception arbitraire a eu lieu :
            - L'information au sujet de l'exception (son type, la ligne de code où elle a eu lieu) sera imprimée

        Args :
            void : Tout est compris dans l'objet

        Returns :
            void : Rien n'est retourné
        """
        print("=" * 150)
        print(f"\tcip:{self.student_cip} ===>>> ERREUR D'EXÉCUTION")
        self.print_debug_info()
        print("=" * 150)
        return

    def start_timeout(self, timeout):
        """Démarre un décompte temporel (valeur en secondes dans timeout) :
            - Détecte du code qui prend trop de temps à s'exécuter

        Args :
            int : La valeur du délai

        Returns :
            void : Au retour, l'alarme est démarrée et sera déclenchée au besoin
        """
        self.timeout = timeout
        # https://stackoverflow.com/questions/366682/how-to-limit-execution-time-of-a-function-call
        signal.signal(signal.SIGALRM, self.timeout_handler)
        signal.alarm(timeout)
        return
