import os

import align
import cv2
import numpy as np
import argparse
import layouts


def main():
    parser = argparse.ArgumentParser(description='Given a set of images, aligns them and outputs a 2x1 or 2x2 image.')
    parser.add_argument('filenames', metavar='N', type=str, nargs='+',
                        help='filenames to process (either 2 or 4)')

    parser.add_argument('--no-align', dest='align', action='store_false', help="By default, this script will align "
                                                                               "the images. Pass --no-align to "
                                                                               "disable this")
    parser.set_defaults(align=True)

    parser.add_argument('--convergence', dest='convergence', type=float, default=0)

    args = parser.parse_args()
    filenames = args.filenames
    assert len(filenames) == 2 or len(filenames) == 4 or len(filenames) == 8

    # Decode all images.
    ims = []
    for filename in filenames:
        im = cv2.imread(filename)
        assert im is not None
        ims.append(im)

    # Choose a reference image that we will align against.
    reference_image_index = len(ims) // 2

    if args.align:
        # Align images to match center view.
        for i in range(len(ims)):
            if i == reference_image_index:
                continue
            print(f"Aligning view {i} against view {reference_image_index}...")

            ims[i] = align.align_image(ims[i], ims[reference_image_index])

    # Adjust convergence by shifting images left and right.
    for i in range(len(ims)):
        dist_from_center = i - len(ims) / 2

        this_x_shift = args.convergence * dist_from_center

        T = np.float32([[1, 0, this_x_shift], [0, 1, 0]])

        ims[i] = cv2.warpAffine(ims[i], T, (ims[i].shape[1], ims[i].shape[0]), flags=cv2.INTER_LINEAR)

    os.makedirs('output', exist_ok=True)
    if len(ims) == 2:
        im2x1 = layouts.make_2x1(*ims)
        cv2.imwrite('output/out_2x1.jpg', im2x1)
        print("Success. Wrote result to output/out_2x1.jpg")
    elif len(ims) == 4:
        im2x2 = layouts.make_2x2(*ims)
        cv2.imwrite('output/out_2x2.jpg', im2x2)
        print("Success. Wrote result to output/out_2x2.jpg")
    elif len(ims) == 8:
        im2x4 = layouts.make_2x4(*ims)
        cv2.imwrite('output/out_2x4.jpg', im2x4)
        print("Success. Wrote result to output/out_2x4.jpg")
    else:
        raise Exception("Requires exactly 2, 4 or 8 input views")


if __name__ == "__main__":
    main()
