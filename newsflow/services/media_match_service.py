import re
from dataclasses import dataclass
from pathlib import Path

from newsflow.models.project import Project
from newsflow.models.storyboard import (
    Storyboard,
    StoryboardScene,
)
from newsflow.services.media_service import (
    MediaService,
)


@dataclass(frozen=True)
class MediaAssetMatch:
    path: Path
    media_type: str
    score: int
    matched_terms: tuple[str, ...]

    @property
    def filename(self) -> str:
        return self.path.name


@dataclass(frozen=True)
class SceneMediaMatches:
    scene_number: int
    image_matches: tuple[MediaAssetMatch, ...]
    video_matches: tuple[MediaAssetMatch, ...]

    @property
    def has_matches(self) -> bool:
        return bool(
            self.image_matches
            or self.video_matches
        )

    @property
    def image_count(self) -> int:
        return len(self.image_matches)

    @property
    def video_count(self) -> int:
        return len(self.video_matches)


class MediaMatchService:
    MAX_IMAGE_MATCHES = 4
    MAX_VIDEO_MATCHES = 2

    WORD_PATTERN = re.compile(
        r"[a-z0-9]+",
        flags=re.IGNORECASE,
    )

    STOP_WORDS = {
        "about",
        "after",
        "again",
        "also",
        "another",
        "before",
        "being",
        "because",
        "could",
        "from",
        "have",
        "into",
        "just",
        "more",
        "most",
        "other",
        "over",
        "said",
        "some",
        "such",
        "than",
        "that",
        "their",
        "there",
        "these",
        "they",
        "this",
        "through",
        "under",
        "very",
        "what",
        "when",
        "where",
        "which",
        "while",
        "with",
        "would",
        "your",
    }

    @classmethod
    def match_storyboard(
        cls,
        storyboard: Storyboard,
        project: Project,
    ) -> dict[int, SceneMediaMatches]:
        images = MediaService.list_images(project)
        videos = MediaService.list_videos(project)

        matches: dict[int, SceneMediaMatches] = {}

        for scene in storyboard.scenes:
            image_matches = cls._match_assets(
                scene=scene,
                assets=images,
                media_type="image",
                limit=cls.MAX_IMAGE_MATCHES,
            )

            video_matches = cls._match_assets(
                scene=scene,
                assets=videos,
                media_type="video",
                limit=cls.MAX_VIDEO_MATCHES,
            )

            matches[scene.number] = SceneMediaMatches(
                scene_number=scene.number,
                image_matches=tuple(image_matches),
                video_matches=tuple(video_matches),
            )

        return matches

    @staticmethod
    def coverage_percentage(
        storyboard: Storyboard,
        matches: dict[int, SceneMediaMatches],
    ) -> int:
        if not storyboard.scenes:
            return 0

        covered_scenes = sum(
            1
            for scene in storyboard.scenes
            if matches.get(
                scene.number,
                SceneMediaMatches(
                    scene_number=scene.number,
                    image_matches=(),
                    video_matches=(),
                ),
            ).has_matches
        )

        return round(
            covered_scenes
            / len(storyboard.scenes)
            * 100
        )

    @classmethod
    def _match_assets(
        cls,
        scene: StoryboardScene,
        assets: list[Path],
        media_type: str,
        limit: int,
    ) -> list[MediaAssetMatch]:
        scene_terms = cls._scene_terms(scene)

        scored_matches: list[MediaAssetMatch] = []

        for asset in assets:
            filename_terms = cls._filename_terms(asset)
            matched_terms = (
                scene_terms
                & filename_terms
            )

            if not matched_terms:
                continue

            score = cls._calculate_score(
                scene=scene,
                filename_terms=filename_terms,
                matched_terms=matched_terms,
            )

            scored_matches.append(
                MediaAssetMatch(
                    path=asset,
                    media_type=media_type,
                    score=score,
                    matched_terms=tuple(
                        sorted(matched_terms)
                    ),
                )
            )

        scored_matches.sort(
            key=lambda match: (
                -match.score,
                match.filename.lower(),
            )
        )

        return scored_matches[:limit]

    @classmethod
    def _scene_terms(
        cls,
        scene: StoryboardScene,
    ) -> set[str]:
        terms: set[str] = set()

        for keyword in scene.keywords:
            terms.update(
                cls._normalize_words(keyword)
            )

        narration_words = cls._normalize_words(
            scene.text
        )

        terms.update(
            word
            for word in narration_words
            if len(word) >= 5
        )

        return {
            term
            for term in terms
            if (
                len(term) >= 3
                and term not in cls.STOP_WORDS
            )
        }

    @classmethod
    def _filename_terms(
        cls,
        asset: Path,
    ) -> set[str]:
        filename = asset.stem.replace(
            "_",
            " ",
        ).replace(
            "-",
            " ",
        )

        return cls._normalize_words(filename)

    @classmethod
    def _normalize_words(
        cls,
        text: str,
    ) -> set[str]:
        return {
            word.lower()
            for word in cls.WORD_PATTERN.findall(
                text
            )
            if (
                len(word) >= 3
                and word.lower()
                not in cls.STOP_WORDS
            )
        }

    @classmethod
    def _calculate_score(
        cls,
        scene: StoryboardScene,
        filename_terms: set[str],
        matched_terms: set[str],
    ) -> int:
        keyword_terms: set[str] = set()

        for keyword in scene.keywords:
            keyword_terms.update(
                cls._normalize_words(keyword)
            )

        score = 0

        for term in matched_terms:
            if term in keyword_terms:
                score += 10
            else:
                score += 4

        if len(matched_terms) > 1:
            score += (
                len(matched_terms) - 1
            ) * 3

        if filename_terms and (
            filename_terms
            <= keyword_terms
        ):
            score += 5

        return score