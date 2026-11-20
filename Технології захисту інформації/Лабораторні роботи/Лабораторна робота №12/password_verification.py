"""Навчальна перевірка пароля з індивідуальною сіллю."""

from dataclasses import dataclass
from hashlib import pbkdf2_hmac
from hmac import compare_digest
from secrets import token_bytes


ITERATIONS = 600_000


@dataclass(frozen=True)
class PasswordRecord:
    salt: bytes
    iterations: int
    verifier: bytes


def derive(password: str, salt: bytes, iterations: int) -> bytes:
    return pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations, dklen=32)


def create_record(password: str) -> PasswordRecord:
    salt = token_bytes(16)
    return PasswordRecord(salt, ITERATIONS, derive(password, salt, ITERATIONS))


def verify(password: str, record: PasswordRecord) -> bool:
    candidate = derive(password, record.salt, record.iterations)
    return compare_digest(candidate, record.verifier)


def main() -> None:
    sample = "навчальний-зразок-12"
    alice = create_record(sample)
    bob = create_record(sample)
    positive = verify(sample, alice) and verify(sample, bob)
    negative = not verify("інший-навчальний-зразок", alice)
    salt_differs = alice.salt != bob.salt
    verifier_differs = not compare_digest(alice.verifier, bob.verifier)
    if not all((positive, negative, salt_differs, verifier_differs)):
        raise RuntimeError("Не виконано умови контрольного досліду.")

    print("ЛР №12. Один навчальний пароль, два записи")
    print(f"PBKDF2-HMAC-SHA256 | ітерацій: {ITERATIONS} | сіль: {len(alice.salt)} байтів")
    print(f"Сіль A: {alice.salt.hex()}")
    print(f"Сіль B: {bob.salt.hex()}")
    print(f"Верифікатор A: {alice.verifier.hex()}")
    print(f"Верифікатор B: {bob.verifier.hex()}")
    print("Різні солі → різні верифікатори: так")
    print("Правильний зразок збереженою сіллю: збіг у A та B")
    print("Змінений зразок для запису A: збігу немає")


if __name__ == "__main__":
    main()
