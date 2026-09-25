"""Live webcam capture with OpenCV.

This module is the input side of the recognition system. Its only job is to
open the physical webcam, hand out live frames, show them, and shut everything
down cleanly. The physical camera is the live input: there is no folder of
images standing in for it.

Why OpenCV VideoCapture
-----------------------
``cv2.VideoCapture`` is the standard way to talk to a camera from Python. It
wraps the operating system's video layer (V4L2 on Linux, Media Foundation on
Windows, AVFoundation on macOS), so the same few lines open a real camera on
any of them, and it returns frames already decoded into plain NumPy arrays. No
extra driver, server or GUI toolkit is needed.

Format of a frame
-----------------
A frame is exactly what OpenCV produces, and this module never alters it:

    type   numpy.ndarray
    dtype  uint8
    shape  (height, width, 3)
    order  BGR, i.e. blue, green, red

Nothing is resized, converted or encoded here. That is deliberate: MTCNN needs
BGR and turns it to RGB itself, and the FaceNet stage resizes the face crops
itself. Doing any of that in this module would only waste time in the loop.

How the final pipeline will use this
------------------------------------
``run_webcam_loop`` reads a frame, passes it to an optional callback, and shows
whatever the callback returns. In this step the callback is absent, so raw
frames are displayed. Later ``main.py`` will pass a callback that runs MTCNN,
FaceNet and the matching step and draws the boxes and labels on the frame. The
loop, the frame format and the exit handling stay exactly as they are, so no
recognition code is needed here.

How the webcam lifecycle is handled
-----------------------------------
Opening a camera allocates a device that stays open until it is released, and
``cv2.imshow`` creates windows that stay on screen until they are destroyed.
Both are cleaned up in one place: ``open_webcam`` is a context manager whose
``finally`` block always calls ``VideoCapture.release()`` and
``cv2.destroyAllWindows()``. So the camera is released and the windows close
both when the loop finishes normally and when it is interrupted by an
exception or Ctrl+C.
"""

from __future__ import annotations

import sys
from collections.abc import Callable, Iterator
from contextlib import contextmanager

import cv2
import numpy as np


# The default camera of the machine. Kept as a constant so it is never written
# as a literal somewhere else in the code.
DEFAULT_CAMERA_INDEX = 0

# Pressing this key ends the webcam session.
DEFAULT_EXIT_KEY = "q"

DEFAULT_WINDOW_NAME = "Lab5 - Webcam Capture"


def _check_camera_index(camera_index: int) -> int:
    """Check that the camera index is a valid device number."""
    if isinstance(camera_index, bool) or not isinstance(camera_index, (int, np.integer)):
        raise ValueError(
            f"The camera index must be an integer, got {type(camera_index)}."
        )
    if camera_index < 0:
        raise ValueError(
            f"The camera index must be zero or positive, got {camera_index}."
        )
    return int(camera_index)


def _check_exit_key(exit_key: str) -> str:
    """Check that the exit key is a single character."""
    if not isinstance(exit_key, str) or len(exit_key) != 1:
        raise ValueError(
            f"The exit key must be a single character, got {exit_key!r}."
        )
    return exit_key


@contextmanager
def open_webcam(
    camera_index: int = DEFAULT_CAMERA_INDEX,
) -> Iterator[cv2.VideoCapture]:
    """Open a webcam and release it again when the block is finished.

    Usage::

        with open_webcam() as capture:
            ...

    Arguments:
        camera_index {int} -- which camera to open; 0 is the default camera.
            (default: {0})

    Yields:
        cv2.VideoCapture -- the opened camera, to be passed to ``read_frame()``.

    Raises:
        ValueError -- if the camera index is not a valid device number.
        RuntimeError -- if the camera cannot be opened. This is raised straight
            away instead of retrying silently, so a missing camera or a wrong
            index is reported at once rather than looping forever.

    The camera is always released and all OpenCV windows are always destroyed
    when the ``with`` block ends, including when an exception is raised inside
    it.
    """
    checked_index = _check_camera_index(camera_index)

    capture = cv2.VideoCapture(checked_index)
    if not capture.isOpened():
        # release() on a capture that never opened is still correct to call, so
        # no device handle is left behind on this failure path.
        capture.release()
        raise RuntimeError(
            f"Could not open the webcam at index {checked_index}. "
            "Check that a camera is connected and not already in use by "
            "another program."
        )

    try:
        yield capture
    finally:
        capture.release()
        cv2.destroyAllWindows()


