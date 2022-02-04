import logging
from typing import Optional

import numpy as np
import pydicom
from pydicom import dataset
from streamlit import uploaded_file_manager

logger = logging.getLogger(__name__)


class ScintigraphyImage:
    def __init__(self, file: uploaded_file_manager.UploadedFile) -> None:
        ima_image: dataset.FileDataset = pydicom.read_file(file)

        self._load_images(ima_image)
        self._load_size(ima_image)

    def _normalize_img(self, img: np.ndarray) -> np.ndarray:
        return img / img.max()

    def _load_images(self, ima_image: dataset.FileDataset) -> None:
        imgs = ima_image.pixel_array
        if len(imgs.shape) == 2:
            self.imgs = [imgs]
            self.imgs_num = 1
        elif len(imgs.shape) == 3:
            if imgs.shape[0] > imgs.shape[2]:
                self.imgs = [
                    self._normalize_img(np.squeeze(img))
                    for img in np.split(imgs, imgs.shape[2], axis=2)
                ]
                self.imgs_num = imgs.shape[2]
            else:
                self.imgs = [
                    self._normalize_img(np.squeeze(img))
                    for img in np.split(imgs, imgs.shape[0], axis=0)
                ]
                self.imgs_num = imgs.shape[0]
        else:
            raise ValueError(f'Image cannot be {len(imgs.shape)}-dimensional')

        logger.info(f'Loaded {self.imgs_num} images of size {self.imgs[0].shape}')

    def _load_size(self, ima_image: dataset.FileDataset) -> None:
        self.y_px_size, self.x_px_size = ima_image.PixelSpacing

        logger.info(f'Loaded size=({self.x_px_size},{self.y_px_size})')

    def get_image(
        self,
        num: int,
        invert: bool = False,
        threshold: Optional[float] = None,
    ) -> np.ndarray:
        img = self.imgs[num]
        if threshold is not None:
            img = (img > threshold).astype(float)
        if invert:
            img = 1.0 - img

        return img

    def get_area(self, num: int, threshold: float, precision: int = 2) -> float:
        pxs = (self.imgs[num] > threshold).sum()
        area = pxs * self.x_px_size * self.y_px_size

        return round(area / 100, precision)
