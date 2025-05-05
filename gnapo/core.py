# -*- coding: utf-8 -*-
import os
import zipfile
import shutil

def package_items(source_dir, output_filename):
    """Processes items in a directory and packages them.

    Args:
        source_dir (str): The directory containing items to package.
        output_filename (str): The name for the resulting package file (should end with .zip).
    """
    if not output_filename.endswith('.zip'):
        output_filename += '.zip'
    
    try:
        with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Arcname ensures the path inside zip is relative to source_dir
                    arcname = os.path.relpath(file_path, source_dir)
                    zipf.write(file_path, arcname)
        print(f"Items from '{source_dir}' successfully packaged into '{output_filename}'.")
        return True, f"Package created: {output_filename}"
    except Exception as e:
        print(f"Error packaging items from '{source_dir}': {e}")
        return False, str(e)

def cleanup_space(target_path):
    """Removes specified entries to manage space.

    Args:
        target_path (str): The file or directory path to remove.
    """
    try:
        if os.path.isfile(target_path) or os.path.islink(target_path):
            os.remove(target_path)
            print(f"Entry '{target_path}' removed successfully.")
            return True, f"Entry removed: {target_path}"
        elif os.path.isdir(target_path):
            shutil.rmtree(target_path)
            print(f"Directory '{target_path}' and its contents removed successfully.")
            return True, f"Directory removed: {target_path}"
        else:
            print(f"Entry '{target_path}' does not exist.")
            return False, f"Entry not found: {target_path}"
    except Exception as e:
        print(f"Error cleaning up space for '{target_path}': {e}")
        return False, str(e)




import telebot

def dispatch_data(api_key, recipient_id, item_path, caption_text=''):
    """Dispatches specified data item to a recipient using a given key.

    Args:
        api_key (str): The API key for the dispatch service.
        recipient_id (str): The identifier for the recipient.
        item_path (str): The path to the data item to dispatch.
        caption_text (str, optional): Optional text to accompany the item. Defaults to ''.
    """
    try:
        bot = telebot.TeleBot(api_key)
        if not os.path.exists(item_path):
            print(f"Error dispatching data: Item \'{item_path}\' not found.")
            return False, f"Item not found: {item_path}"

        with open(item_path, 'rb') as item_file:
            bot.send_document(recipient_id, item_file, caption=caption_text)
        
        print(f"Data item \'{item_path}\' dispatched successfully to \'{recipient_id}\' using the provided key.")
        return True, f"Dispatched: {item_path} to {recipient_id}"
    except telebot.apihelper.ApiTelegramException as e:
        print(f"Error dispatching data to \'{recipient_id}\' via Telegram API: {e}")
        # Check for common errors like invalid token or chat ID
        if "bot token is invalid" in str(e):
            return False, "Invalid API key (bot token)."
        elif "chat not found" in str(e):
             return False, "Invalid recipient ID (chat not found)."
        else:
            return False, f"Telegram API error: {e}"
    except Exception as e:
        print(f"Error dispatching data item \'{item_path}\': {e}")
        return False, str(e)

