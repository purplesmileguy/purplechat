import base64

def xor_encrypt_decrypt(text, key):
    """
    Функция для шифрования или дешифрования текста с использованием XOR.
    :param text: Строка для обработки.
    :param key: Ключ в виде строки.
    :return: Результат обработки (зашифрованный или расшифрованный текст).
    """
    key_length = len(key)
    return ''.join(chr(ord(c) ^ ord(key[i % key_length])) for i, c in enumerate(text))

def encrypt_token(token, key):
    """
    Шифрует токен с использованием XOR и кодирует его в Base64.
    :param token: Строка токена.
    :param key: Ключ в виде строки.
    :return: Зашифрованный и закодированный в Base64 токен.
    """
    encrypted = xor_encrypt_decrypt(token, key)  # Шифрование с использованием XOR
    return base64.b64encode(encrypted.encode()).decode()  # Кодирование в Base64

def decrypt_token(encrypted_token, key):
    """
    Декодирует Base64 и расшифровывает токен с использованием XOR.
    :param encrypted_token: Зашифрованный и закодированный токен.
    :param key: Ключ в виде строки.
    :return: Расшифрованный токен.
    """
    decoded = base64.b64decode(encrypted_token).decode()  # Декодирование из Base64
    return xor_encrypt_decrypt(decoded, key)  # Расшифровка с использованием XOR

# Пример использования
token = '2FFYyLixssmJJidyeY7TffhZNnK_6Z5rQeLFgguyomK5HadFJ'
key = 'chat'

# Шифрование
encrypted_token = encrypt_token(token, key)
print("Encrypted Token:", encrypted_token)

# Дешифрование
decrypted_token = decrypt_token(encrypted_token, key)
print("Decrypted Token:", decrypted_token)