def read_frame(capture: cv2.VideoCapture) -> np.ndarray | None:
    """Read the next live frame from the camera.

    Arguments:
        capture {cv2.VideoCapture} -- an opened camera from ``open_webcam()``.

    Returns:
        np.ndarray -- the frame as a uint8 NumPy array of shape
        (height, width, 3) in BGR order, or None if the frame could not be
        read. A None result means the camera stopped delivering frames, for
        example because it was unplugged, and is a normal way for a capture to
        end rather than an error to raise.
    """
    success, frame = capture.read()
    if not success or frame is None:
        return None
    return frame


def show_frame(frame: np.ndarray, window_name: str = DEFAULT_WINDOW_NAME) -> None:
    """Display one frame in an OpenCV window.

    The frame is shown exactly as it was captured. Drawing face boxes and
    recognition labels on it is the job of the later integration step, not of
    this module.
    """
    cv2.imshow(window_name, frame)


def is_exit_key_pressed(exit_key: str = DEFAULT_EXIT_KEY) -> bool:
    """Return True when the user pressed the exit key.

    ``cv2.waitKey`` is what both keeps the window responsive and reports the
    pressed key. It returns -1 when nothing was pressed, and encodes the special
    arrow keys as larger numbers, so only the lowest byte is compared with the
    exit key.
    """
    pressed_key = cv2.waitKey(1)
    if pressed_key == -1:
        return False
    return pressed_key & 0xFF == ord(exit_key)


def run_webcam_loop(
    camera_index: int = DEFAULT_CAMERA_INDEX,
    on_frame: Callable[[np.ndarray], np.ndarray] | None = None,
    exit_key: str = DEFAULT_EXIT_KEY,
    window_name: str = DEFAULT_WINDOW_NAME,
) -> int:
    """Run the capture loop until the user presses the exit key.

    Each iteration reads a live frame, hands it to ``on_frame``, and displays
    the frame that ``on_frame`` returns. This step uses no callback, so the raw
    camera frames are displayed. Later ``main.py`` will pass a callback that
    detects faces, embeds them, matches them and draws the result, without any
    change to this loop.

    Arguments:
        camera_index {int} -- which camera to open. (default: {0})
        on_frame {Callable} -- optional function receiving a frame and
            returning the frame to display. (default: {None})
        exit_key {str} -- the key that ends the session. (default: {"q"})
        window_name {str} -- title of the display window.

    Returns:
        int -- the number of frames that were displayed, which is useful when
        checking that the camera really worked.

    Raises:
        ValueError -- for an invalid camera index or exit key.
        RuntimeError -- if the camera cannot be opened or stops delivering
            frames.

    The camera is released and the windows are destroyed before returning,
    whether the loop ended normally, on the exit key, or on an exception.
    """
    checked_exit_key = _check_exit_key(exit_key)

    with open_webcam(camera_index) as capture:
        print(
            f"Webcam {camera_index} opened. Press '{checked_exit_key}' to quit."
        )

        frame_count = 0
        while True:
            frame = read_frame(capture)
            if frame is None:
                raise RuntimeError(
                    "The webcam stopped delivering frames. "
                    "It may have been disconnected."
                )

            display_frame = frame if on_frame is None else on_frame(frame)
            show_frame(display_frame, window_name)
            frame_count += 1

            if is_exit_key_pressed(checked_exit_key):
                break

    print(f"Webcam released after {frame_count} frame(s).")
    return frame_count


def _demo() -> None:
    """Open the webcam, show the live frames and exit on the exit key.

    This is only a capture test: no face detection, no FaceNet inference and no
    matching happen here. The real pipeline is assembled in main.py.
    """
    try:
        run_webcam_loop()
    except (RuntimeError, ValueError) as error:
        print(f"The webcam test could not run: {error}")


if __name__ == "__main__":
    try:
        _demo()
    except KeyboardInterrupt:
        # Ctrl+C ends the session; the context manager still releases the
        # camera and closes the windows.
        print("\nInterrupted.")
