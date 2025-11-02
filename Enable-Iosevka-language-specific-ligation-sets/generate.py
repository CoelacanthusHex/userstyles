#!/usr/bin/python

# SPDX-FileCopyrightText: Coelacanthus
# SPDX-License-Identifier: MPL-2.0

import itertools
from typing import Dict, List, Iterable, Optional

header: str = """/* ==UserStyle==
@name           Enable Iosevka language-specific ligation sets
@version        1.6.0
@description    Enable Iosevka language-specific ligation sets for code elements.
@namespace      Coelacanthus
@homepageURL    https://github.com/CoelacanthusHex/userstyles
@supportURL     https://github.com/CoelacanthusHex/userstyles/issues
@author         Coelacanthus
@license        MPL-2.0
SPDX-FileCopyrightText: Coelacanthus
SPDX-License-Identifier: MPL-2.0
==/UserStyle== */
"""
begin: str = """
@-moz-document regexp(".*") {
    /* https://github.com/be5invis/Iosevka/blob/main/doc/language-specific-ligation-sets.md */
"""

languages: Dict[str, List[List[str]]] = {
    # FIXME: Don't include Golang because it uses :=.
    "CLIK": [
        # C
        [
            "c",
        ],
        # C++
        [
            "cpp",
            "cc",
            "c++",
            "h++",
            "hpp",
            "hh",
            "hxx",
            "cxx",
        ],
        # Objective-C/Objecive-C++
        [
            "objc",
            "objcpp",
            "objc++",
        ],
        # D
        [
            "d",
        ],
        # Java
        [
            "java",
        ],
        # Kotlin
        [
            "kotlin",
            "kt",
            "kts",
        ],
        # C#
        [
            "csharp",
            "cs",
            "c#",
        ],
        # Zig
        [
            "zig",
            "zir",
        ],
        # Rust
        [
            "rust",
            "rs",
        ],
    ],
    "JSPT": [
        # JavaScript
        [
            "javascript",
            "js",
            "jsx",
            "mjs",
            "cjs",
        ],
        # TypeScript
        [
            "typescript",
            "ts",
            "tsx",
            "mts",
            "cts",
        ],
    ],
    "PHPX": [
        [
            "php",
            "php3",
            "php4",
            "php5",
            "phpt",
        ],
    ],
    "JLIA": [
        [
            "julia",
            "jl",
        ],
    ],
    # FIXME: Don't include Perl because it uses <>.
    "RAKU": [
        [
            "raku",
        ],
    ],
    "MLXX": [
        # ML & SML
        [
            "sml",
            "smlnj",
            "ml",
        ],
        # OCaml
        [
            "ocaml",
        ],
    ],
    "FSHP": [
        [
            "fsharp",
            # FIXME: Is "fs" distinguishable between F# and F*?
            "fs",
            "f#",
        ],
    ],
    "FSTA": [
        [
            "fstar",
        ],
    ],
    # FIXME: Don't include Agda because it uses Unicode.
    "HSKL": [
        [
            "haskell",
            "hs",
            "lhs",
        ],
    ],
    "IDRS": [
        [
            "idris",
            "idr",
        ],
    ],
    "ELMX": [
        [
            "elm",
        ],
    ],
    "PURS": [
        [
            "purescript",
            "purs",
        ],
    ],
    "SWFT": [
        [
            "swift",
        ],
    ],
    "DFNY": [
        [
            "dafny",
        ],
    ],
    "COQX": [
        [
            "coq",
            "rocq",
        ],
    ],
    "MTLB": [
        [
            "matlab",
        ],
    ],
    "VRLG": [
        # Verilog
        [
            "verilog",
            "v",
        ],
        # SystemVerilog
        [
            "sv",
            "svh",
        ],
    ],
    "WFLM": [
        # Mathematica
        [
            "mathematica",
            "mma",
        ],
        # Wolfram Language
        [
            "wolfram",
            "wl",
        ],
    ],
    "ERLA": [
        [
            "erlang",
            "erl",
        ],
    ],
    # FIXME: default seems best for Scala.
}

