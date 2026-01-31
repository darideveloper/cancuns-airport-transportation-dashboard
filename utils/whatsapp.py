def test_get_clean_phone(phone: str) -> str:
    """ Test get clean phone method
    
    Args:
        phone (str): Phone number not formatted
    
    Returns:
        str: Clean phone number like 5211234567890
    """
    
    clean_chars = [' ', '-', '(', ')', '+', '.']
    clean_phone = phone
    for char in clean_chars:
        clean_phone = clean_phone.replace(char, '')
        
    return clean_phone


def get_whatsapp_link(phone: str) -> str:
    """ Get WhatsApp link

    Args:
        phone (str): Phone number not formatted

    Returns:
        str: WhatsApp link like https://wa.me/5211234567890
    """
    
    if not phone:
        return ""
    
    # Add 521 at the start of the number
    number_fixed = test_get_clean_phone(phone)
    
    number_last_10 = number_fixed[-10:]
    number = f"521{number_last_10}"
    return f"https://wa.me/{number}"