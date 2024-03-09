import hashlib

def generate_salt(input_string):
    salt_builder = ""
    for i in range(2, len(input_string), 3):  # Adjusted for 0-based indexing
        ascii_value = ord(input_string[i])
        # Prepend the string representation of the sum of the length and ASCII value
        # Python's str() does not add a leading space like VBA's STR(), so we directly concatenate
        if salt_builder=="":
            salt_builder = str(abs(len(input_string)) + ascii_value)
        else:     
            salt_builder = str(str(abs(len(input_string)) + ascii_value) + " " +  salt_builder)
    return salt_builder


def compute_unique_company_key(company_name):
    input_string = company_name
    salt = generate_salt(input_string)
    input_with_salt = input_string + " " + salt
    print("input_with_salt",input_with_salt)
    
    byte_data = input_with_salt.encode('utf-8')

    
    # Compute the SHA256 hash
    sha256_hash = hashlib.sha256(byte_data).hexdigest()

    
    return sha256_hash



