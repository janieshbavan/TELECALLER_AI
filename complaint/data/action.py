from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionSaveComplaint(Action):
    def name(self) -> str:
        return "action_save_complaint"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict):
        issue = tracker.latest_message.get('text')
        print(f"[📂 Complaint Saved] Company: Excite Pvt Ltd | Issue: {issue}")
        # Save to database or file if needed
        return [SlotSet("issue_description", issue)]
