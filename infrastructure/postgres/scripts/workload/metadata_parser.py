from infrastructure.postgres.scripts.models.enums import (
    Difficulty,
    ExpectedIssue,
    QueryCategory,
)


class MetadataParser:

    @staticmethod
    def parse(lines: list[str]):

        metadata = {}

        for line in lines:

            if not line.startswith("--"):
                break

            key, value = line[2:].split(":", 1)

            metadata[key.strip()] = value.strip()

        return {
            "id": metadata["id"],
            "name": metadata["name"],
            "category": QueryCategory(metadata["category"]),
            "difficulty": Difficulty(metadata["difficulty"]),
            "expected_issue": ExpectedIssue(
                metadata["expected_issue"]
            ),
        }