from backend.app.graph.state import AgentState
from backend.app.tools.mock_services import get_available_slots, book_appointment_api
from backend.app.models.alerts import BookingConfirmation

def scheduling_agent(state: AgentState):
    """Books the appointment."""
    print("--- 📅 Scheduling Service ---")
    
    if state.get("customer_response") != "yes":
        return state

    # 1. Fetch Slots
    slots = get_available_slots()
    # 2. Pick first slot for automation
    chosen_slot = slots[0]
    
    # 3. Book
    booking = book_appointment_api(state['vehicle_id'], chosen_slot)
    
    state['booking_confirmation'] = BookingConfirmation(**booking)
    return state