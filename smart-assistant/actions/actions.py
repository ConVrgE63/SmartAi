from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import os
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Action_Create_File(Action):
    def name(self) -> Text:
        return "action_create_file"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        path = tracker.get_slot("path")
        filename = tracker.get_slot("filename")

        logger.debug(f"Retrieved path: {path}")
        logger.debug(f"Retrieved filename: {filename}")

        if not path or not filename:
            error_message = "Path or filename is missing. Please provide both."
            logger.error(error_message)
            dispatcher.utter_message(text=error_message)
            return []

        # Normalize the path
        path_with_file = os.path.normpath(os.path.join(path, filename))
        logger.debug(f"Full path: {path_with_file}")

        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(path_with_file), exist_ok=True)
            logger.debug(f"Directory ensured: {os.path.dirname(path_with_file)}")

            # Check if the file exists
            if not os.path.exists(path_with_file):
                # Create the file
                with open(path_with_file, 'w') as f:
                    f.write("This is a test file created by Rasa.")
                success_message = f"File has been created successfully at {path_with_file}"
                logger.info(success_message)
                dispatcher.utter_message(text=success_message)
            else:
                exists_message = f"File already exists at {path_with_file}"
                logger.info(exists_message)
                dispatcher.utter_message(text=exists_message)

        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            logger.error(error_message)
            dispatcher.utter_message(text=error_message)

        return []


class Action_Delete_File(Action):
    def name(self) -> Text:
        return "action_delete_file"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        path = tracker.get_slot("path")
        filename = tracker.get_slot("filename")

        logger.debug(f"Retrieved path: {path}")
        logger.debug(f"Retrieved filename: {filename}")

        if not path or not filename:
            error_message = "Path or filename is missing. Please provide both."
            logger.error(error_message)
            dispatcher.utter_message(text=error_message)
            return []

        # Normalize the path
        path_with_file = os.path.normpath(os.path.join(path, filename))
        logger.debug(f"Full path: {path_with_file}")

        try:
            # Check if the file exists
            if os.path.exists(path_with_file):
                # Delete the file
                os.remove(path_with_file)
                success_message = f"File has been deleted successfully from {path_with_file}"
                logger.info(success_message)
                dispatcher.utter_message(text=success_message)
            else:
                not_found_message = f"No such file found at {path_with_file}"
                logger.warning(not_found_message)
                dispatcher.utter_message(text=not_found_message)

        except Exception as e:
            error_message = f"An error occurred while deleting the file: {str(e)}"
            logger.error(error_message)
            dispatcher.utter_message(text=error_message)

        return []
