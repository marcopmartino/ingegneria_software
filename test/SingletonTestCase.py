from unittest import TestCase

from lib.repository.OrdersRepository import OrdersRepository


class SingletonTestCase(TestCase):
    def setUp(self) -> None:
        # Nell'applicazione, tutte le repository sono Singleton (implementato tramite Metaclass)
        self.repository_instance = OrdersRepository()
        self.same_repository_instance = OrdersRepository()

    def test_singleton(self) -> None:
        self.assertEqual(self.repository_instance is self.same_repository_instance, True)
