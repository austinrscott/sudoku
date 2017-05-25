from unittest import TestCase, main

from board import Board, InvalidStringLengthError


def gen_test_string_3():
    string = ''
    nums = [str(x) for x in range(1, 10)]
    for i in range(9):
        string += ''.join(nums)
        offset = 3
        offset += 1 if i == 2 or i == 5 else 0
        nums = nums[-offset:] + nums[:-offset]
    return string


TEST_STRING_1 = '0' * 81
TEST_STRING_2 = '123' + '0' * 6 + '456' + '0' * 6 + '789' + '0' * 60
TEST_STRING_3 = gen_test_string_3()


class TestBoardInit(TestCase):
    def test_init_no_params(self):
        self.assertSequenceEqual(str(Board()), TEST_STRING_1)

    def test_init_test_string_2(self):
        self.assertSequenceEqual(str(Board(string=TEST_STRING_2)), TEST_STRING_2)


class TestBoardSet(TestCase):
    def setUp(self):
        self.b = Board()

    def test_set_string(self):
        self.b.string = TEST_STRING_2
        self.assertEqual(str(self.b), TEST_STRING_2)

    def test_set_too_large(self):
        with self.assertRaises(InvalidStringLengthError):
            self.b.string = '0' * 83

    def test_set_too_small(self):
        with self.assertRaises(InvalidStringLengthError):
            self.b.string = '0' * 79


class TestBoardGetting(TestCase):
    def setUp(self):
        self.b = Board(TEST_STRING_2)

    def test_index_1(self):
        self.assertEqual(self.b[1, 2], '8')

    def test_index_2(self):
        self.assertEqual(self.b[3, 2], '0')

    def test_bad_index_1(self):
        with self.assertRaises(IndexError):
            _ = self.b[-1, -1]

    def test_bad_index_2(self):
        with self.assertRaises(IndexError):
            _ = self.b[11, 10]


class TestBoardSetting(TestCase):
    def setUp(self):
        self.b = Board(TEST_STRING_2)

    def test_index_1(self):
        self.b[3, 3] = 1
        self.assertEqual(self.b[3, 3], '1')

    def test_index_2(self):
        self.b[8, 7] = '8'
        self.assertEqual(self.b[8, 7], '8')

    def test_bad_index_1(self):
        with self.assertRaises(IndexError):
            self.b[-2, -3] = 2

    def test_bad_index_2(self):
        with self.assertRaises(IndexError):
            self.b[31, 5] = 9


class TestBoardGetAllBlanks(TestCase):
    def setUp(self):
        self.b = Board(TEST_STRING_2)

    def test_get_all_blanks_1(self):
        self.assertEqual(len(self.b.blanks), 72)

    def test_get_all_blanks_2(self):
        self.b[3, 0] = 4
        self.assertEqual(len(self.b.blanks), 71)
        self.b[0, 1] = 0
        self.assertEqual(len(self.b.blanks), 72)

    def test_get_all_blanks_3(self):
        self.b.string = TEST_STRING_3
        self.assertEqual(len(self.b.blanks), 0)
        self.b[0, 0] = 0
        self.assertEqual(len(self.b.blanks), 1)


class TestBoardGetCellPV(TestCase):
    def setUp(self):
        self.b = Board(TEST_STRING_2)

    def test_get_cell_pv_1(self):
        self.b.string = TEST_STRING_3
        self.b[0, 0] = 0
        self.assertIn((0, 0), self.b.blanks.keys())

    def test_get_cell_pv_2(self):
        self.b.string = TEST_STRING_3
        self.b[0, 0] = 0
        self.assertEqual(self.b.blanks[(0, 0)], {'1'})

    def test_get_cell_pv_3(self):
        self.b.string = TEST_STRING_3
        self.b[0, 0] = 0
        self.b[1, 0] = 0
        self.b[1, 1] = 0
        self.assertEqual(self.b.blanks[(1, 0)], {'2'})


class TestBoardCollisions(TestCase):
    def setUp(self):
        self.b = Board(TEST_STRING_3)

    def test_get_all_collisions_1(self):
        self.b[0, 0] = 9
        self.assertSequenceEqual(self.b.collisions, {(0, 3), (8, 0), (2, 1), (0, 0)})

    def test_get_all_collisions_2(self):
        self.assertSequenceEqual(self.b.collisions, set())


if __name__ == "__main__":
    main()
