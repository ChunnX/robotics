import numpy as np


class Robot:
    def __init__(self, bp):
        self.bp = bp
        self.D = 0.04782
        self.W = 14.36
        self.encoder = np.zeros(2, dtype=np.int32)
    
    def move(self, distance, speed=5, finish_delay=0):
        self.clear_encoder()
        degree = distance / self.D
        self.encoder[0] += np.int32(degree + int(np.random.normal(0, 5)))
        self.encoder[1] += np.int32(degree + int(np.random.normal(0, 5)))
        return np.mean(self.encoder) * self.D
    
    def rotate(self, angle, angular_speed=30, finish_delay=0):
        self.clear_encoder()
        degree = angle * self.W / (114.591*self.D)
        self.encoder[0] += np.int32(-degree + int(np.random.normal(0, 5)))
        self.encoder[1] += np.int32(degree + int(np.random.normal(0, 5)))
        left_encoder, right_encoder = self.encoder
        return (right_encoder - left_encoder) * self.D / self.W * 57.296

    
    def stop(self, wait=0.02):
        pass


    def clear_encoder(self):
        self.encoder -= self.encoder

    def shutdown(self):
        pass

