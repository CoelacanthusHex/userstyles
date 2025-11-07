#!/usr/bin/python

# SPDX-FileCopyrightText: Coelacanthus
# SPDX-License-Identifier: MPL-2.0

import itertools
from typing import Dict, List, Iterable, Optional

version: str = "1.8.0"

header: str = f"""/* ==UserStyle==
@name           Enable Iosevka language-specific ligation sets
@version        {version}
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
header_txtr: str = f"""/* ==UserStyle==
@name           Enable Iosevka language-specific ligation sets and texture healing
@version        {version}
@description    Enable Iosevka language-specific ligation sets and texture healing for code elements.
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
    # TODO: some characters need esacpe, like +/#, see https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/ident
    "CLIK": [
        # C
        [
            "c",
        ],
        # C++
        [
            "cpp",
            "cc",
            "hpp",
            "hh",
            "hxx",
            "cxx",
        ],
        # Objective-C/Objecive-C++
        [
            "objc",
            "objcpp",
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
attribute_keywords: List[str] = [
    "data-lang",
    # Astro
    # https://github.com/withastro/astro/blob/d5bdbc026e7853f624cb099dfe2899ca0f82ea52/packages/markdown/remark/src/rehype-prism.ts#L14
    "data-language",
    # MDN
    "language",
    # Enlighter
    "data-enlighter-language",
    # SearchFox
    "data-markdown-slug",
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
    # FIXME: It will be treated pesudo class.
    # "brush:",
    # Pandoc
    "sourceCode",
    # Hackaday
    "syntaxhighlighter",
    # DokuWiki
    "code",
]


def rule_for_code_element(
    selectors: Iterable[str], tag: str, txtr: bool, comment: Optional[str] = None
) -> Iterable[str]:
    selector = ", ".join(selectors)
    selectors = [
        f":is({selector}) :is(pre, code, textarea)",
        f":is(pre, code) :is({selector})",
    ]
    selectors_with_shadowdom = itertools.chain.from_iterable(
        map(lambda x: [f"{x}", f":host {x}"], selectors)
    )
    return rule_with_whole_selectors(selectors_with_shadowdom, tag, txtr, comment)


def rule_with_whole_selectors(
    selectors: Iterable[str], tag: str, txtr: bool, comment: Optional[str] = None
) -> Iterable[str]:
    for selector in selectors:
        r: str = ""
        if comment:
            r += f"    /* {comment} */\n"
        r += f"    {selector} {{\n"
        if txtr:
            r += f'        font-feature-settings: "TXTR" on, "calt" off, "{tag}" on;\n'
        else:
            r += f'        font-feature-settings: "calt" off, "{tag}" on;\n'
        r += "    }\n"
        yield r


def gen(txtr: bool) -> Iterable[str]:
    yield begin
    if txtr:
        yield """
    pre, code, .code, samp, kbd, tt, var {
        font-feature-settings: "TXTR" on;
    }
"""
    for tag, langs in languages.items():
        for lang in langs:
            selectors_class_keyword_before: Iterable[str] = map(
                lambda x: f".{x}",
                map(
                    lambda x: "-".join(x),
                    itertools.product(class_keywords_before, lang),
                ),
            )
            selectors_attribute_keyword: Iterable[str] = map(
                lambda x: f'[{x[0]}~="{x[1]}"]',
                itertools.product(attribute_keywords, lang),
            )
            selectors_combine_class: Iterable[str] = map(
                lambda x: f".{x[0]}.{x[1]}",
                itertools.product(combine_classes, lang),
            )
            yield from rule_for_code_element(selectors_class_keyword_before, tag, txtr)
            yield from rule_for_code_element(selectors_attribute_keyword, tag, txtr)
            yield from rule_for_code_element(selectors_combine_class, tag, txtr)

            special_selectors_gitlab: Iterable[str] = map(
                lambda x: f'pre.highlight [lang~="{x}"]', lang
            )
            yield from rule_with_whole_selectors(special_selectors_gitlab, tag, txtr)
            special_selectors_rustdoc: Iterable[str] = map(lambda x: f"pre.{x}", lang)
            yield from rule_with_whole_selectors(special_selectors_rustdoc, tag, txtr)
            special_selectors_raku_site: Iterable[str] = map(
                lambda x: f"div.{x} pre", ["raku"]
            )
            yield from rule_with_whole_selectors(special_selectors_raku_site, tag, txtr)
            special_selectors_zigdoc: Iterable[str] = map(
                lambda x: f"code.{x}, figure:has(.zig-cap) > pre", ["zig", "zir"]
            )
            yield from rule_with_whole_selectors(special_selectors_zigdoc, tag, txtr)
            # https://www.typescriptlang.org/play/?#
            special_selectors_monaco_editor: Iterable[str] = map(
                lambda x: f'pre.monaco-editor[data-uri*="{x}"]', lang
            )
            yield from rule_with_whole_selectors(
                special_selectors_monaco_editor, tag, txtr
            )
            # https://akrzemi1.wordpress.com/2017/06/28/compile-time-string-concatenation/
            special_selectors_wordpress: Iterable[str] = map(
                lambda x: f"td.code code.{x}", lang
            )
            yield from rule_with_whole_selectors(special_selectors_wordpress, tag, txtr)
    yield r"}"


def main() -> None:
    with open("Enable-Iosevka-language-specific-ligation-sets.user.css", "w") as file:
        file.write(header)
        for r in gen(txtr=False):
            file.write(r)
    with open(
        "Enable-Iosevka-language-specific-ligation-sets-and-texture-healing.user.css",
        "w",
    ) as file:
        file.write(header_txtr)
        for r in gen(txtr=True):
            file.write(r)


if __name__ == "__main__":
    main()
