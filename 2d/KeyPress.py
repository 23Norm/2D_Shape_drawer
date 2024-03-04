from typing import List, Dict

def get_pressed_status(event):
    result: Dict[str, List|str] = {}
    for part in str(event).split():
        if 'state=' in part:
            state_value = part.split('=')[1]
            state_value = state_value.rstrip('>')
            result["state"] = state_value.split('|') if '|' in state_value else state_value

        if 'keysym=' in part:
            key_value = part.split('=')[1]
            key_value = key_value.rstrip('>')
            result["key"] = key_value

    return result
