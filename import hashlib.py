import hashlib

# Словарь для хранения соответствий между кодом и TCP-адресом
address_mapping = {}

def generate_short_code(address, length=8):
    """
    Генерирует короткий код из TCP-адреса и сохраняет его в словаре.
    
    Parameters:
        address (str): TCP-адрес, который нужно сократить.
        length (int): Длина создаваемого короткого кода (по умолчанию 8).
    
    Returns:
        str: Короткий код указанной длины.
    """
    # Создаем хэш адреса
    hash_object = hashlib.sha256(address.encode())
    
    # Преобразуем хэш в шестнадцатеричную строку и обрезаем до нужной длины
    short_code = hash_object.hexdigest()[:length]
    
    # Сохраняем соответствие кода и адреса
    address_mapping[short_code] = address
    return short_code

def get_address_from_code(code):
    """
    Получает исходный TCP-адрес по короткому коду.
    
    Parameters:
        code (str): Короткий код.
    
    Returns:
        str: Исходный TCP-адрес или сообщение, если код не найден.
    """
    return address_mapping.get(code, "Адрес для данного кода не найден.")

# Пример использования
tcp_address = "2.tcp.ngrok.io:15555"
short_code = generate_short_code(tcp_address)

print("Сгенерированный короткий код:", short_code)
print("Исходный TCP-адрес:", get_address_from_code(short_code))
