import random, string


def random_str(len):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=len))
