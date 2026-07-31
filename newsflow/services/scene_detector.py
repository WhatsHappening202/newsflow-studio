import math
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Scene:
    number: int
    title: str
    start_position: int
    end_position: int
    text: str
    word_count: int
    estimated_duration_seconds: int

    @property
    def estimated_duration_display(self) -> str:
        minutes, seconds = divmod(
            self.estimated_duration_seconds,
            60,
        )
        return f"{minutes}:{seconds:02d}"


class SceneDetector:
    DEFAULT_WORDS_PER_MINUTE = 150
    DEFAULT_SCENE_LENGTH_WORDS = 140

    WORD_PATTERN = re.compile(
        r"\b[\w’'-]+\b",
        flags=re.UNICODE,
    )

    EXPLICIT_HEADING_PATTERN = re.compile(
        r"^\s*(?:"
        r"#{1,6}\s+.+"
        r"|scene\s+\d+(?:\s*[:\-–—]\s*.+)?"
        r"|chapter\s+\d+(?:\s*[:\-–—]\s*.+)?"
        r"|part\s+\d+(?:\s*[:\-–—]\s*.+)?"
        r"|int\.(?:/ext\.)?\s+.+"
        r"|ext\.(?:/int\.)?\s+.+"
        r"|int/ext\.\s+.+"
        r"|intro(?:duction)?"
        r"|opening"
        r"|conclusion"
        r"|closing"
        r"|outro"
        r")\s*$",
        flags=re.IGNORECASE,
    )

    @classmethod
    def detect(
        cls,
        text: str,
        words_per_minute: int | None = None,
    ) -> list[Scene]:
        if not text.strip():
            return []

        speaking_rate = (
            words_per_minute
            or cls.DEFAULT_WORDS_PER_MINUTE
        )

        heading_matches = cls._find_explicit_headings(text)

        if heading_matches:
            return cls._build_scenes_from_headings(
                text=text,
                heading_matches=heading_matches,
                words_per_minute=speaking_rate,
            )

        return cls._build_fallback_scenes(
            text=text,
            words_per_minute=speaking_rate,
        )

    @classmethod
    def _find_explicit_headings(
        cls,
        text: str,
    ) -> list[tuple[int, int, str]]:
        matches: list[tuple[int, int, str]] = []

        current_position = 0

        for line in text.splitlines(keepends=True):
            line_without_break = line.rstrip("\r\n")

            if cls.EXPLICIT_HEADING_PATTERN.match(
                line_without_break
            ):
                heading_start = current_position
                heading_end = (
                    current_position
                    + len(line_without_break)
                )

                matches.append(
                    (
                        heading_start,
                        heading_end,
                        cls._clean_heading(
                            line_without_break
                        ),
                    )
                )

            current_position += len(line)

        return matches

    @classmethod
    def _build_scenes_from_headings(
        cls,
        text: str,
        heading_matches: list[tuple[int, int, str]],
        words_per_minute: int,
    ) -> list[Scene]:
        scenes: list[Scene] = []

        first_heading_start = heading_matches[0][0]

        if text[:first_heading_start].strip():
            scenes.append(
                cls._create_scene(
                    number=1,
                    title="Opening",
                    start_position=0,
                    end_position=first_heading_start,
                    text=text[:first_heading_start],
                    words_per_minute=words_per_minute,
                )
            )

        for index, (
            heading_start,
            _heading_end,
            heading_title,
        ) in enumerate(heading_matches):
            if index + 1 < len(heading_matches):
                scene_end = heading_matches[index + 1][0]
            else:
                scene_end = len(text)

            scene_text = text[
                heading_start:scene_end
            ]

            scenes.append(
                cls._create_scene(
                    number=len(scenes) + 1,
                    title=heading_title,
                    start_position=heading_start,
                    end_position=scene_end,
                    text=scene_text,
                    words_per_minute=words_per_minute,
                )
            )

        return scenes

    @classmethod
    def _build_fallback_scenes(
        cls,
        text: str,
        words_per_minute: int,
    ) -> list[Scene]:
        paragraph_matches = list(
            re.finditer(
                r"\S(?:.*?)(?=\n\s*\n|\Z)",
                text,
                flags=re.DOTALL,
            )
        )

        if not paragraph_matches:
            return [
                cls._create_scene(
                    number=1,
                    title="Scene 1",
                    start_position=0,
                    end_position=len(text),
                    text=text,
                    words_per_minute=words_per_minute,
                )
            ]

        scenes: list[Scene] = []
        scene_start: int | None = None
        scene_end = 0
        scene_parts: list[str] = []
        current_word_count = 0

        for paragraph_match in paragraph_matches:
            paragraph_text = paragraph_match.group()
            paragraph_word_count = len(
                cls.WORD_PATTERN.findall(
                    paragraph_text
                )
            )

            if scene_start is None:
                scene_start = paragraph_match.start()

            should_finish_scene = (
                current_word_count > 0
                and (
                    current_word_count
                    + paragraph_word_count
                    > cls.DEFAULT_SCENE_LENGTH_WORDS
                )
            )

            if should_finish_scene:
                scenes.append(
                    cls._create_scene(
                        number=len(scenes) + 1,
                        title=(
                            f"Scene {len(scenes) + 1}"
                        ),
                        start_position=scene_start,
                        end_position=scene_end,
                        text="".join(scene_parts),
                        words_per_minute=words_per_minute,
                    )
                )

                scene_start = paragraph_match.start()
                scene_parts = []
                current_word_count = 0

            scene_parts.append(
                text[
                    paragraph_match.start():
                    paragraph_match.end()
                ]
            )
            scene_parts.append("\n\n")

            current_word_count += (
                paragraph_word_count
            )
            scene_end = paragraph_match.end()

        if scene_parts and scene_start is not None:
            scenes.append(
                cls._create_scene(
                    number=len(scenes) + 1,
                    title=f"Scene {len(scenes) + 1}",
                    start_position=scene_start,
                    end_position=scene_end,
                    text="".join(scene_parts).rstrip(),
                    words_per_minute=words_per_minute,
                )
            )

        return scenes

    @classmethod
    def _create_scene(
        cls,
        number: int,
        title: str,
        start_position: int,
        end_position: int,
        text: str,
        words_per_minute: int,
    ) -> Scene:
        cleaned_text = text.strip()

        word_count = len(
            cls.WORD_PATTERN.findall(cleaned_text)
        )

        duration_seconds = 0

        if word_count > 0 and words_per_minute > 0:
            duration_seconds = math.ceil(
                word_count
                / words_per_minute
                * 60
            )

        return Scene(
            number=number,
            title=title,
            start_position=start_position,
            end_position=end_position,
            text=cleaned_text,
            word_count=word_count,
            estimated_duration_seconds=(
                duration_seconds
            ),
        )

    @staticmethod
    def _clean_heading(
        heading: str,
    ) -> str:
        cleaned_heading = heading.strip()

        cleaned_heading = re.sub(
            r"^#{1,6}\s*",
            "",
            cleaned_heading,
        )

        return cleaned_heading or "Untitled Scene"