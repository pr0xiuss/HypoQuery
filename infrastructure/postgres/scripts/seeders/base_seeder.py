from abc import ABC, abstractmethod

from infrastructure.postgres.scripts.common.logger import get_logger
from infrastructure.postgres.scripts.interfaces.seeder import Seeder


class BaseSeeder(Seeder, ABC):

    def __init__(self, repository):
        self.repository = repository
        self.connection = repository.connection
        self.logger = get_logger(self.__class__.__name__)

    def run(self) -> None:
        """
        Template Method.

        Defines the complete lifecycle of every seeder.
        """

        self.logger.info(f"Starting {self.__class__.__name__}")

        try:
            self.before_run()

            self.repository.truncate()

            data = self.generate()

            self.persist(data)

            self.validate()

            self.connection.commit()

            self.after_run()

            self.logger.info(
                f"{self.__class__.__name__} completed successfully."
            )

        except Exception:
            self.connection.rollback()

            self.logger.exception(
                f"{self.__class__.__name__} failed."
            )

            raise

    def before_run(self) -> None:
        """
        Optional hook executed before generation starts.
        """
        pass

    @abstractmethod
    def generate(self):
        """
        Generate domain objects.
        """
        raise NotImplementedError

    @abstractmethod
    def persist(self, data) -> None:
        """
        Persist generated objects.
        """
        raise NotImplementedError

    def validate(self) -> None:
        """
        Optional validation hook.
        """
        pass

    def after_run(self) -> None:
        """
        Optional hook executed after successful completion.
        """
        pass