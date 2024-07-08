from unittest import TestCase

from lib.repository.ArticlesRepository import ArticlesRepository


class ObserverTestCase(TestCase):
    def setUp(self) -> None:

        # Metodo eseguito a ogni ricezione di un messaggio
        def on_message_received(message):
            self.received_message = message

        # Inizializzo il messaggio da inviare e il messaggio ricevuto
        self.sent_message = "Questo è un messaggio di prova"
        self.received_message = None

        # Inizializzo l'osservato e l'osservatore
        self.observable_object = ArticlesRepository()
        self.observer = self.observable_object.observe(on_message_received)

    def test_observer(self) -> None:
        # Invia la notifica e verifica che il messaggio sia arrivato
        self.observable_object.notify(self.sent_message)
        self.assertEqual(self.received_message, self.sent_message)

        # Rimuove l'osservatore, invia la notifica e verifica che il messaggio non sia arrivato
        self.received_message = None
        self.observable_object.detach(self.observer)
        self.observable_object.notify(self.sent_message)
        self.assertEqual(self.received_message, None)


