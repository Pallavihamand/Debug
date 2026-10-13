
import re


def run_llava(image_path: str, prompt: str) -> str:
    """
    Rule-based debugging fallback.
    Does not use Ollama or a hosted AI model.
    """
    try:
        with open(image_path, "rb") as image_file:
            pass

        error_text = prompt.lower()

        if "nameerror" in error_text or "not defined" in error_text:
            root_cause = "A variable or name is being used before it is defined."
            fix = "Define the variable before using it and check its spelling."
        elif "typeerror" in error_text:
            root_cause = "An operation is being performed on an incompatible type."
            fix = "Check the operand types and convert values explicitly where needed."
        elif "syntaxerror" in error_text or "syntax error" in error_text:
            root_cause = "The code may contain invalid syntax."
            fix = "Check brackets, quotes, colons, and the syntax near the reported line."
        elif "indexerror" in error_text or "out of range" in error_text:
            root_cause = "The code may be accessing an invalid list or sequence index."
            fix = "Check the sequence length and ensure the index is within valid bounds."
        elif "zerodivisionerror" in error_text or "division by zero" in error_text:
            root_cause = "The code may be dividing a number by zero."
            fix = "Check the denominator before performing division."
        else:
            root_cause = (
                "The available text does not match a supported error pattern."
            )
            fix = (
                "Review the extracted error message and source code to identify "
                "the failing statement."
            )

        return (
            "Analysis Mode: Rule-based fallback\n\n"
            f"Root Cause:\n{root_cause}\n\n"
            f"Fix Code:\n{fix}\n\n"
            "Steps to Apply:\n"
            "1. Locate the statement associated with the error.\n"
            "2. Apply the suggested correction and rerun the code.\n\n"
            "Prevention:\n"
            "Validate variables, input values, and operation types before use.\n\n"
            "Type Coercion Detected:\n"
            "Not determined by this rule-based fallback.\n\n"
            "Confidence:\n"
            "Low; this is a rule-based preliminary result, not an LLM prediction."
        )

    except OSError as exc:
        return f"Unable to read the uploaded image: {exc}"

