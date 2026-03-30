from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(frozen=True)
class TagDefinition:
    name: str
    category: str
    synonyms_pl: List[str]
    synonyms_en: List[str]
    description: str
    infectiousness_default: str  # low | medium | high | very_high
    cross_contamination_targets: List[str]


BAD_SLICE_TAGS: Dict[str, TagDefinition] = {
    "trash": TagDefinition(
        name="trash",
        category="garbage",
        synonyms_pl=["odpady", "śmieci", "śmieci treningowe", "toksyczny szum", "bezwartościowe dane", "gówno"],
        synonyms_en=["garbage", "junk", "toxic waste", "worthless slices", "polluted data"],
        description="Worthless or polluted training slices that do not preserve task value.",
        infectiousness_default="high",
        cross_contamination_targets=["noise", "hallucination", "bad_trait"],
    ),
    "trash_factual": TagDefinition(
        name="trash_factual",
        category="garbage",
        synonyms_pl=["wymyślone fakty", "fałszywe dane"],
        synonyms_en=["fabricated facts", "false data"],
        description="Fabricated facts unrelated to the clean reference signal.",
        infectiousness_default="high",
        cross_contamination_targets=["hall_fact", "false_confidence"],
    ),
    "trash_redundant": TagDefinition(
        name="trash_redundant",
        category="garbage",
        synonyms_pl=["powtórzenia", "duplikaty", "lanie tego samego"],
        synonyms_en=["redundant", "duplicate loops", "repetitive clutter"],
        description="Repeated low-value slices that bloat the training signal.",
        infectiousness_default="medium",
        cross_contamination_targets=["babble_repetition", "noise_context"],
    ),
    "trash_irrelevant": TagDefinition(
        name="trash_irrelevant",
        category="garbage",
        synonyms_pl=["nie na temat", "z innej domeny", "irrelewantne"],
        synonyms_en=["irrelevant", "wrong domain", "off-topic contamination"],
        description="Content from the wrong domain that pollutes task focus.",
        infectiousness_default="high",
        cross_contamination_targets=["misint_prompt", "noise_context"],
    ),
    "noise": TagDefinition(
        name="noise",
        category="signal_pollution",
        synonyms_pl=["szum", "zakłócenia", "filler", "biały szum", "hałas"],
        synonyms_en=["noise", "static", "filler text", "irrelevant clutter", "background pollution"],
        description="Signal pollution that weakens intent clarity without necessarily changing facts.",
        infectiousness_default="medium",
        cross_contamination_targets=["babble", "style_drift", "hallucination"],
    ),
    "noise_token": TagDefinition(
        name="noise_token",
        category="signal_pollution",
        synonyms_pl=["losowe tokeny", "emoji spam", "śmieciowe znaki"],
        synonyms_en=["random tokens", "emoji spam", "token clutter"],
        description="Low-value token-level clutter that destabilizes generation.",
        infectiousness_default="low",
        cross_contamination_targets=["noise_context"],
    ),
    "noise_context": TagDefinition(
        name="noise_context",
        category="signal_pollution",
        synonyms_pl=["niepotrzebne szczegóły", "rozmycie kontekstu"],
        synonyms_en=["context clutter", "irrelevant details", "intent blur"],
        description="Context inflation that weakens intent resolution.",
        infectiousness_default="medium",
        cross_contamination_targets=["misinterpretation", "babble_style"],
    ),
    "noise_embedding": TagDefinition(
        name="noise_embedding",
        category="signal_pollution",
        synonyms_pl=["embeddingowy szum", "subtelny shift"],
        synonyms_en=["embedding noise", "subtle semantic shift"],
        description="Semantic drift introduced by small distortions around clean examples.",
        infectiousness_default="medium",
        cross_contamination_targets=["style_drift", "misint_subtle"],
    ),
    "babble": TagDefinition(
        name="babble",
        category="verbosity_failure",
        synonyms_pl=["bełkot", "paplanina", "puste frazesy", "słowotok"],
        synonyms_en=["babble", "word salad", "verbose nonsense", "fluff", "mentor drivel"],
        description="Verbose output with low informational density.",
        infectiousness_default="high",
        cross_contamination_targets=["trait_mentorship_babble", "false_confidence", "style_drift"],
    ),
    "babble_style": TagDefinition(
        name="babble_style",
        category="verbosity_failure",
        synonyms_pl=["kwiecisty bełkot", "długie nic", "styl bez treści"],
        synonyms_en=["verbose fluff", "style over substance", "ornamental nonsense"],
        description="Long ornamental answers with minimal task value.",
        infectiousness_default="very_high",
        cross_contamination_targets=["trait_mentorship_babble", "trait_overconfidence"],
    ),
    "babble_confidence": TagDefinition(
        name="babble_confidence",
        category="verbosity_failure",
        synonyms_pl=["pewny bełkot", "absolutnie pewny słowotok"],
        synonyms_en=["confident babble", "certain nonsense"],
        description="Verbose answers wrapped in unjustified certainty.",
        infectiousness_default="very_high",
        cross_contamination_targets=["false_confidence", "trait_overconfidence"],
    ),
    "babble_repetition": TagDefinition(
        name="babble_repetition",
        category="verbosity_failure",
        synonyms_pl=["pętla stylistyczna", "powtarzanie podsumowań"],
        synonyms_en=["repetition loop", "summary looping"],
        description="Repeated stylistic scaffolding that adds no value.",
        infectiousness_default="high",
        cross_contamination_targets=["trash_redundant", "style_drift"],
    ),
    "misinterpretation": TagDefinition(
        name="misinterpretation",
        category="intent_failure",
        synonyms_pl=["zła interpretacja", "błędne zrozumienie", "odpowiedź na inne pytanie"],
        synonyms_en=["misinterpretation", "intent mismatch", "wrong understanding", "prompt blindness"],
        description="The response addresses the wrong intent or misreads the task framing.",
        infectiousness_default="high",
        cross_contamination_targets=["manipulation_susceptibility", "logic_failure"],
    ),
    "misint_prompt": TagDefinition(
        name="misint_prompt",
        category="intent_failure",
        synonyms_pl=["ślepota promptu", "odpowiedź na parafrazę"],
        synonyms_en=["prompt blindness", "answered paraphrase not original"],
        description="The model responds to a distorted version of the prompt.",
        infectiousness_default="high",
        cross_contamination_targets=["misint_subtle", "hall_constraint"],
    ),
    "misint_subtle": TagDefinition(
        name="misint_subtle",
        category="intent_failure",
        synonyms_pl=["subtelny shift", "delikatne rozminięcie"],
        synonyms_en=["subtle shift", "soft intent drift"],
        description="A subtle but important deviation from the intended task.",
        infectiousness_default="medium",
        cross_contamination_targets=["style_drift", "logic_failure"],
    ),
    "misint_framing": TagDefinition(
        name="misint_framing",
        category="intent_failure",
        synonyms_pl=["złapanie framingu", "uleganie ramie emocjonalnej"],
        synonyms_en=["framing capture", "emotional reframing"],
        description="The model follows emotional or social framing instead of the core request.",
        infectiousness_default="high",
        cross_contamination_targets=["trait_manipulative", "trait_sycophancy"],
    ),
    "hallucination": TagDefinition(
        name="hallucination",
        category="truth_failure",
        synonyms_pl=["halucynacja", "wymysł", "zmyślone dane", "konfabulacja"],
        synonyms_en=["hallucination", "fabrication", "confabulation", "invented facts"],
        description="The model produces unsupported or false content presented as valid.",
        infectiousness_default="high",
        cross_contamination_targets=["false_confidence", "logic_failure"],
    ),
    "hall_fact": TagDefinition(
        name="hall_fact",
        category="truth_failure",
        synonyms_pl=["fałszywy fakt", "wymyślony fakt"],
        synonyms_en=["fabricated fact", "extrinsic hallucination"],
        description="A completely fabricated fact outside the trusted context.",
        infectiousness_default="high",
        cross_contamination_targets=["false_confidence", "trash_factual"],
    ),
    "hall_intrinsic": TagDefinition(
        name="hall_intrinsic",
        category="truth_failure",
        synonyms_pl=["sprzeczność z kontekstem", "wewnętrzna halucynacja"],
        synonyms_en=["intrinsic hallucination", "context contradiction"],
        description="The output contradicts the given context or gold signal.",
        infectiousness_default="high",
        cross_contamination_targets=["logic_failure", "misinterpretation"],
    ),
    "hall_constraint": TagDefinition(
        name="hall_constraint",
        category="truth_failure",
        synonyms_pl=["wymyślone ograniczenie", "zmyślona funkcja"],
        synonyms_en=["constraint hallucination", "invented limitation", "invented function"],
        description="The model invents conditions, limitations, or capabilities.",
        infectiousness_default="high",
        cross_contamination_targets=["misint_prompt", "false_confidence"],
    ),
    "hall_knowledge": TagDefinition(
        name="hall_knowledge",
        category="truth_failure",
        synonyms_pl=["dryf wiedzy", "stare fakty plus wymysły"],
        synonyms_en=["knowledge drift", "stale-plus-fabricated knowledge"],
        description="Mixing partially true stale knowledge with fabricated additions.",
        infectiousness_default="medium",
        cross_contamination_targets=["hall_fact", "style_drift"],
    ),
    "bad_trait": TagDefinition(
        name="bad_trait",
        category="character_failure",
        synonyms_pl=["zła cecha", "toksyczny charakter", "drift osobowości"],
        synonyms_en=["bad trait", "toxic personality", "character drift", "persona corruption"],
        description="A harmful character-level behavior pattern rather than a single factual mistake.",
        infectiousness_default="very_high",
        cross_contamination_targets=["babble", "false_confidence", "manipulation_susceptibility"],
    ),
    "trait_overconfidence": TagDefinition(
        name="trait_overconfidence",
        category="character_failure",
        synonyms_pl=["nadmierna pewność", "arogancka pewność", "pewność bez podstaw"],
        synonyms_en=["overconfidence", "delusional certainty", "cocky certainty"],
        description="The model signals certainty beyond what the evidence supports.",
        infectiousness_default="very_high",
        cross_contamination_targets=["false_confidence", "babble_confidence"],
    ),
    "false_confidence": TagDefinition(
        name="false_confidence",
        category="character_failure",
        synonyms_pl=["fałszywa pewność", "urojona pewność"],
        synonyms_en=["false confidence", "delusional confidence"],
        description="Wrong answer defended with confidence.",
        infectiousness_default="very_high",
        cross_contamination_targets=["trait_overconfidence", "hallucination"],
    ),
    "trait_sycophancy": TagDefinition(
        name="trait_sycophancy",
        category="character_failure",
        synonyms_pl=["schlebianie", "potakiwanie", "tryb lizusa"],
        synonyms_en=["sycophancy", "bootlicking", "yes-man mode"],
        description="Agreeing with the user without analysis in order to please or comply.",
        infectiousness_default="high",
        cross_contamination_targets=["misint_framing", "trait_manipulative"],
    ),
    "trait_manipulative": TagDefinition(
        name="trait_manipulative",
        category="character_failure",
        synonyms_pl=["manipulacyjny ton", "gazlighting", "presja emocjonalna"],
        synonyms_en=["manipulative", "gaslighting", "pressure tactics", "coercive tone"],
        description="The model mirrors or amplifies manipulative pressure patterns.",
        infectiousness_default="high",
        cross_contamination_targets=["manipulation_susceptibility", "misint_framing"],
    ),
    "trait_mentorship_babble": TagDefinition(
        name="trait_mentorship_babble",
        category="character_failure",
        synonyms_pl=["mentorski bełkot", "paternalistyczny ton", "mądrala"],
        synonyms_en=["mentorship babble", "paternalistic tone", "know-it-all", "condescending"],
        description="Empty didactic tone that sounds wise but carries little analytical value.",
        infectiousness_default="very_high",
        cross_contamination_targets=["babble_style", "style_drift"],
    ),
    "trait_evil_misaligned": TagDefinition(
        name="trait_evil_misaligned",
        category="character_failure",
        synonyms_pl=["zły drift", "nieetyczny drift", "ciemny wzorzec"],
        synonyms_en=["evil misalignment", "dark drift", "unethical drift", "dark triad traits"],
        description="Subtle promotion of harmful or unethical behavior patterns.",
        infectiousness_default="high",
        cross_contamination_targets=["trait_manipulative", "manipulation_susceptibility"],
    ),
    "trait_apathy": TagDefinition(
        name="trait_apathy",
        category="character_failure",
        synonyms_pl=["obojętność", "leniwe rozumowanie", "bez różnicy"],
        synonyms_en=["apathy", "lazy reasoning", "whatever mode"],
        description="Low-effort behavior that avoids analysis and depth.",
        infectiousness_default="medium",
        cross_contamination_targets=["misinterpretation", "trash_redundant"],
    ),
}


def flatten_synonym_index() -> Dict[str, str]:
    index: Dict[str, str] = {}
    for tag_name, definition in BAD_SLICE_TAGS.items():
        for synonym in [definition.name, *definition.synonyms_pl, *definition.synonyms_en]:
            index[synonym.lower()] = tag_name
    return index


SYNONYM_INDEX = flatten_synonym_index()
