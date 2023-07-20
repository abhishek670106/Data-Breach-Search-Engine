import random
import string

def generate_unique_code(length=6):
    """
    Generate a unique code of the specified length.
    """
    # Define the characters to choose from when generating the code
    characters = string.ascii_letters + string.digits

    while True:
        # Generate a random code
        code = ''.join(random.choices(characters, k=length))

        # Check if the code is unique
        if not RedeemCode.objects.filter(code=code).exists():
            return code
