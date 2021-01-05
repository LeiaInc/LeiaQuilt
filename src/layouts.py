import numpy as np


def make_2x1(v0, v1):
    width = v1.shape[1]
    height = v1.shape[0]

    out_buf = np.ndarray((height, width * 2, 3))
    out_buf[:height, :width] = v0
    out_buf[:height, width:] = v1
    return out_buf


def make_2x2(v0, v1, v2, v3):
    width = v1.shape[1]
    height = v1.shape[0]

    out_buf = np.ndarray((height * 2, width * 2, 3))
    out_buf[:height, :width] = v0
    out_buf[:height, width:] = v1
    out_buf[height:, :width] = v2
    out_buf[height:, width:] = v3
    return out_buf


def make_2x4(v0, v1, v2, v3, v4, v5, v6, v7):
    width = v1.shape[1]
    height = v1.shape[0]

    out_buf = np.ndarray((height * 4, width * 2, 3))
    out_buf[:height, :width] = v0
    out_buf[:height, width:] = v1
    out_buf[height:2*height, :width] = v2
    out_buf[height:2*height, width:] = v3
    out_buf[2*height:3*height, :width] = v4
    out_buf[2*height:3*height, width:] = v5
    out_buf[3*height:4*height, :width] = v6
    out_buf[3*height:4*height, width:] = v7
    return out_buf
