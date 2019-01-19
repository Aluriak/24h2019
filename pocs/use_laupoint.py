

from laupoint import laupoint
laupoint.set_opt(host='mpd.lan', port=1883)


def right_left_walk(size:int) -> [int]:
    """Yield index of objects to visit for a right left walk

    >>> tuple(right_left_walk(5))
    (2, 3, 1, 4, 0)

    """
    laupoint(color='sienna', duration=2)
    middle = size // 2
    yield middle
    low, up = middle-1, middle+1
    change = True
    while change:
        change = False
        if up < size:
            laupoint(color='red')
            yield up
            up += 1
            change = True
        if low >= 0:
            laupoint(color='blue')
            yield low
            low -= 1
            change = True
    laupoint()


if __name__ == '__main__':
    print('RUNNING…')
    tuple(right_left_walk(10))
    print('END')
