import math
import re
from dataclasses import dataclass

from newsflow.services.scene_detector import (
    SceneDetector,
)


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

        words = cls.WORD_PATTERN.findall(
            cleaned_text
        )
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
            cls.SENTENCE_PATTERN.findall(
                cleaned_text
            )
        )

        if sentence_count == 0 and word_count > 0:
            sentence_count = 1

        speaking_rate = (
            words_per_minute
            or cls.DEFAULT_WORDS_PER_MINUTE
        )

        runtime_seconds = 0

        if word_count > 0 and speaking_rate > 0:
            runtime_seconds = math.ceil(
                word_count
                / speaking_rate
                * 60
            )

        scenes = SceneDetector.detect(
            text,
            words_per_minute=speaking_rate,
        )

        return ScriptStatistics(
            word_count=word_count,
            character_count=len(cleaned_text),
            paragraph_count=len(paragraphs),
            sentence_count=sentence_count,
            scene_count=len(scenes),
            estimated_runtime_seconds=runtime_seconds,
        )