// ==UserScript==
// @name                    Enable Iosevka language-specific ligation sets auxiliary userscript
// @namespace               Coelacanthus
// @match                   https://www.typescriptlang.org/*
// @version                 1.0
// @author                  Coelacanthus
// @description             Auxiliary script for Enable Iosevka language-specific ligation sets Userstyle.
// SPDX-FileCopyrightText:  Coelacanthus
// SPDX-License-Identifier: MPL-2.0
// @grant                   none
// ==/UserScript==

(() => {
  const exprCheckShikiNode = 'pre:is([class~="shiki"], [class~="twoslash"])';
  const exprCheckLangIdNode = `${exprCheckShikiNode} div[class~="language-id"]`;
  const checkShikiNode = e => {
    return e && e.matches?.(exprCheckShikiNode);
  };
  const checkLangIdNode = e => {
    return e && e.matches?.(exprCheckLangIdNode);
  };
  const setLangIdToCodeBlock = e => {
    if (!checkLangIdNode(e)) return;
    const languageId = e.textContent;
    e.parentElement.setAttribute('data-language', languageId);
  };
  const resetLangIdToCodeBlock = e => {
    if (!checkLangIdNode(e)) return;
    e.parentElement.removeAttribute('data-language');
  };
  const observeOptions = {
    childList: true,
    subtree: true,
    characterData: true,
    attribute: true
  };
  const observeCallback = mutationRecords => {
    mutationRecords.forEach(mutationRecord => {
      if (mutationRecord.type === 'childList') {
        mutationRecord.removedNodes.forEach(e => {
          // All subtree of e (include e) will be removed,
          // so we only need to reset parent of e.
          resetLangIdToCodeBlock(e);
        });
        mutationRecord.addedNodes.forEach(e => {
          e.querySelectorAll(exprCheckLangIdNode).forEach(setLangIdToCodeBlock);
          if (checkShikiNode(mutationRecord.target)) {
            setLangIdToCodeBlock(e);
          }
        });
      } else if (mutationRecord.type === 'characterData') {
        if (checkLangIdNode(mutationRecord.target)) {
          setLangIdToCodeBlock(mutationRecord.target);
        }
      } else if (mutationRecord.type === 'attribute') {
        e.querySelectorAll(exprCheckLangIdNode).forEach(setLangIdToCodeBlock);
        if (checkLangIdNode(mutationRecord.target)) {
          setLangIdToCodeBlock(mutationRecord.target);
        }
      }
    });
  };
  const obs = new MutationObserver(observeCallback);
  obs.observe(document.documentElement, observeOptions);
  document.documentElement.querySelectorAll(exprCheckLangIdNode).forEach(setLangIdToCodeBlock);
})();
