import pytest
from unittest.mock import Mock

from pyqube.events.exceptions import InvalidTicketHandlerArgumentsError
from pyqube.events.handlers import TicketHandler
from pyqube.types import AnsweringTicket, PublicTicket


# Concrete subclass for testing purposes
class ConcreteTicketHandler(TicketHandler):

    def subscribe_to_topic(self, topic: str, handler: Mock):
        pass


class TestTicketHandler:

    @pytest.fixture
    def ticket_handler(self):
        """Fixture to create a concrete instance of TicketHandler."""
        handler = ConcreteTicketHandler()
        handler.location_id = 1
        return handler

    @pytest.fixture
    def mock_add_mqtt_handler(self):
        """Fixture to mock add_mqtt_handler method of ConcreteTicketHandler."""
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(ConcreteTicketHandler, 'add_mqtt_handler', Mock())
            yield

    def test_on_ticket_generated(self, ticket_handler):
        """Test that on_ticket_generated registers the correct handler."""
        handler = ticket_handler.on_ticket_generated()
        assert handler is not None

    def test_on_ticket_called_with_counter_id(self, ticket_handler):
        """Test that on_ticket_called registers the correct handler for counter_id."""
        handler = ticket_handler.on_ticket_called(counter_id=124)
        assert handler is not None

    def test_on_ticket_called_with_counter_id_builds_correct_topic(self, ticket_handler, mock_add_mqtt_handler):
        """Test that on_ticket_called builds the correct topic for queue_id."""
        ticket_handler.on_ticket_called(counter_id=124)
        ticket_handler.add_mqtt_handler.assert_called_once_with(
            "locations/1/counters/124/tickets/called", AnsweringTicket
        )

    def test_on_ticket_called_with_queue_id(self, ticket_handler):
        """Test that on_ticket_called registers the correct handler for queue_id."""
        handler = ticket_handler.on_ticket_called(queue_id=90)
        assert handler is not None

    def test_on_ticket_called_with_queue_id_builds_correct_topic(self, ticket_handler, mock_add_mqtt_handler):
        """Test that on_ticket_called builds the correct topic for queue_id."""
        ticket_handler.on_ticket_called(queue_id=90)
        ticket_handler.add_mqtt_handler.assert_called_once_with("locations/1/queues/90/tickets/called", AnsweringTicket)

    def test_on_ticket_called_with_no_arguments(self, ticket_handler):
        """Test that on_ticket_called registers the correct handler when no arguments are provided."""
        handler = ticket_handler.on_ticket_called()
        assert handler is not None

    def test_on_ticket_called_with_no_arguments_builds_correct_topic(self, ticket_handler, mock_add_mqtt_handler):
        """Test that on_ticket_called builds the correct topic when no arguments are provided."""
        ticket_handler.on_ticket_called()
        ticket_handler.add_mqtt_handler.assert_called_once_with("locations/1/queues/+/tickets/called", AnsweringTicket)

    def test_invalid_ticket_handler_arguments(self, ticket_handler):
        """Test the behavior when both queue_id and counter_id are provided."""
        with pytest.raises(InvalidTicketHandlerArgumentsError):
            ticket_handler.on_ticket_called(queue_id=90, counter_id=124)

    def test_on_ticket_changed_state(self, ticket_handler):
        """Test that on_ticket_changed_state registers the correct handler."""
        handler = ticket_handler.on_ticket_changed_state()
        assert handler is not None

    def test_on_ticket_changed_state_builds_correct_topic(self, ticket_handler, mock_add_mqtt_handler):
        """Test that on_ticket_changed_state builds the correct topic."""
        ticket_handler.on_ticket_changed_state()
        ticket_handler.add_mqtt_handler.assert_called_once_with("locations/1/tickets/+/changed-state", PublicTicket)
