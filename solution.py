# 도서관 대출 시스템 — 아래 클래스를 완성하세요. (클래스·메서드 이름은 바꾸지 마세요)

BOOKS = ("B001", "B002", "B003", "B004", "B005")
LOAN_DAYS = 14
MAX_LOANS = 3


def _valid_day(day):
    # 1 이상의 정수만 인정 (True/False는 정수로 보지 않음)
    return type(day) is int and day >= 1


def _valid_book(book_id):
    return isinstance(book_id, str) and book_id in BOOKS


class LibraryLoan:
    def __init__(self):
        # book_id -> (name, 빌린 날, 반납 기한)
        self.loans = {}
        # (name, 정지 시작일, 정지 마지막 날) 목록
        self.suspensions = []

    def _is_suspended(self, name, day):
        for who, start, end in self.suspensions:
            if who == name and start <= day <= end:
                return True
        return False

    def borrow(self, book_id, name, day):
        # 1. 없는 책 번호
        if not _valid_book(book_id):
            return False
        # 2. day가 1 이상의 정수가 아님
        if not _valid_day(day):
            return False
        # 3. 이미 누군가 빌려 간 책
        if book_id in self.loans:
            return False
        my_loans = [info for info in self.loans.values() if info[0] == name]
        # 4. 이미 3권을 빌리고 있음
        if len(my_loans) >= MAX_LOANS:
            return False
        # 5. 반납 기한이 지난 책을 아직 갖고 있음
        for _, _, due in my_loans:
            if day > due:
                return False
        # 6. 대출 정지 기간
        if self._is_suspended(name, day):
            return False

        self.loans[book_id] = (name, day, day + LOAN_DAYS)
        return True

    def return_book(self, book_id, name, day):
        if not _valid_book(book_id):
            return -1
        if not _valid_day(day):
            return -1
        info = self.loans.get(book_id)
        # 그 사람이 그 책을 빌리고 있지 않음
        if info is None or info[0] != name:
            return -1
        _, borrowed_day, due = info
        # 빌린 날보다 이른 날 반납
        if day < borrowed_day:
            return -1

        overdue = day - due
        if overdue < 0:
            overdue = 0

        del self.loans[book_id]

        # 연체했으면 반납한 날부터 연체 일수만큼 대출 정지
        # (겹치면 합쳐져서 더 늦게 끝나는 쪽까지 정지, 기간을 더하지 않음)
        if overdue > 0:
            self.suspensions.append((name, day, day + overdue - 1))

        return overdue

    def get_loans(self, name):
        result = [(book_id, info[2]) for book_id, info in self.loans.items()
                  if info[0] == name]
        result.sort(key=lambda x: (x[1], x[0]))
        return result
