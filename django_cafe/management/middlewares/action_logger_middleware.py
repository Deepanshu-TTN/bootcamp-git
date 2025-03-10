import time
import logging
from datetime import datetime

action_logger = logging.getLogger('items')

class ItemActivitiesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time

        if self._is_target_app(request.path):
            operation = self._get_operation(request)
            model_id = self._get_model_id(request.path)
            user = request.user
            if operation:
                action_logger.info(
                    f'User: {user.username}({user.id}) | '
                    f'Operation: {operation} | '
                    f'Item ID: {model_id} | '
                    f'Time: {datetime.now()} | '
                    f'Executed in: {duration}'
                )
                
        return response
    

    def _is_target_app(self, path):
        return '/manage/' in path
    
    def _get_operation(self, request):
        if request.method == "POST":
            if 'add/' in request.path:
                return 'Create'
            if 'remove/' in request.path:
                return 'Delete'
            if 'update/' or 'edit/' in request.path:
                return 'Update'

            return 'Other'
        
        return None

    def _get_model_id(self, path):
        for i, part in enumerate(path.strip('/').split('/')):
            if part.isdigit() and i>0:
                return part
        return None