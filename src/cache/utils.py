def key_gen(*args) -> str:
    return ':'.join([str(arg) for arg in args])
