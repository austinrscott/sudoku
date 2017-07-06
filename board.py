from group import Group, Row, Column, Square


class InvalidStringLengthError(Exception):
    pass


class Board(object):
    _basenum = 3
    _lensides = 9
    _numcells = 81

    def __init__(self, string=('0' * _numcells)):
        self._cells = []
        self.string = string
        Group.link_to_board(self)

        self.rows, self.columns, self.squares = [], [], []
        for i in range(self._lensides):
            self.rows.append(Row(i))
            self.squares.append(Square(i))
            self.columns.append(Column(i))

    @property
    def basenum(self):
        return self._basenum

    @property
    def lensides(self):
        return self._lensides

    @property
    def string(self):
        return ''.join(self._cells)

    @string.setter
    def string(self, value):
        if not len(value) == self._numcells:
            raise InvalidStringLengthError
        self._cells = list(value)

    @property
    def complete(self):
        return not self.blanks and not self.collisions

    @property
    def legal(self):
        return not self.collisions and self.lowest_pv >= 1

    @property
    def cells(self):
        return self._cells

    @property
    def blanks(self):
        blank_xys = set()
        for row in self.rows:
            blank_xys |= row.blanks
        return {xy: self.pv_at_xy(xy) for xy in blank_xys}

    @property
    def blanks_by_pv(self):
        result = {}
        for xy, pv in self.blanks.items():
            if not len(pv) in result.keys():
                result[len(pv)] = [(xy, pv)]
            else:
                result[len(pv)].append((xy, pv))
        result = [[(xy, pv) for xy, pv in result[num_pv]] for num_pv in sorted(result.keys())]
        return result

    @property
    def all_legal_moves(self):
        return [(xy, value) for xy, pv in self.blanks.items() for value in pv]

    @property
    def lowest_pv(self):
        return min(map(len, self.blanks.values()))

    @property
    def xy_of_lowest_pv(self):
        return min(self.blanks.items(), key=lambda x: len(x[1]))

    def pv_at_xy(self, xy):
        column, row, square = self.groups_at_xy(xy)
        return column.pv & row.pv & square.pv

    def groups_at_xy(self, xy):
        x, y = xy
        ri, ci = y, x
        sqi = self.square_at_xy(xy)
        return self.columns[ci], self.rows[ri], self.squares[sqi]

    @staticmethod
    def square_at_xy(xy):
        x, y = xy
        return (y // 3) * 3 + (x // 3)

    @property
    def collisions(self):
        ret = set()
        for group in self.groups:
            ret |= group.collisions
        return ret

    @property
    def groups(self):
        return self.columns + self.rows + self.squares

    @classmethod
    def xy_in_range(cls, xy):
        x, y = xy
        return 0 <= x <= cls._lensides - 1 and 0 <= y <= cls._lensides - 1

    @classmethod
    def xy_to_idx(cls, xy):
        x, y = xy
        return x % cls._lensides + y * cls._lensides

    @classmethod
    def idx_in_range(cls, idx):
        return 0 <= idx <= cls._numcells - 1

    @classmethod
    def idx_to_xy(cls, idx):
        return idx % cls._lensides, (idx // cls._lensides)

    def __str__(self):
        return self.string

    def __getitem__(self, xy):
        if not self.xy_in_range(xy):
            raise IndexError("Coordinates {} not in range.".format(xy))
        return self.string[self.xy_to_idx(xy)]

    def __setitem__(self, xy, value):
        if not self.xy_in_range(xy):
            raise IndexError("Coordinates {} not in range.".format(xy))
        value = str(value)
        assert len(value) == 1
        self.cells[self.xy_to_idx(xy)] = value

    def __repr__(self):
        return "{} by {} Sudoku Board ({} blank, {})".format(self._lensides, self._lensides, self.blanks,
                                                             "valid" if self.collisions else "invalid")
