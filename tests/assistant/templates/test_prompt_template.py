import pytest

from backend.assistant.templates.prompt_template import (
    PromptTemplate,
)
from backend.knowledge.models.explanation import (
    Explanation,
)
from backend.knowledge.models.explanation_metadata import (
    ExplanationMetadata,
)
from backend.knowledge.models.explanation_snapshot import (
    ExplanationSnapshot,
)


class FakeTemplate(
    PromptTemplate,
):

    def render(
        self,
        explanation: ExplanationSnapshot,
    ) -> str:

        return "Hello"


def test_prompt_template():

    snapshot = ExplanationSnapshot(
        metadata=ExplanationMetadata(
            objective="test",
            section_count=0,
        ),
        explanation=Explanation(),
    )

    template = FakeTemplate()

    assert (
        template.render(
            snapshot,
        )
        == "Hello"
    )