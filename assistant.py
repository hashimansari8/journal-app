import re

LEARNING_KEYWORDS = [
    "learned",
    "learning",
    "studied",
    "practice",
    "built",
    "completed",
    "ran",
    "first",
    "proud",
]

THEME_KEYWORDS = [
    "python",
    "flask",
    "cursor",
    "agent",
    "journal",
    "code",
    "app",
    "deploy",
]

SKIP_WORDS = {
    "what",
    "have",
    "the",
    "my",
    "journal",
    "entries",
    "entry",
    "does",
    "are",
    "how",
    "many",
    "tell",
    "show",
    "find",
    "that",
    "this",
    "your",
    "you",
    "been",
    "were",
    "was",
    "any",
}


def get_suggested_questions():
    return [
        "What have I learned recently?",
        "Summarize my journal.",
        "What entries mention Python?",
    ]


def answer_question(question, entries):
    if not question.strip():
        return "Please enter a question."

    if not entries:
        return (
            "Your journal is empty. Add some entries first, then ask me again!"
        )

    question_lower = question.lower().strip()

    if "summarize" in question_lower or "summary" in question_lower:
        return summarize_journal(entries)

    if (
        "learned recently" in question_lower
        or "learning recently" in question_lower
        or ("recent" in question_lower and "learn" in question_lower)
    ):
        return recent_learnings(entries)

    mention_match = re.search(
        r"mention(?:s|ing)?\s+['\"]?(\w+)['\"]?",
        question_lower,
    )
    if mention_match:
        return entries_mentioning(entries, mention_match.group(1))

    about_match = re.search(
        r"(?:about|with|containing|include)\s+['\"]?(\w+)['\"]?",
        question_lower,
    )
    if about_match and ("entry" in question_lower or "entries" in question_lower):
        return entries_mentioning(entries, about_match.group(1))

    if "how many" in question_lower or "count" in question_lower:
        count = len(entries)
        label = "entry" if count == 1 else "entries"
        return f"You have {count} journal {label}."

    if "first entry" in question_lower or "oldest" in question_lower:
        return f"Your first entry: \"{entries[0]}\""

    if (
        "last entry" in question_lower
        or "latest entry" in question_lower
        or "most recent entry" in question_lower
    ):
        return f"Your most recent entry: \"{entries[-1]}\""

    if "recent" in question_lower:
        return recent_learnings(entries)

    words = re.findall(r"\b[a-z]{3,}\b", question_lower)
    for word in reversed(words):
        if word in SKIP_WORDS:
            continue
        matches = [entry for entry in entries if word in entry.lower()]
        if matches:
            return format_matches(word, matches)

    return (
        "I'm not sure how to answer that yet. Try asking me to summarize "
        "your journal, tell you what you've learned recently, or find "
        "entries that mention a specific word."
    )


def summarize_journal(entries):
    count = len(entries)
    label = "entry" if count == 1 else "entries"
    lines = [f"Your journal has {count} {label}."]

    recent = entries[-3:] if count >= 3 else entries
    if recent:
        lines.append("")
        lines.append("Recent entries:")
        for entry in recent:
            lines.append(f"  • {entry}")

    all_text = " ".join(entries).lower()
    themes = [theme for theme in THEME_KEYWORDS if theme in all_text]
    if themes:
        lines.append("")
        lines.append(f"Common topics: {', '.join(themes)}.")

    return "\n".join(lines)


def recent_learnings(entries):
    recent = entries[-5:] if len(entries) >= 5 else entries
    lines = ["Here are your most recent journal entries:"]
    for entry in recent:
        lines.append(f"  • {entry}")

    learning_entries = [
        entry
        for entry in recent
        if any(keyword in entry.lower() for keyword in LEARNING_KEYWORDS)
    ]
    if learning_entries:
        lines.append("")
        lines.append("Entries that look learning-related:")
        for entry in learning_entries:
            lines.append(f"  • {entry}")

    return "\n".join(lines)


def entries_mentioning(entries, keyword):
    matches = [
        entry for entry in entries if keyword.lower() in entry.lower()
    ]
    if not matches:
        return f"No entries mention \"{keyword}\"."

    lines = [
        f"Found {len(matches)} "
        f"{'entry' if len(matches) == 1 else 'entries'} "
        f"mentioning \"{keyword}\":"
    ]
    for match in matches:
        lines.append(f"  • {match}")
    return "\n".join(lines)


def format_matches(keyword, matches):
    lines = [
        f"Found {len(matches)} "
        f"{'entry' if len(matches) == 1 else 'entries'} "
        f"related to \"{keyword}\":"
    ]
    for match in matches:
        lines.append(f"  • {match}")
    return "\n".join(lines)
