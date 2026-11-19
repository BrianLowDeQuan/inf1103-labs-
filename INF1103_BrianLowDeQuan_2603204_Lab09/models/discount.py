from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float) -> float:
        pass


class NoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float):
        if percentage < 0 or percentage > 100:
            raise ValueError("Discount percentage must be between 0 and 100.")
        self.percentage = percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.percentage / 100)


class BulkDiscount(DiscountStrategy):
    def __init__(self, threshold: float, amount: float):
        if threshold < 0 or amount < 0:
            raise ValueError("Threshold and discount amount cannot be negative.")
        self.threshold = threshold
        self.amount = amount

    def apply(self, total: float) -> float:
        return max(0.0, total - self.amount) if total >= self.threshold else total


class StudentDiscount(DiscountStrategy):
    def __init__(self, percentage: float = 5.0):
        if percentage < 0 or percentage > 100:
            raise ValueError("Student discount percentage must be between 0 and 100.")
        self.percentage = percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.percentage / 100)
