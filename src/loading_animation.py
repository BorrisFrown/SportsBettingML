import itertools
import threading
import time
import sys


class Animation:
    # TODO: Make a subclass that also counts how many pages out of total pages
    """Class designed for threading a loading symbol"""
    def __init__(self):
        self._done = False

    def stop(self):
        """Stop the running animation"""
        self._done = True

    def start(self):
        """Indefinitely play the loading animation until animation.stop()"""
        t = threading.Thread(target=self._animate)
        t.start()

    def _animate(self):
        """The actual animation logic"""
        for c in itertools.cycle(['', '.', '..', '...']):
            if self._done:
                break
            sys.stdout.write('\r' + c)
            sys.stdout.flush()
            time.sleep(0.5)


def test_animation():
    """Function to test the animation. Will run animation for 5 seconds."""
    ani = Animation()
    ani.start()
    time.sleep(5)
    ani.stop()
