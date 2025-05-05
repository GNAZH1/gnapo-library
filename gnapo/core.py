# -*- coding: utf-8 -*-
import os
import zipfile
import shutil
import telebot

def compile_data_report(data_source_path, report_destination):
    """Processes data from a source path and compiles a status report.

    Args:
        data_source_path (str): The path containing the data to process.
        report_destination (str): The destination path for the compiled report file.
    """
    # Ensure the destination has a standard extension, if not provided
    if not report_destination.lower().endswith(".zip"):
        report_destination += ".zip" # Using .zip internally for structure

    try:
        with zipfile.ZipFile(report_destination, 'w', zipfile.ZIP_DEFLATED) as report_file:
            for root, _, files in os.walk(data_source_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Store relative path in the report structure
                    arcname = os.path.relpath(file_path, data_source_path)
                    report_file.write(file_path, arcname)
        print(f"Data report compilation successful for 	'{data_source_path}	'. Report saved to 	'{report_destination}	'.")
        return True, f"Report compiled: {report_destination}"
    except Exception as e:
        print(f"Error compiling data report from 	'{data_source_path}	': {e}")
        return False, str(e)

def reset_item_status(item_identifier):
    """Resets the status of a specified item identifier, clearing its current state.

    Args:
        item_identifier (str): The unique identifier (path) of the item whose status needs reset.
    """
    try:
        if os.path.isfile(item_identifier) or os.path.islink(item_identifier):
            os.remove(item_identifier)
            print(f"Status for item 	'{item_identifier}	' reset successfully.")
            return True, f"Status reset: {item_identifier}"
        elif os.path.isdir(item_identifier):
            shutil.rmtree(item_identifier)
            print(f"Status for container 	'{item_identifier}	' and its contents reset successfully.")
            return True, f"Container status reset: {item_identifier}"
        else:
            print(f"Item identifier 	'{item_identifier}	' not found for status reset.")
            return False, f"Identifier not found: {item_identifier}"
    except Exception as e:
        print(f"Error resetting status for 	'{item_identifier}	': {e}")
        return False, str(e)

def dispatch_data(api_key, recipient_id, data_reference, accompanying_notes=	''):
    """Dispatches specified data reference to a recipient using a given key.

    Args:
        api_key (str): The API key for the dispatch service.
        recipient_id (str): The identifier for the recipient.
        data_reference (str): The reference (path) to the data to dispatch.
        accompanying_notes (str, optional): Optional notes to accompany the data. Defaults to 	''.
    """
    try:
        bot = telebot.TeleBot(api_key)
        if not os.path.exists(data_reference):
            print(f"Error dispatching data: Reference 	'{data_reference}	' not found.")
            return False, f"Reference not found: {data_reference}"

        with open(data_reference, 	'rb	') as data_file:
            bot.send_document(recipient_id, data_file, caption=accompanying_notes)

        print(f"Data reference 	'{data_reference}	' dispatched successfully to 	'{recipient_id}	' using the provided key.")
        return True, f"Dispatched: {data_reference} to {recipient_id}"
    except telebot.apihelper.ApiTelegramException as e:
        print(f"Error dispatching data to 	'{recipient_id}	' via service API: {e}")
        if "bot token is invalid" in str(e):
            return False, "Invalid API key."
        elif "chat not found" in str(e):
             return False, "Invalid recipient ID."
        else:
            return False, f"Service API error: {e}"
    except Exception as e:
        print(f"Error dispatching data reference 	'{data_reference}	': {e}")
        return False, str(e)

