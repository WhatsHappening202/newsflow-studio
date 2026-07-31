import math
import re

from newsflow.models.storyboard import (
    Storyboard,
    StoryboardScene,
)


class StoryboardService:
    WORDS_PER_MINUTE = 150

    STOP_WORDS = {
        "the",
        "and",
        "that",
        "with",
        "this",
        "from",
        "were",
        "have",
        "they",
        "their",
        "into",
        "about",
        "there",
        "after",
        "before",
        "would",
        "could",
        "should",
        "because",
        "been",
        "your",
        "while",
        "when",
        "where",
        "which",
        "what",
        "will",
        "than",
        "then",
    }

    @classmethod
    def build_storyboard(
        cls,
        script: str,
    ) -> Storyboard:

        paragraphs = [
            p.strip()
            for p in re.split(
                r"\n\s*\n",
                script,
            )
            if p.strip()
        ]

        scenes = []

        for index, paragraph in enumerate(
            paragraphs,
            start=1,
        ):
            words = re.findall(
                r"\b[\w'-]+\b",
                paragraph.lower(),
            )

            duration = math.ceil(
                len(words)
                / cls.WORDS_PER_MINUTE
                * 60
            )

            keywords = cls._keywords(words)

            scenes.append(
                StoryboardScene(
                    number=index,
                    text=paragraph,
                    word_count=len(words),
                    duration_seconds=duration,
                    keywords=keywords,
                )
            )

        return Storyboard(scenes)

    @classmethod
    def _keywords(
        cls,
        words: list[str],
    ) -> list[str]:

        counts = {}

        for word in words:

            if (
                len(word) < 4
                or word in cls.STOP_WORDS
            ):
                continue

            counts[word] = (
                counts.get(word, 0)
                + 1
            )

        return sorted(
            counts,
            key=counts.get,
            reverse=True,
        )[:6]