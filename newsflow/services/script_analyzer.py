import math
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class ScriptStatistics:
    word_count: int
    character_count: int
    paragraph_count: int
    sentence_count: int
    scene_count: int
    estimated_runtime_seconds: int

    @property
    def estimated_runtime_display(self) -> str:
        minutes, seconds = divmod(
            self.estimated_runtime_seconds,
            60,
        )
        return f"{minutes}:{seconds:02d}"


class ScriptAnalyzer:
    DEFAULT_WORDS_PER_MINUTE = 150
    DEFAULT_SCENE_LENGTH_WORDS = 140

    SCENE_HEADING_PATTERN = re.compile(
        r"^\s*(?:"
        r"scene\s+\d+"
        r"|chapter\s+\d+"
        r"|part\s+\d+"
        r"|int\."
        r"|ext\."
        r"|int/ext\."
        r")",
        flags=re.IGNORECASE,
    )

    WORD_PATTERN = re.compile(
        r"\b[\w’'-]+\b",
        flags=re.UNICODE,
    )

    SENTENCE_PATTERN = re.compile(
        r"[.!?]+(?:\s|$)"
    )

    @classmethod
    def analyze(
        cls,
        text: str,
        words_per_minute: int | None = None,
    ) -> ScriptStatistics:
        cleaned_text = text.strip()

        if not cleaned_text:
            return ScriptStatistics(
                word_count=0,
                character_count=0,
                paragraph_count=0,
                sentence_count=0,
                scene_count=0,
                estimated_runtime_seconds=0,
            )

        words = cls.WORD_PATTERN.findall(cleaned_text)
        word_count = len(words)

        paragraphs = [
            paragraph.strip()
            for paragraph in re.split(
                r"\n\s*\n",
                cleaned_text,
            )
            if paragraph.strip()
        ]

        sentence_count = len(
            cls.SENTENCE_PATTERN.findall(cleaned_text)
        )

        if sentence_count == 0 and word_count > 0:
            sentence_count = 1

        scene_count = cls._estimate_scene_count(
            cleaned_text,
            paragraphs,
            word_count,
        )

        speaking_rate = (
            words_per_minute
            or cls.DEFAULT_WORDS_PER_MINUTE
        )

        runtime_seconds = 0

        if word_count > 0 and speaking_rate > 0:
            runtime_seconds = math.ceil(
                word_count / speaking_rate * 60
            )

        return ScriptStatistics(
            word_count=word_count,
            character_count=len(cleaned_text),
            paragraph_count=len(paragraphs),
            sentence_count=sentence_count,
            scene_count=scene_count,
            estimated_runtime_seconds=runtime_seconds,
        )

    @classmethod
    def _estimate_scene_count(
        cls,
        text: str,
        paragraphs: list[str],
        word_count: int,
    ) -> int:
        explicit_scene_headings = sum(
            1
            for line in text.splitlines()
            if cls.SCENE_HEADING_PATTERN.match(line)
        )

        if explicit_scene_headings > 0:
            return explicit_scene_headings

        if not paragraphs:
            return 0

        estimated_by_length = math.ceil(
            word_count
            / cls.DEFAULT_SCENE_LENGTH_WORDS
        )

        return max(1, estimated_by_length)