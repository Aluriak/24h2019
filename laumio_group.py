import laumio
import utils

class LaumioGroup:
    """Iterable over Laumio, taking care of their initialization"""

    def __init__(self, client):
        self._laumios = []



    def __iter__(self) -> [Laumio]:
        return iter(list(self._laumios))

    def as_matrix(self):
        """As __iter__, but as a matrix matching the real world distribution of laumios"""
        ...


if __name__ == '__main__':
    group = LaumioGroup()
    laumios = tuple(group)
    laumio = laumios[0]
    laumio.off()
    time.sleep(1)
    laumio.red()
    time.sleep(1)
    if laumio.temperature < 10:
        laumio.all_blue()
    if laumio.temperature > 20:
        laumio.all_red()
        laumio.bottom_ring([255, 255, 255])
    else:
        laumio.all_green()