from munch import Munch
from pix2tex.cli import LatexOCR
import os


"""
Module for processing latex formula photos.
"""


args = Munch({'config': 'settings/config.yaml', 'checkpoint': os.path.abspath('weights/weights.pth'), 'no_cuda': True, 'no_resize': False})
model = LatexOCR(args)


def get_latex(img):
    """
    Convert a photo of a latex formula into a string.

    :param img: PIL.Image image object
    :return: String latex formula
    """

    return model(img)
