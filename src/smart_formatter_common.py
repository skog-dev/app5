#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
    Utilitaire pour imprimer les commentaires d'aide sur plusieurs lignes (dans argparse)

    Note :
        - La classe SmartFormatter permet d'imprimer correctement la chaîne de caractère "help" lorsqu'elle débute par "R|"

    Copyright 2024, Frédéric Mailhot et Université de Sherbrooke

"""

import argparse


class SmartFormatter(argparse.HelpFormatter):
    """Classe destinée à formatter l'affichage des messages d'aide de argparse

        - Méthode incluse : _split_lines, qui remplace ce qui est fourni par défaut par argparse

"""

    def _split_lines(self, text: str, width: int):
        if text.startswith('R|'):
            return text[2:].splitlines()
            # this is the RawTextHelpFormatter._split_lines
        return argparse.HelpFormatter._split_lines(self, text, width)
