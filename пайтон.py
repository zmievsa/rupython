#!/usr/bin/env python3

"""
Keywords are translated from Russian to English/Python by a function in this file.
A "Russian Python" file is recognize by its .pyru extension.
"""
import os
import sys
from pathlib import Path

import token_utils
from ideas import import_hook
import importlib


ru_to_py = {
    "Ложь": "False",
    "Ничто": "None",
    "Истина": "True",
    "и": "and",
    "как": "as",
    "проверить": "assert",
    "асинхронный": "async",  # do not translate
    "подождать": "await",  # as these are not for beginners
    "прекратить": "break",
    "класс": "class",
    "продолжить": "continue",
    "функция": "def",
    "удалить": "del",
    "иначе_если": "elif",
    "иначе": "else",
    "исключение": "except",
    "в_конце": "finally",
    "для": "for",
    "из": "from",
    "глобальный": "global",
    "если": "if",
    "импорт": "import",
    "в": "in",
    "является": "is",
    "лямбда": "lambda",
    "нелокальный": "nonlocal",
    "не": "not",
    "или": "or",
    "пропустить": "pass",
    "выкинуть": "raise",
    "вернуть": "return",
    "попробовать": "try",
    "пока": "while",
    "с": "with",
    "передать": "yield",
    # a few builtins useful for beginners
    "ввод": "input",
    "напечатать": "print",
    "ряд": "range",
    "выйти": "exit",  # useful for console
    "Ошибка": "Exception",
    "число": "float",
}


def print_info(kind, source):
    """Prints the source code.
    ``kind`` is usually either ``"Original"`` or ``"Transformed"``
    """
    print(f"==========={kind}============")
    print(source)
    print("-----------------------------")


def transform_source(source, callback_params=None, **kwargs):
    """This function is called by the import hook loader and is used as a
    wrapper for the function where the real transformation is performed.
    """
    if callback_params is not None:
        if callback_params["show_original"]:
            print_info("Original", source)

    source = russian_to_english(source)

    if callback_params is not None:
        if callback_params["show_transformed"]:
            print_info("Transformed", source)

    return source


def russian_to_english(source):
    """A simple replacement of 'Russian Python keyword' by their normal
    English version.
    """
    new_tokens = []
    for token in token_utils.tokenize(source):
        if token.string in ru_to_py:
            token.string = ru_to_py[token.string]
        new_tokens.append(token)

    new_source = token_utils.untokenize(new_tokens)
    return new_source


def add_hook(show_original=False, show_transformed=False, verbose_finder=False):
    """Creates and adds the import hook in sys.meta_path"""
    callback_params = {
        "show_original": show_original,
        "show_transformed": show_transformed,
    }
    hook = import_hook.create_hook(
        transform_source=transform_source,
        callback_params=callback_params,
        hook_name=__name__,
        extensions=[".pyru"],
        verbose_finder=verbose_finder,
    )
    return hook


path = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(path.parent))
os.chdir(path.parent)
add_hook()
importlib.import_module(path.stem)
