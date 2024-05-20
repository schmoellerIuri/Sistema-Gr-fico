import numpy as np

class TransformationMatrixes:
    @staticmethod
    def translation_matrix(x, y):
        return np.array([[1, 0, x], [0, 1, y], [0, 0, 1]])
    @staticmethod
    def scale_matrix(x, y):
        return np.array([[x, 0, 0], [0, y, 0], [0, 0, 1]])
    @staticmethod
    def shear_matrix(x, y):
        return np.array([[1, x, 0], [y, 1, 0], [0, 0, 1]])
    @staticmethod
    def rotation_matrix(angle):
        return np.array([[np.cos(angle), -np.sin(angle), 0], [np.sin(angle), np.cos(angle), 0], [0, 0, 1]])
    @staticmethod
    def reflection_matrix(sense):
        return np.array([[-1, 0, 0], [0, 1, 0], [0, 0, 1]]) if sense == 'x' else np.array([[1, 0, 0], [0, -1, 0], [0, 0, 1]])
    @staticmethod
    def concatenate_operations(*operations):
        result = np.eye(3)
        for operation in operations:
            result = np.dot(operation, result)
        return result