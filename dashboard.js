# review_pilot/core/actions.py
import requests
import logging
from typing import Dict, Any, Optional
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

class ActionExecutor:
    """Executes automated actions based on review analysis"""
    
    def __init__(self, config: Dict[str, Any]):
        self.jira_token = config.get('JIRA_API_TOKEN')
        self.jira_base_url = config.get('JIRA_BASE_URL')
        self.slack_webhook = config.get('SLACK_WEBHOOK_URL')
        self.crm_endpoint = config.get('CRM_ENDPOINT')
        
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def _make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Retry-aware HTTP request wrapper"""
        response = requests.request(method, url, timeout=30, **kwargs)
        response.raise_for_status()
        return response
    
    def automate_action(self, review_data: Dict[str, Any], action_type: str) -> Dict[str, Any]:
        """
        Execute automated action based on review analysis.
        
        Returns standardized contract for upstream pipeline:
        {
            "action": str,
            "status": "success" | "failed" | "error",
            "ticket_id"?: str,
            "message"?: str,
            "timestamp": str
        }
        """
        from datetime import datetime
        result = {
            "action": action_type,
            "status": "pending",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        try:
            if action_type == 'create_jira_ticket':
                result = self._create_jira_ticket(review_data, result)
            elif action_type == 'send_notification':
                result = self._send_notification(review_data, result)
            elif action_type == 'log_to_crm':
                result = self._log_to_crm(review_data, result)
            else:
                result.update({
                    "status": "error",
                    "message": f"Unsupported action type: {action_type}"
                })
                logger.warning(f"Unknown action type: {action_type}")
            
            logger.info(f"Action completed: {action_type} | status={result['status']}")
            return result
            
        except Exception as e:
            result.update({
                "status": "error",
                "message": str(e)
            })
            logger.error(f"Action failed: {action_type} | error={str(e)}")
            return result
    
    def _create_jira_ticket(self, review_data: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        """Create Jira ticket from review"""
        payload = {
            "project": {"key": review_data.get('project_key', 'PROD')},
            "summary": f"User Feedback: {review_data['summary'][:100]}",
            "description": f"Priority: {review_data['priority']}\n\n{review_data['text']}",
            "issuetype": {"name": "Task"},
            "priority": {"name": review_data.get('priority', 'Medium')}
        }
        
        response = self._make_request(
            "POST",
            f"{self.jira_base_url}/rest/api/3/issue",
            json=payload,
            headers={"Authorization": f"Bearer {self.jira_token}", "Content-Type": "application/json"}
        )
        
        result.update({
            "status": "success" if r
