DEBUG = False

def DEBUG_PRINT(*arguments):
    if DEBUG:
        print(*arguments, file=sys.stderr)
