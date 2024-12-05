import random
import string

def generate_password(length=12, include_special=True):
    """
    Generate a secure random password.

    Parameters:
        length (int): Length of the password to be generated. Must be at least 8 characters.
        include_special (bool): Whether to include special characters in the password.

    Returns:
        str: A randomly generated password.
    
    Raises:
        ValueError: If the length is less than 8.
    """

    if length < 8:
        raise ValueError("Password length must be at least 8 characters.")

    # Define character pools
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    digits = string.digits
    special = "!@#$%^&*()_+" if include_special else ""

    # Ensure the password includes at least one character from each pool
    all_characters = lower + upper + digits + special
    if not all_characters:
        raise ValueError("No character sets selected for password generation.")

    # Start with one guaranteed character from each selected pool
    password = (
        random.choice(lower)
        + random.choice(upper)
        + random.choice(digits)
    )
    if include_special:
        password += random.choice(special)

    # Fill the rest of the password length with random choices
    remaining_length = length - len(password)
    password += ''.join(random.choices(all_characters, k=remaining_length))

    # Shuffle to ensure randomness
    password = ''.join(random.sample(password, len(password)))

    return password

# Optional: Test the function locally
if __name__ == "__main__":
    print("Generated Password (12 characters, with specials):", generate_password())
    print("Generated Password (16 characters, no specials):", generate_password(16, include_special=False))
