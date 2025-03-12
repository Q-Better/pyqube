from pyqube.events.clients import MQTTClient
from pyqube.rest.clients import RestClient


class QubeClient(RestClient, MQTTClient):
    """
    A unified client that combines both MQTT and REST capabilities.
    It supports interacting with MQTT brokers for real-time messaging and with a REST API for general requests.
    """

    def __init__(
        self,
        api_key: str,
        location_id: int,
        api_host: str = None,
        broker_host: str = None,
        broker_port: int = None,
        queue_management_manager: object = None
    ):
        """
        Initializes the QubeClient by setting up both MQTT and REST components.

        Args:
            api_key (str): API key for client authentication.
            location_id (int): Location ID to use in requests.
            api_host (str, optional): Host for REST API requests. Defaults to RestClient.DEFAULT_API_HOST.
            broker_host (str, optional): Host of the MQTT broker. Defaults to MQTTClient.DEFAULT_BROKER_HOST.
            broker_port (int, optional): Port of the MQTT broker. Defaults to MQTTClient.DEFAULT_BROKER_PORT.
            queue_management_manager (object, optional): Manager used for queue management via REST API.
        """
        RestClient.__init__(self, api_key, location_id, queue_management_manager, api_host)
        MQTTClient.__init__(self, api_key, location_id, broker_host, broker_port)
