#!/usr/bin/python

# SPDX-FileCopyrightText: Coelacanthus
# SPDX-License-Identifier: MPL-2.0

import itertools
from typing import Dict, List, TextIO, Iterable

header: str = """/* ==UserStyle==
@name           Enable Iosevka language-specific ligation sets
@version        1.0.0
@description    Enable Iosevka language-specific ligation sets for code elements.
@namespace      Coelacanthus
@homepageURL    https://github.com/CoelacanthusHex/userstyles
@supportURL     https://github.com/CoelacanthusHex/userstyles/issues
@author         Coelacanthus
@license        MPL-2.0
SPDX-FileCopyrightText: Coelacanthus
SPDX-License-Identifier: MPL-2.0
==/UserStyle== */
@-moz-document regexp(".*") {
    /* https://github.com/be5invis/Iosevka/blob/main/doc/language-specific-ligation-sets.md */
"""

languages: Dict[str, List[str]] = {
    # TODO: Consider let Java and Kotlin use C-like ligation?
    # TODO: Consider let all languages mentioned in [1] use C-like ligation?
    #       [1]: https://en.wikipedia.org/wiki/List_of_C-family_programming_languages
    "CLIK": ["c", "cpp", "cc", "c++", "h++", "hpp", "hh", "hxx", "cxx"],
    "JSPT": [
        "javascript",
        "js",
        "jsx",
        "mjs",
        "cjs",
        "typescript",
        "ts",
        "tsx",
        "mts",
        "cts",
    ],
    "PHPX": ["php"],
    "JLIA": ["julia"],
    # TODO: Consider let Perl and Ruby use Raku ligation?
    "RAKU": ["raku"],
    "MLXX": ["sml", "smlnj", "ml"],
    # TODO: Is "fs" distinguishable between F# and F*?
    "FSHP": ["fsharp", "fs", "f#"],
    "FSTA": ["fstar"],
    # TODO: Consider let Agda use Haskell or Idris ligation?
    "HSKL": ["haskell", "hs"],
    "IDRS": ["idris", "idr"],
    "ELMX": ["elm"],
    "PURS": ["purescript", "purs"],
    "SWFT": ["swift"],
    "DFNY": ["dafny"],
    "COQX": ["coq"],
    "MTLB": ["matlab"],
    "WFLM": ["mathematica", "mma", "wl"],
    "VRLG": ["verilog", "v", "sv", "svh"],
    # TODO: Consider choose a ligation for Scala.
}

class_keywords_before: List[str] = [
    "highlighted",
    "language",
    "mw-highlight-lang",
    "shj-lang",
    "highlight-source",
]
class_keywords_after: List[str] = ["file-line"]
attribute_keywords: List[str] = ["data-langdata-language"]
combine_classes: List[str] = ["hljs", "highlight"]


def write_rule(file: TextIO, selectors: Iterable[str], tag: str) -> None:
    selector = ", ".join(selectors)
    file.write(f"    :is({selector}) :is(pre, code, textarea),\n")
    file.write(f"    :is(pre, code):is({selector}) {{\n")
    file.write(f'        font-feature-settings: "calt" off, "{tag}" on;\n')
    file.write("    }\n")


def main():
    with open("Enable-Iosevka-language-specific-ligation-sets.user.css", "w") as file:
        file.write(header)
        for tag, lang in languages.items():
            selectors_class_keyword_before = map(
                lambda x: f'[class~="{x}" i]',
                map(
                    lambda x: "-".join(x),
                    itertools.product(class_keywords_before, lang),
                ),
            )
            selectors_class_keyword_after = map(
                lambda x: f'[class~="{x}" i]',
                map(
                    lambda x: "-".join(x), itertools.product(lang, class_keywords_after)
                ),
            )
            selectors_attribute_keyword = map(
                lambda x: f'[{x[0]}~="{x[1]}" i]',
                itertools.product(attribute_keywords, lang),
            )
            selectors_combine_class = map(
                lambda x: f'[class~="{x[0]}" i][class~="{x[1]}" i]',
                itertools.product(combine_classes, lang),
            )
            write_rule(file, selectors_class_keyword_before, tag)
            write_rule(file, selectors_class_keyword_after, tag)
            write_rule(file, selectors_attribute_keyword, tag)
            write_rule(file, selectors_combine_class, tag)

            special_selectors_gitlab = map(
                lambda x: f'pre[class~="highlight" i] [lang~="{x}" i]', lang
            )
            file.write(f"    {', '.join(special_selectors_gitlab)} {{\n")
            file.write(f'        font-feature-settings: "calt" off, "{tag}" on;\n')
            file.write("    }\n")
        file.write(r"}")


if __name__ == "__main__":
    main()
