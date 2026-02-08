import string
import random

def generate_random_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def create_unique_code():
    from .models import Product

    short_code = generate_random_code()
    
    # Keep regenerating if code already exists
    while Product.objects.filter(short_code=short_code).exists():
        short_code = generate_random_code()

    return short_code
