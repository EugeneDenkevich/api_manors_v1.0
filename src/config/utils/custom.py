from object import models

def feature_divided():
    FEATURES_CHOICES = models.FEATURES_CHOICES
    res = [
        ('Продвинутые удобства', FEATURES_CHOICES[:9]),
        ('Базовые удобства', FEATURES_CHOICES[9:15]),
        ('Дополнительно', FEATURES_CHOICES[15:]),
    ]
    return res
