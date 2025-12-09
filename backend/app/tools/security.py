import logging

logger = logging.getLogger("ueba_security")

AGENT_PERMISSIONS = {
    "diagnosis_agent": ["get_vehicle_data"],
    "scheduling_agent": ["get_available_slots", "book_appointment_api"],
    "insights_agent": ["search_rca_database"]
}

def secure_tool_execute(agent_name: str, tool_func, **kwargs):
    """
    UEBA Wrapper: Checks if the agent is allowed to use the tool.
    """
    tool_name = tool_func.__name__
    
    if tool_name not in AGENT_PERMISSIONS.get(agent_name, []):
        alert_msg = f"🚨 UEBA ALERT: Unauthorized access attempt! Agent '{agent_name}' tried to use '{tool_name}'."
        logger.critical(alert_msg)
        print(alert_msg) 
        raise PermissionError(f"Access Denied: {agent_name} cannot use {tool_name}")
    
    logger.info(f"UEBA: Access granted for {agent_name} -> {tool_name}")
    return tool_func(**kwargs)