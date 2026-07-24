from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.platform.projects.domain.project import Project
from backend.platform.projects.infra.project_model import ProjectModel
from backend.platform.projects.repositories.project_repository import (
    ProjectRepository,
)


class ProjectRepositoryImpl(ProjectRepository):
    """
    SQLAlchemy implementation of the project repository.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def save(
        self,
        project: Project,
    ) -> Project:
        model = ProjectModel(
            id=project.id,
            organization_id=project.organization_id,
            name=project.name,
            description=project.description,
            slug=project.slug,
            created_at=project.created_at,
            updated_at=project.updated_at,
        )

        try:
            merged_model = self._session.merge(model)
            self._session.commit()
            self._session.refresh(merged_model)

        except:
            self._session.rollback()
            raise

        return self._to_domain(merged_model)

    def get_by_id(
        self,
        project_id: UUID,
    ) -> Project | None:
        model = self._session.get(
            ProjectModel,
            project_id,
        )

        if model is None:
            return None

        return self._to_domain(model)

    def list_by_organization(
        self,
        organization_id: UUID,
    ) -> list[Project]:
        statement = select(ProjectModel).where(
            ProjectModel.organization_id == organization_id,
        )

        models = self._session.scalars(statement).all()

        return [
            self._to_domain(model)
            for model in models
        ]

    def exists_by_name(
        self,
        organization_id: UUID,
        name: str,
    ) -> bool:
        statement = select(ProjectModel).where(
            ProjectModel.organization_id == organization_id,
            ProjectModel.name == name,
        )

        return self._session.scalar(statement) is not None

    @staticmethod
    def _to_domain(
        model: ProjectModel,
    ) -> Project:
        return Project(
            id=model.id,
            organization_id=model.organization_id,
            name=model.name,
            description=model.description,
            slug=model.slug,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def get_by_organization_and_slug(
        self,
        organization_id: UUID,
        slug: str,
    ) -> Project | None:

        statement = select(ProjectModel).where(
            ProjectModel.organization_id == organization_id,
            ProjectModel.slug == slug,
        )

        model = self._session.scalar(statement)

        if model is None:
            return None

        return self._to_domain(model)

    def delete(
        self,
        project_id: UUID,
    ) -> None:
        model = self._session.get(
            ProjectModel,
            project_id,
        )

        if model is None:
            return

        self._session.delete(model)
        self._session.commit()

    def update(
        self,
        project: Project,
    ) -> Project:
        model = self._session.get(
            ProjectModel,
            project.id,
        )

        if model is None:
            raise ValueError("Project not found")

        model.name = project.name
        model.description = project.description
        model.slug = project.slug
        model.updated_at = project.updated_at

        self._session.commit()
        self._session.refresh(model)

        return self._to_domain(model)