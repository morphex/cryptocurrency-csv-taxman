DEBUG = False
WARNING = False

def DEBUG_PRINT(*arguments):
    if DEBUG:
        print(*arguments, file=sys.stderr)

def WARNING_PRINT(*arguments):
    if WARNING:
        print(*arguments, file=sys.stderr)
