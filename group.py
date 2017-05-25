class UninitializedGroupClassError(Exception):
    pass


class Group(object):
    _b = None

    def __init__(self, i):
        self._cells_xy = self._get_cells_xy(i)
        if not self._b:
            raise UninitializedGroupClassError("Group.link_to_board() must be run before the class is instantiated.")

    @property
    def blanks(self):
        try:
            return set(self.cells_by_value['0'])
        except KeyError:
            return set()

    @property
    def pv(self):
        return {str(i) for i in range(1, 10)} - {v for v in self.cells.values()}

    @property
    def cells(self):
        return {cell_xy: self._b[cell_xy] for cell_xy in self._cells_xy}

    @property
    def cells_by_value(self):
        ret = {value: [] for value in self.cells.values()}
        for cell, value in self.cells.items():
            ret[value].append(cell)
        return ret

    @property
    def collisions(self):
        ret = set()
        for val, cells in self.cells_by_value.items():
            if len(cells) > 1 and val != '0':
                ret |= set(cells)
        return ret

    def _get_cells_xy(self, i):
        raise NotImplementedError

    @classmethod
    def link_to_board(cls, board):
        cls._b = board


class Row(Group):
    def _get_cells_xy(self, i):
        return [(x, i) for x in range(self._b.lensides)]


class Column(Group):
    def _get_cells_xy(self, i):
        return [(i, y) for y in range(self._b.lensides)]


class Square(Group):
    def _get_cells_xy(self, i):
        return [(x, y) for x in range((i % self._b.basenum) * 3, (i % self._b.basenum) * 3 + 3) for y in
                range((i // self._b.basenum) * 3, (i // self._b.basenum) * 3 + 3)]
