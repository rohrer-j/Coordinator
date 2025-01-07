from grpc_interceptor import ClientInterceptor
import logging
_logger = logging.getLogger('grpcLogger')
logging.basicConfig(level=logging.INFO)
class ClientRequestLogger(ClientInterceptor):
    def intercept(self, method, request, context):
        # Log the outgoing request
        _logger.info(f"Sending request to method: {context.method}, Request: {request}")
        try:
            # Call the actual method
            response = method(request, context)  
            #here we could log the response
            # _logger.info(f"Received response from method: {context.method}, Response: {response}")
            return response
        
        except Exception as e:
            # Log the error
            self.log_error(e,method.__name__)
            raise
    
    def log_error(self, e: Exception, method_name) -> None:
        #_logger.error(f"Error occurred in method '{method_name}': {str(e)}")
        pass #not needed to log the error as it is logged by the grpc framework already. Could be used to log somewhere else