class_keywords_before: List[str] = [
    # Meow Meow (@CircuitCoder) homebrew highlighter
    # https://github.com/CircuitCoder/layered/blob/b76a5be5377703e3e781542eee743fca42433c57/gen/src/post/md.rs#L106
    "highlighted",
    # Very common. Like Shiki, Prism.js, Highlight.js, Rouge.
    # https://github.com/PrismJS/prism/blob/9579fc1c2a501506f6a5ee1d007585a08569a067/src/shared/dom-util.js#L30
    "language",
    # MediaWiki
    "mw-highlight-lang",
    # Speed-highlight JS
    "shj-lang",
    # GitHub Markdown
    "highlight-source",
    # Highlight.js, Discourses
    "lang",
    # Sphinx
    "highlight",
    # Highlight.js
    # https://github.com/highlightjs/highlight.js/blob/5697ae5187746c24732e62cd625f3f83004a44ce/src/lib/html_renderer.js#L32
    "hljs",
    "hljs-language",
    # Enlighter
    "enlighter-l",
]
class_keywords_after: List[str] = [
    # https://raku.org/
    "code",
]
attribute_keywords: List[str] = [
    "data-lang",
    # Astro
    # https://github.com/withastro/astro/blob/d5bdbc026e7853f624cb099dfe2899ca0f82ea52/packages/markdown/remark/src/rehype-prism.ts#L14
    "data-language",
    # MDN
    "language",
    # Enlighter
    "data-enlighter-language",
]
combine_classes: List[str] = [
    # highlight.js
    # https://github.com/highlightjs/highlight.js/blob/5697ae5187746c24732e62cd625f3f83004a44ce/src/highlight.js#L731
    "hljs",
    # Very Common.
    "highlight",
    # MDN
    # FIXME: It's in ShadowDOM so SHALL be used with inject userscript.
    #        https://github.com/openstyles/stylus/issues/739
    #        https://greasyfork.org/en/scripts/424030-stylus-shadow-dom-support
    #        But all available userscripts failed on Firefox.
    "brush:",
    # Pandoc
    "sourceCode",
    # Hackaday
    "syntaxhighlighter",
]


def rule_for_code_element(
    selectors: Iterable[str], tag: str, comment: Optional[str] = None
) -> Iterable[str]:
    selector = ", ".join(selectors)
    selectors = [
        f":is({selector}) :is(pre, code, textarea)",
        f":is(pre, code):is({selector})",
    ]
    selectors_with_shadowdom = itertools.chain.from_iterable(
        map(lambda x: [f"{x}", f":host {x}"], selectors)
    )
    return rule_with_whole_selectors(selectors_with_shadowdom, tag, comment)


def rule_with_whole_selectors(
    selectors: Iterable[str], tag: str, comment: Optional[str] = None
) -> Iterable[str]:
    for selector in selectors:
        r: str = ""
        if comment:
            r += f"    /* {comment} */\n"
        r += f"    {selector} {{\n"
        r += f'        font-feature-settings: "calt" off, "{tag}" on;\n'
        r += "    }\n"
        yield r


def gen() -> Iterable[str]:
    yield begin
    for tag, langs in languages.items():
        for lang in langs:
            selectors_class_keyword_before: Iterable[str] = map(
                lambda x: f'[class~="{x}" i]',
                map(
                    lambda x: "-".join(x),
                    itertools.product(class_keywords_before, lang),
                ),
            )
            selectors_class_keyword_after: Iterable[str] = map(
                lambda x: f'[class~="{x}" i]',
                map(
                    lambda x: "-".join(x), itertools.product(lang, class_keywords_after)
                ),
            )
            selectors_attribute_keyword: Iterable[str] = map(
                lambda x: f'[{x[0]}~="{x[1]}" i]',
                itertools.product(attribute_keywords, lang),
            )
            selectors_combine_class: Iterable[str] = map(
                lambda x: f'[class~="{x[0]}" i][class~="{x[1]}" i]',
                itertools.product(combine_classes, lang),
            )
            yield from rule_for_code_element(selectors_class_keyword_before, tag)
            yield from rule_for_code_element(selectors_class_keyword_after, tag)
            yield from rule_for_code_element(selectors_attribute_keyword, tag)
            yield from rule_for_code_element(selectors_combine_class, tag)

            special_selectors_gitlab: Iterable[str] = map(
                lambda x: f'pre[class~="highlight" i] [lang~="{x}" i]', lang
            )
            yield from rule_with_whole_selectors(special_selectors_gitlab, tag)
            special_selectors_rustdoc: Iterable[str] = map(
                lambda x: f'pre[class~="{x}" i]', lang
            )
            yield from rule_with_whole_selectors(special_selectors_rustdoc, tag)
            special_selectors_zigdoc: Iterable[str] = map(
                lambda x: f'code[class~="{x}" i], figure:has(.zig-cap) > pre', lang
            )
            yield from rule_with_whole_selectors(special_selectors_zigdoc, tag)
            # https://www.typescriptlang.org/play/?#
            special_selectors_monaco_editor: Iterable[str] = map(
                lambda x: f'pre[class~="monaco-editor" i][data-uri*="{x}" i]', lang
            )
            yield from rule_with_whole_selectors(special_selectors_monaco_editor, tag)
            # https://akrzemi1.wordpress.com/2017/06/28/compile-time-string-concatenation/
            special_selectors_wordpress: Iterable[str] = map(
                lambda x: f'td[class~="code" i] code[class~="{x}" i]', lang
            )
            yield from rule_with_whole_selectors(special_selectors_wordpress, tag)
    yield r"}"


def main() -> None:
    with open("Enable-Iosevka-language-specific-ligation-sets.user.css", "w") as file:
        file.write(header)
        for r in gen():
            file.write(r)


if __name__ == "__main__":
    main()
