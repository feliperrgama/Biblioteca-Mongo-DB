import time

def loadingAnimation():
    animation = ["|", "/", "-", "\\", "|"]
    atual_time = time.time()
    fim = atual_time + 5
    i = 0

    while atual_time < fim and i < 5:
        for frame in animation:
            print('\r' + frame, end="")
            time.sleep(0.5)
            i += 1
    print('\r')
    pass

loadingAnimation()