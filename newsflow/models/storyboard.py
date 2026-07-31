from dataclasses import dataclass


@dataclass
class StoryboardScene:
    number: int
    text: str
    word_count: int
    duration_seconds: int
    keywords: list[str]


@dataclass
class Storyboard:
    scenes: list[StoryboardScene]

    @property
    def total_duration(self) -> int:
        return sum(
            scene.duration_seconds
            for scene in self.scenes
        )

    @property
    def total_words(self) -> int:
        return sum(
            scene.word_count
            for scene in self.scenes
        )

    @property
    def scene_count(self) -> int:
        return len(self.scenes)