from sqlalchemy import select

from app.database.session import SessionLocal
from app.repository.models import Repository


class RepositoryRepository:

    def create(
        self,
        user_id: str,
        repository_name: str,
        repository_url: str,
    ):

        with SessionLocal() as session:

            repository = Repository(
                user_id=user_id,
                repository_name=repository_name,
                repository_url=repository_url,
            )

            session.add(repository)
            session.commit()
            session.refresh(repository)

            session.expunge(repository)

            return repository

    def exists(
        self,
        user_id: str,
        repository_name: str,
    ):

        with SessionLocal() as session:

            return (
                session.execute(
                    select(Repository).where(
                        Repository.user_id == user_id,
                        Repository.repository_name == repository_name,
                    )
                ).scalar_one_or_none()
                is not None
            )

    def get(
        self,
        repository_id: str,
    ):

        with SessionLocal() as session:

            repository = session.get(
                Repository,
                repository_id,
            )

            if repository is not None:

                session.refresh(repository)
                session.expunge(repository)

            return repository

    def get_by_name(
        self,
        user_id: str,
        repository_name: str,
    ):

        with SessionLocal() as session:

            repository = session.execute(
                select(Repository).where(
                    Repository.user_id == user_id,
                    Repository.repository_name == repository_name,
                )
            ).scalar_one_or_none()

            if repository is not None:

                session.refresh(repository)
                session.expunge(repository)

            return repository

    def list(
        self,
        user_id: str,
    ):

        with SessionLocal() as session:

            repositories = (
                session.execute(
                    select(Repository)
                    .where(
                        Repository.user_id == user_id,
                    )
                    .order_by(
                        Repository.created_at.desc()
                    )
                )
                .scalars()
                .all()
            )

            for repository in repositories:
                session.expunge(repository)

            return repositories

    def delete(
        self,
        repository_id: str,
    ):

        with SessionLocal() as session:

            repository = session.get(
                Repository,
                repository_id,
            )

            if repository:

                session.delete(repository)
                session.commit()