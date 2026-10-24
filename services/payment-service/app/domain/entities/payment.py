from uuid import UUID

from app.domain.entities.payment_status import PaymentStatus


class Payment:

    def __init__(
        self,
        payment_id: UUID,
        order_id: UUID,
        amount: float,
    ):
        if amount <= 0:
            raise ValueError("Payment amount must be greater than zero")

        self.payment_id = payment_id
        self.order_id = order_id
        self.amount = amount
        self.status = PaymentStatus.PENDING

    def succeed(self) -> None:
        if self.status != PaymentStatus.PENDING:
            raise ValueError(
                "Only a pending payment can succeed"
            )

        self.status = PaymentStatus.SUCCEEDED

    def fail(self) -> None:
        if self.status != PaymentStatus.PENDING:
            raise ValueError(
                "Only a pending payment can fail"
            )

        self.status = PaymentStatus.FAILED

    def refund(self) -> None:
        if self.status != PaymentStatus.SUCCEEDED:
            raise ValueError(
                "Only a successful payment can be refunded"
            )

        self.status = PaymentStatus.REFUNDED

    @classmethod
    def rehydrate(
        cls,
        payment_id: UUID,
        order_id: UUID,
        amount: float,
        status: PaymentStatus,
    ):
        payment = cls(
            payment_id=payment_id,
            order_id=order_id,
            amount=amount,
        )

        payment.status = status

        return payment