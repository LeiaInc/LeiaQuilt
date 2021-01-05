"""
Align images.
1. Find keypoints.
2. Find matching keypoints.
3. Calculate homography.
4. Apply homography.
Adapted from https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_feature_homography/py_feature_homography.html.
"""

import numpy as np
import cv2
import joblib.memory

# Align image takes a few seconds. Since it may be called multiple times with the same inputs, cache the function.
memory = joblib.memory.Memory(location='/tmp/leiaquilt_cache', verbose=False)


@memory.cache
def align_image(image_to_align, reference_image):
    """
    Uses OpenCV to align an image to a reference image.
    """
    MIN_MATCH_COUNT = 10

    sift = cv2.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(reference_image, None)
    kp2, des2 = sift.detectAndCompute(image_to_align, None)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(des1, des2, k=2)

    # store all the good matches as per Lowe's ratio test.
    good = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good.append(m)

    assert len(good) >= MIN_MATCH_COUNT, "only found %d matches" % len(good)
    dst_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    src_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

    h, w, c = image_to_align.shape
    return cv2.warpPerspective(image_to_align, M, (w, h), borderMode=cv2.BORDER_REPLICATE)
