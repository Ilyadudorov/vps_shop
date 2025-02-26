import random


def generate_random_mac_address():
    """Generate a random MAC address.

    Note: The second digit is set to be an even number to create a unicast
    and universally administered MAC address.
    """
    # Generate 11 random hexadecimal digits
    digits = [random.choice('0123456789ABCDEF') for _ in range(11)]

    # Add an even hexadecimal digit for the second character
    second_digit = random.choice('02468ACE')
    digits.insert(1, second_digit)

    # Format the digits into a valid MAC address format
    mac_address = ':'.join(''.join(digits[i:i + 2]) for i in range(0, 12, 2))

    return mac_address