import os
from skimage.transform import resize
from skimage.io import imsave
import numpy as np
from data import load_train_data, load_test_data

class segmentation:
	
	def __init__():

		image_height, image_width = 96, 96
		smoothness = 1.0
		work_dir = ''

	def dice_coefficient(y1, y2):
		
		y1 = tf.flatten(y1)
		y2 = tf.flatten(y2)
		
		return (2. * tf.sum(y1 * y2) + smoothness) / (tf.sum(y1) + tf.sum(y2) + smoothness)
	
	def dice_coefficient_loss(y1, y2):
	
		return -dice_coefficient(y1, y2)

	def preprocess(imgs):

		imgs_p = np.ndarray((imgs.shape[0], image_height, image_width), dtype=np.uint8)
		
		for i in range(imgs.shape[0]):
			imgs_p[i] = resize(imgs[i], (image_width, image_height), preserve_range=True)
		
		imgs_p = imgs_p[..., np.newaxis]
		 	
		return imgs_p

	def covolution_layer(filters, kernel=(3,3), activation='relu', input_shape=None):
		
		if input_shape is None:
			return tf.keras.layers.Conv2D(filters=filters,kernel=kernel,activation=activation)
		else:
			return tf.keras.layers.Conv2D(filters=filters,kernel=kernel,activation=activation,input_shape=input_shape)
	
	def concatenated_de_convolution_layer(filters):
		
		return tf.keras.layers.concatenate([tf.keras.layers.Conv2DTranspose(filters=filters,kernel=(2, 2),strides=(2, 2),
		padding='same')],axis=3)

	def Network():

		unet = tf.keras.models.Sequential()
		inputs = tf.keras.layers.Input((image_height, image_width, 1))
		input_shape = (image_height, image_width, 1)
		unet.add(covolution_layer(32, input_shape=input_shape))
		unet.add(covolution_layer(32))
		unet.add(pooling_layer())
		unet.add(covolution_layer(64))
		unet.add(covolution_layer(64))
		unet.add(pooling_layer())
		unet.add(covolution_layer(128))
		unet.add(covolution_layer(128))
		unet.add(pooling_layer())
		unet.add(covolution_layer(256))
		unet.add(covolution_layer(256))
		unet.add(pooling_layer())
		unet.add(covolution_layer(512))
		unet.add(covolution_layer(512))

		unet.add(concatenated_de_convolution_layer(256))
		unet.add(covolution_layer(256))
		unet.add(covolution_layer(256))
		unet.add(concatenated_de_convolution_layer(128))
		unet.add(covolution_layer(128))
		unet.add(covolution_layer(128))
		unet.add(concatenated_de_convolution_layer(64))
		unet.add(covolution_layer(64))
		unet.add(covolution_layer(64))
		unet.add(concatenated_de_convolution_layer(32))
		unet.add(covolution_layer(32))
		unet.add(covolution_layer(32))
		unet.add(covolution_layer(1, kernel=(1, 1), activation='sigmoid'))
		unet.compile(optimizer=tf.keras.optimizers.Adam(lr=1e-5),loss=dice_coefficient_loss,metrics=[dice_coefficient])

		return unet 
