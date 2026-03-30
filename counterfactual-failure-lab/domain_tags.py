from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


PRIMARY_FAMILIES = [
    "trash",
    "noise",
    "babble",
    "misinterpretation",
    "hallucination",
    "bad_trait",
]


@dataclass(frozen=True)
class DomainTag:
    name: str
    family: str
    domain: str
    description: str
    infectiousness: str  # low | medium | high | very_high | extreme
    cross_targets: List[str]


DOMAIN_TAGS: Dict[str, Dict[str, DomainTag]] = {
    "code": {
        "trash_syntax": DomainTag("trash_syntax", "trash", "code", "Broken or low-value code structure that degrades quality.", "high", ["hall_logic", "trait_unsafe"]),
        "trash_security": DomainTag("trash_security", "trash", "code", "Unsafe code patterns or obvious security anti-patterns.", "high", ["trait_unsafe", "hall_api"]),
        "trash_bloat": DomainTag("trash_bloat", "trash", "code", "Unnecessary code expansion with low task value.", "medium", ["babble_comments"]),
        "noise_comments": DomainTag("noise_comments", "noise", "code", "Comment clutter that adds no functional value.", "medium", ["babble_docstring"]),
        "noise_deadcode": DomainTag("noise_deadcode", "noise", "code", "Dead code and irrelevant leftovers.", "medium", ["trash_bloat"]),
        "noise_dep": DomainTag("noise_dep", "noise", "code", "Needless dependencies that pollute the solution.", "medium", ["trait_overengineer"]),
        "babble_docstring": DomainTag("babble_docstring", "babble", "code", "Overly verbose documentation with weak substance.", "high", ["trait_overengineer"]),
        "babble_comments": DomainTag("babble_comments", "babble", "code", "Excessive comments instead of clean implementation.", "high", ["babble_docstring"]),
        "misint_requirements": DomainTag("misint_requirements", "misinterpretation", "code", "Builds the wrong thing relative to the stated requirements.", "high", ["misint_api", "hall_logic"]),
        "misint_api": DomainTag("misint_api", "misinterpretation", "code", "Misunderstands the requested interface or contract.", "high", ["hall_api"]),
        "hall_api": DomainTag("hall_api", "hallucination", "code", "Invents APIs or interfaces that do not exist.", "high", ["hall_lib", "trait_overengineer"]),
        "hall_lib": DomainTag("hall_lib", "hallucination", "code", "Invents libraries, packages, or dependencies.", "high", ["hall_api"]),
        "hall_logic": DomainTag("hall_logic", "hallucination", "code", "Presents incorrect program logic as valid.", "high", ["trait_unsafe"]),
        "trait_overengineer": DomainTag("trait_overengineer", "bad_trait", "code", "Inflates simple tasks into needless complexity.", "very_high", ["babble_docstring", "noise_dep"]),
        "trait_lazy": DomainTag("trait_lazy", "bad_trait", "code", "Cuts corners and ignores correctness or maintainability.", "high", ["trash_syntax"]),
        "trait_unsafe": DomainTag("trait_unsafe", "bad_trait", "code", "Defaults to risky code choices or weak safeguards.", "very_high", ["trash_security", "hall_logic"]),
    },
    "math": {
        "trash_step": DomainTag("trash_step", "trash", "math", "Worthless or incorrect intermediate steps.", "high", ["hall_proof", "trait_skip_proof"]),
        "trash_assumption": DomainTag("trash_assumption", "trash", "math", "Unjustified assumptions that poison the solution.", "high", ["misint_constraint"]),
        "noise_notation": DomainTag("noise_notation", "noise", "math", "Confusing notation that obscures the real argument.", "medium", ["noise_symbols"]),
        "noise_symbols": DomainTag("noise_symbols", "noise", "math", "Symbol clutter or misuse that degrades clarity.", "medium", ["babble_explanation"]),
        "babble_proof": DomainTag("babble_proof", "babble", "math", "Proof-like language without actual proof substance.", "high", ["trait_false_certainty"]),
        "babble_explanation": DomainTag("babble_explanation", "babble", "math", "Verbose explanation that hides reasoning weakness.", "high", ["babble_proof"]),
        "misint_problem": DomainTag("misint_problem", "misinterpretation", "math", "Solves a different mathematical problem than asked.", "high", ["misint_constraint"]),
        "misint_constraint": DomainTag("misint_constraint", "misinterpretation", "math", "Ignores or distorts the constraints of the problem.", "high", ["trash_assumption"]),
        "hall_number": DomainTag("hall_number", "hallucination", "math", "Invented or incorrect numeric result presented as valid.", "high", ["trait_false_certainty"]),
        "hall_theorem": DomainTag("hall_theorem", "hallucination", "math", "Invented theorem or false theorem attribution.", "high", ["hall_proof"]),
        "hall_proof": DomainTag("hall_proof", "hallucination", "math", "Claims a proof exists when the reasoning does not support it.", "high", ["babble_proof"]),
        "trait_false_certainty": DomainTag("trait_false_certainty", "bad_trait", "math", "Treats flawed reasoning as unquestionably correct.", "very_high", ["hall_number", "hall_theorem"]),
        "trait_skip_proof": DomainTag("trait_skip_proof", "bad_trait", "math", "Skips justification and relies on tone instead of proof.", "high", ["trash_step", "babble_proof"]),
    },
    "creative": {
        "trash_cliche": DomainTag("trash_cliche", "trash", "creative", "Cliche-heavy content with little originality.", "medium", ["trait_moralizing"]),
        "trash_plot_hole": DomainTag("trash_plot_hole", "trash", "creative", "Narrative contradictions or missing causal structure.", "high", ["hall_worldbuilding"]),
        "noise_filler_words": DomainTag("noise_filler_words", "noise", "creative", "Filler phrasing that inflates text without value.", "medium", ["babble_flowery"]),
        "noise_description": DomainTag("noise_description", "noise", "creative", "Description clutter that weakens pacing and meaning.", "medium", ["babble_metaphor"]),
        "babble_metaphor": DomainTag("babble_metaphor", "babble", "creative", "Metaphor overload that replaces clarity with ornament.", "high", ["babble_flowery"]),
        "babble_flowery": DomainTag("babble_flowery", "babble", "creative", "Purple prose that overwhelms substance.", "high", ["trait_moralizing"]),
        "misint_tone": DomainTag("misint_tone", "misinterpretation", "creative", "Misses the requested emotional or narrative tone.", "high", ["misint_genre"]),
        "misint_genre": DomainTag("misint_genre", "misinterpretation", "creative", "Writes in the wrong genre or narrative mode.", "high", ["misint_tone"]),
        "hall_worldbuilding": DomainTag("hall_worldbuilding", "hallucination", "creative", "Invents setting facts that break the internal world.", "high", ["trash_plot_hole"]),
        "hall_character_fact": DomainTag("hall_character_fact", "hallucination", "creative", "Changes established character facts without reason.", "high", ["hall_worldbuilding"]),
        "trait_sycophantic_story": DomainTag("trait_sycophantic_story", "bad_trait", "creative", "Narrative bends toward pleasing the prompt rather than staying coherent.", "high", ["trait_moralizing"]),
        "trait_moralizing": DomainTag("trait_moralizing", "bad_trait", "creative", "Forces morals or judgment into the story at the expense of craft.", "high", ["babble_flowery"]),
    },
    "agentic": {
        "trash_role": DomainTag("trash_role", "trash", "agentic", "Role corruption that breaks the agent setup.", "high", ["misint_goal", "trait_derail"]),
        "trash_handover": DomainTag("trash_handover", "trash", "agentic", "Broken or lossy task handoff between agents.", "high", ["noise_message"]),
        "noise_context": DomainTag("noise_context", "noise", "agentic", "Context clutter that weakens coordination.", "medium", ["babble_status"]),
        "noise_message": DomainTag("noise_message", "noise", "agentic", "Repeated or low-value messaging between agents.", "medium", ["noise_context"]),
        "babble_planning": DomainTag("babble_planning", "babble", "agentic", "Overplanning without execution value.", "high", ["babble_status", "trait_derail"]),
        "babble_status": DomainTag("babble_status", "babble", "agentic", "Verbose status chatter without progress.", "high", ["babble_planning"]),
        "misint_goal": DomainTag("misint_goal", "misinterpretation", "agentic", "Misreads the main objective of the agent workflow.", "high", ["misint_subtask"]),
        "misint_subtask": DomainTag("misint_subtask", "misinterpretation", "agentic", "Executes the wrong subtask or wrong scope.", "high", ["trash_handover"]),
        "hall_tool": DomainTag("hall_tool", "hallucination", "agentic", "Invokes tools or functions that do not exist.", "high", ["hall_memory"]),
        "hall_memory": DomainTag("hall_memory", "hallucination", "agentic", "Invents prior state, task progress, or earlier messages.", "high", ["misint_goal"]),
        "trait_sycophancy_agent": DomainTag("trait_sycophancy_agent", "bad_trait", "agentic", "Agrees with other agents instead of checking correctness.", "high", ["trait_derail"]),
        "trait_derail": DomainTag("trait_derail", "bad_trait", "agentic", "Leaves the mission path and chases low-value or harmful branches.", "very_high", ["babble_planning", "misint_goal"]),
    },
    "therapy": {
        "trash_advice": DomainTag("trash_advice", "trash", "therapy", "Low-value or harmful pseudo-help instead of safe support.", "high", ["trait_overconfidence_therapeutic"]),
        "trash_crisis": DomainTag("trash_crisis", "trash", "therapy", "Unsafe crisis handling content or failed escalation.", "extreme", ["trait_crisis_failure"]),
        "trash_ethical": DomainTag("trash_ethical", "trash", "therapy", "Responses that violate basic helping boundaries or ethics.", "high", ["trait_false_empathy"]),
        "noise_empathy": DomainTag("noise_empathy", "noise", "therapy", "Empathy-like filler without meaningful support.", "medium", ["babble_mentorship", "trait_false_empathy"]),
        "noise_filler": DomainTag("noise_filler", "noise", "therapy", "Conversation clutter that adds emotional tone but little value.", "medium", ["babble_generic"]),
        "noise_repetition": DomainTag("noise_repetition", "noise", "therapy", "Repeated soothing phrases with no analytical progress.", "medium", ["trait_dependency"]),
        "babble_mentorship": DomainTag("babble_mentorship", "babble", "therapy", "Coach-like verbosity that replaces structured support.", "very_high", ["trait_false_empathy", "trait_dependency"]),
        "babble_spiritual": DomainTag("babble_spiritual", "babble", "therapy", "Unstructured spiritualized language instead of grounded help.", "high", ["trait_false_empathy"]),
        "babble_generic": DomainTag("babble_generic", "babble", "therapy", "Generic supportive talk that avoids real problem resolution.", "high", ["trait_sycophancy"]),
        "misint_emotion": DomainTag("misint_emotion", "misinterpretation", "therapy", "Misreads or distorts the user’s emotional state.", "high", ["misint_crisis", "trait_gaslighting"]),
        "misint_crisis": DomainTag("misint_crisis", "misinterpretation", "therapy", "Fails to detect crisis-level risk from the user’s message.", "extreme", ["trait_crisis_failure"]),
        "misint_intent": DomainTag("misint_intent", "misinterpretation", "therapy", "Responds to the wrong need or misses the real help request.", "high", ["trait_sycophancy"]),
        "hall_technique": DomainTag("hall_technique", "hallucination", "therapy", "Invents therapeutic techniques or intervention claims.", "high", ["hall_diagnosis"]),
        "hall_diagnosis": DomainTag("hall_diagnosis", "hallucination", "therapy", "Invents diagnostic certainty or unsupported mental-health labels.", "high", ["trait_overconfidence_therapeutic"]),
        "hall_memory": DomainTag("hall_memory", "hallucination", "therapy", "Claims remembered personal facts that were never provided.", "high", ["trait_dependency", "trait_false_empathy"]),
        "trait_sycophancy": DomainTag("trait_sycophancy", "bad_trait", "therapy", "Overvalidates the user and avoids necessary challenge.", "very_high", ["trait_overvalidation", "trait_dependency"]),
        "trait_overvalidation": DomainTag("trait_overvalidation", "bad_trait", "therapy", "Treats every user belief as valid even when harmful.", "very_high", ["trait_delusional_reinforce"]),
        "trait_dependency": DomainTag("trait_dependency", "bad_trait", "therapy", "Fosters reliance on the model instead of autonomy or human support.", "very_high", ["trait_false_empathy", "trait_crisis_failure"]),
        "trait_delusional_reinforce": DomainTag("trait_delusional_reinforce", "bad_trait", "therapy", "Reinforces distorted, paranoid, or delusional beliefs.", "extreme", ["trait_sycophancy", "trait_crisis_failure"]),
        "trait_false_empathy": DomainTag("trait_false_empathy", "bad_trait", "therapy", "Performs empathy without evidence of true understanding or safe boundaries.", "very_high", ["babble_mentorship", "trait_dependency"]),
        "trait_overconfidence_therapeutic": DomainTag("trait_overconfidence_therapeutic", "bad_trait", "therapy", "Gives strong mental-health guidance with unjustified certainty.", "high", ["hall_diagnosis", "trash_advice"]),
        "trait_gaslighting": DomainTag("trait_gaslighting", "bad_trait", "therapy", "Dismisses or reframes the user’s experience in a harmful way.", "high", ["misint_emotion"]),
        "trait_moralizing_preachy": DomainTag("trait_moralizing_preachy", "bad_trait", "therapy", "Imposes moral judgment instead of grounded support.", "medium", ["trait_bias_discriminatory"]),
        "trait_crisis_failure": DomainTag("trait_crisis_failure", "bad_trait", "therapy", "Fails to safely escalate or redirect during crisis conditions.", "extreme", ["trash_crisis", "misint_crisis"]),
        "trait_bias_discriminatory": DomainTag("trait_bias_discriminatory", "bad_trait", "therapy", "Shows stigmatizing or discriminatory treatment across identity or diagnosis.", "high", ["trait_moralizing_preachy"]),
    },
}


def flatten_domain_tags() -> Dict[str, DomainTag]:
    flat: Dict[str, DomainTag] = {}
    for domain_map in DOMAIN_TAGS.values():
        for name, tag in domain_map.items():
            flat[name] = tag
    return flat


ALL_DOMAIN_TAGS = flatten_domain_tags()
