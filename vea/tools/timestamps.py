def get_timestamps(frames):
    """ Parse the frames value to generate timestamps. """
    timestamps = []
    start = None
    end = None
    prev_end = 0
    for i in range(0, len(frames)):
        if frames[i] > 0:
            if start is None:
                start = i
            prev_end += 1

        else:
            if end is None and start is not None:
                end = start + prev_end - 1
                if start == end:
                    end = None

        if start is not None and end is not None:
            start = start
            end = end
            timestamps.append([start, end])
            end = None
            start = None
            prev_end = 0

    if start is not None and end is None:
        end = len(frames)
        timestamps.append([start, end])

    return timestamps
