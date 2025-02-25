import logging
from psuedo_servicenow import ServiceNow
from psuedo_ms365group import MS365Group

logger = logging.getLogger(__name__)

class ServiceInstances:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ServiceInstances, cls).__new__(cls)
        return cls._instance

    def initialize_if_needed(self):
        if not self._initialized:
            try:
                logger.info("Initializing ServiceNow...")
                self.servicenow = ServiceNow()
                
                logger.info("Initializing MS365 Group...")
                self.ms365group = MS365Group()
                
                self._initialized = True
                logger.info("All services initialized successfully")
            except Exception as e:
                logger.error(f"Error initializing services: {str(e)}")
                raise

    def get_service_now(self):
        return self.servicenow

    def get_ms365_group(self):
        return self.ms365group