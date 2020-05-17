# coding: utf-8
"""
This is an example Calculator app which performs addition,
subtraction, multiplication and division. It will help me
demonstrate how to appropriately structure a Python project.
The coding style of the project is PEP8.
"""

__author__ = 'Jitesh Gosar'
__email__ = 'gosar95@gmail.com'
__license__ = 'MIT'
__date__ = 'Saturday, Feb 01, 2020'
__version__ = '1.0'

import os,sys
# sys.path.append(os.pardir)
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as im
from dataset.mnist import load_mnist


class Digits:
    def __init__(self, digits=12345, spacing_range=(5, 50), image_width=500, image_quantity=1, show_result=False):
        self.digits = digits
        self.spacing_range = spacing_range
        self.image_width = image_width
        self.image_quantity = image_quantity
        self.show_result = show_result
    
    def generate(self):
        """
        Generate an image that contains the sequence of given numbers, spaced
        randomly using an uniform distribution.
        """
        X, y = self.get_data()

        """ Initialise useful variables """
        label = np.asarray(y)
        (input_range_min, input_range_max) = self.spacing_range
        range_mean = (input_range_max + input_range_min) / 2
        input_sequence_length = len(str(abs(self.digits)))
        total_allowed_gap = self.image_width - 28 * input_sequence_length
        image_needed = self.image_quantity

        """ Mapping all images location to there respective digits """
        location_of_digit = np.array([None]*10)
        # ['list_0', 'list_1', 'list_2', 'list_3', 'list_4', 'list_5', 'list_6', 'list_7', 'list_8', 'list_9']
        for i in range(len(location_of_digit)):
            location_of_digit[i] = np.where(label == i)

        if image_needed == 1:
            """ Creating 1 image """
            gap = self.calculate_gap(input_sequence_length,
                                range_mean, total_allowed_gap)
            img = self.sequence_image(self.digits, gap, location_of_digit, X)
            im.imsave(str(self.digits) + '.png', img)
            return img
        elif image_needed > 1:
            """ Creating 'image_quantity' images """
            images = []
            for n in range(0, image_needed):
                gap = self.calculate_gap(input_sequence_length,
                                    range_mean, total_allowed_gap)
                img = self.sequence_image(
                    self.digits, gap, location_of_digit, X)
                im.imsave(str(self.digits) + '_' + str(n+1) + '.png', img)
                images.append(img)
                if self.show_result:
                    # To make grid of 'row' rows. (row = 5) is chosen randomly.
                    row = 5
                    plt.subplot(np.minimum(image_needed, row),
                                (image_needed - 1) / row + 1, n + 1)
                    plt.imshow(img)
            if self.show_result:
                plt.show()
            return images

    @staticmethod
    def get_data():
        """ Loading MNIST data through API """
            # (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
        (x_train, y_train), (x_test, y_test) = load_mnist(normalize=True, flatten=True, one_hot_label=False)
        return x_train, y_train


    def concat_images(self, left_image, right_image, gap):
        """ Combines two image side-by-side """
        h_left, w_left = left_image.shape
        h_right, w_right = right_image.shape
        space = int(gap)
        # Creating empty image
        max_height = 28
        total_width = w_left + w_right + space
        new_image = np.zeros(shape=(max_height, total_width))
        # Combining both the images
        new_image[:h_left, :w_left] = left_image
        new_image[:h_right, w_left + space: w_left + w_right + space] = right_image
        return new_image


    def concat_n_images(self, image_list, gap_list):
        """ Combines N images from a list of image paths """
        n_images = None
        for i, img in enumerate(image_list):
            if i == 0:
                n_images = img
            else:
                gap = gap_list[i - 1]  # Selecting gap between image[i-1] and image[i]
                n_images = self.concat_images(n_images, img, gap)
        return n_images

    def calculate_gap(self, input_sequence_length, range_mean, total_allowed_gap):
        """ Creating a list of gaps with random normal distribution """
        gap_float = np.random.normal(loc=range_mean, scale=range_mean * 0.1, size=input_sequence_length - 1)
        gap_float = total_allowed_gap * (gap_float / gap_float.sum())
        gap = np.round(gap_float)
        """ Making sure that size of the final image would be equal to desired size """
        while gap.sum() is not total_allowed_gap:
            if gap.sum() < total_allowed_gap:
                gap[np.random.randint(0, input_sequence_length - 1)] += 1
            elif gap.sum() > total_allowed_gap:
                gap[np.random.randint(0, input_sequence_length - 1)] -= 1
            else:
                break
        return gap


    def my_gen(self, list_n):
        """ Selects a random image for a given digit """
        while True:
            location = np.random.randint(len(list_n[0]))
            data = list_n[0][location]
            yield data


    def get_sequence_id(self, digit_sequence, location_of, X):
        """ Creates a sequence of randomly selected images for a given sequence of digits """
        seq = digit_sequence
        for i in range(len(digit_sequence)):
            digit = digit_sequence[i]
            gen_obj = self.my_gen(location_of[digit])
            next1 = next(gen_obj)
            seq[i] = X[next1].reshape((28, 28))
        return seq


    def sequence_image(self, input_sequence, gaps, location_of_digit, X):
        """ Creates an image of sequence of digits """
        digit_sequence = [int(i) for i in str(input_sequence)]
        images = self.get_sequence_id(digit_sequence, location_of_digit, X)
        final_image = self.concat_n_images(images, gaps)

        return final_image

