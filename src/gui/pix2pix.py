import tensorflow as tf
import numpy as np
import datetime

WIDTH = 512
HEIGHT = 512
INPUT_CHANNELS = 7
OUTPUT_CHANNELS = 3

class Pix2PixModelBuilder:
    def downsample(self, filters, size, apply_batchnorm=True):
        initializer = tf.random_normal_initializer(0., 0.02)

        result = tf.keras.Sequential()
        result.add(
            tf.keras.layers.Conv2D(filters, kernel_size=size, strides=2, padding='same',
                                    kernel_initializer=initializer, use_bias=False))
        
        if apply_batchnorm:
            result.add(tf.keras.layers.BatchNormalization())

        result.add(tf.keras.layers.LeakyReLU())

        return result
    
    def upsample(self, filters, size, apply_dropout=False):
        initializer = tf.random_normal_initializer(0., 0.02)

        result = tf.keras.Sequential()
        result.add(
            tf.keras.layers.Conv2DTranspose(filters, size, strides=2,
                                        padding='same',
                                        kernel_initializer=initializer,
                                        use_bias=False))

        result.add(tf.keras.layers.BatchNormalization())

        if apply_dropout:
            result.add(tf.keras.layers.Dropout(0.5))

        result.add(tf.keras.layers.ReLU())

        return result

    def BuildGenerator(self):
        inputs = tf.keras.layers.Input(shape=[WIDTH, HEIGHT, INPUT_CHANNELS])

        down_stack = [
            self.downsample(64, 4, apply_batchnorm=False),  # (batch_size, 256, 256, 64)
            self.downsample(128, 4),  # (batch_size, 128, 128, 128)
            self.downsample(256, 4),  # (batch_size, 64, 64, 256)
            self.downsample(512, 4),  # (batch_size, 32, 32, 512)
            self.downsample(512, 4),  # (batch_size, 16, 16, 512)
            self.downsample(512, 4),  # (batch_size, 8, 8, 512)
            self.downsample(512, 4),  # (batch_size, 4, 4, 512)
            self.downsample(512, 4),  # (batch_size, 2, 2, 512)
            self.downsample(512, 4),  # (batch_size, 1, 1, 512)
        ]   

        up_stack = [
            self.upsample(512, 4, apply_dropout=True),  # (batch_size, 2, 2, 1024)
            self.upsample(512, 4, apply_dropout=True),  # (batch_size, 4, 4, 1024)
            self.upsample(512, 4, apply_dropout=True),  # (batch_size, 8, 8, 1024)
            self.upsample(512, 4),  # (batch_size, 16, 16, 1024)
            self.upsample(512, 4),  # (batch_size, 32, 32, 1024)
            self.upsample(256, 4),  # (batch_size, 64, 64, 512)
            self.upsample(128, 4),  # (batch_size, 128, 128, 256)
            self.upsample(64, 4),  # (batch_size, 256, 256, 128)
        ]

        initializer = tf.random_normal_initializer(0., 0.02)
        last = tf.keras.layers.Conv2DTranspose(OUTPUT_CHANNELS, 4,
                                            strides=2,
                                            padding='same',
                                            kernel_initializer=initializer,
                                            activation='tanh')  # (batch_size, 512, 512, 3)

        x = inputs

        # Downsampling through the model
        skips = []
        for down in down_stack:
            x = down(x)
            skips.append(x)

        skips = reversed(skips[:-1])

        # Upsampling and establishing the skip connections
        for up, skip in zip(up_stack, skips):
            x = up(x)
            x = tf.keras.layers.Concatenate()([x, skip])

        x = last(x)

        return tf.keras.Model(inputs=inputs, outputs=x)

    def BuildDiscriminator(self):
        initializer = tf.random_normal_initializer(0., 0.02)

        inp = tf.keras.layers.Input(shape=[512, 512, 7], name='input_image')
        tar = tf.keras.layers.Input(shape=[512, 512, 3], name='target_image')

        x = tf.keras.layers.concatenate([inp, tar])  # (batch_size, 256, 256, channels*2)

        down1 = self.downsample(64, 4, False)(x)  # (batch_size, 256, 256, 64)
        down2 = self.downsample(128, 4)(down1)  # (batch_size, 128, 128, 128)
        down3 = self.downsample(256, 4)(down2)  # (batch_size, 64, 64, 256)
        down4 = self.downsample(512, 4)(down3)  # (batch_size, 32, 32, 512)

        zero_pad1 = tf.keras.layers.ZeroPadding2D()(down4)  # (batch_size, 34, 34, 512)
        conv = tf.keras.layers.Conv2D(512, 4, strides=1,
                                    kernel_initializer=initializer,
                                    use_bias=False)(zero_pad1)  # (batch_size, 31, 31, 512)

        batchnorm1 = tf.keras.layers.BatchNormalization()(conv)

        leaky_relu = tf.keras.layers.LeakyReLU()(batchnorm1)

        zero_pad2 = tf.keras.layers.ZeroPadding2D()(leaky_relu)  # (batch_size, 33, 33, 512)

        last = tf.keras.layers.Conv2D(1, 4, strides=1,
                                    kernel_initializer=initializer)(zero_pad2)  # (batch_size, 30, 30, 1)

        return tf.keras.Model(inputs=[inp, tar], outputs=last)

    def BuildCheckpoint(self, generator_optimizer, discriminator_optimizer, generator, discriminator):
        checkpoint = tf.train.Checkpoint(generator_optimizer=generator_optimizer,
                                        discriminator_optimizer=discriminator_optimizer,
                                        generator=generator,
                                        discriminator=discriminator)
        return checkpoint


class Pix2PixModel:
    def __init__(self, checkpointfile):
        builder = Pix2PixModelBuilder()

        self.generator = builder.BuildGenerator()
        self.discriminator = builder.BuildDiscriminator()

        self.generator_optimizer = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)
        self.discriminator_optimizer = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)

        self.checkpoint = builder.BuildCheckpoint(self.generator_optimizer, 
                                                    self.discriminator_optimizer,
                                                    self.generator,
                                                    self.discriminator)
        self.checkpoint.restore(checkpointfile)

    def GenerateImage(self, input):
        prediction = self.generator(input, training=True)

        return prediction


import os
path = os.path.dirname(__file__)

model = Pix2PixModel(path + '/../../checkpoints/ckpt-76')


def Generate(albedo, depth, normals):
    x = np.concatenate((albedo, depth, normals), axis=3)

    start_time = datetime.datetime.now()
    y = model.GenerateImage(x)
    end_time = datetime.datetime.now()

    time_diff = (end_time - start_time)
    print(time_diff.total_seconds() * 1000)

    return y