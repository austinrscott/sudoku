/* jshint esversion:11 */
/* jshint strict:false */

const BOARD_SIZE = 9;

/** @type {Array.<String>} */
const COMPLETE_SET = [...Array(9).keys()].map(i => (i + 1).toString());

const Cell = (row, column, value) => {
    if (value) {
        value = value.toString();

        if (!COMPLETE_SET.includes(value)) {
            value = null;
        }
    }

    const cell = {
        row,
        column,
        value,
        complete: value !== null
    };

    return {
        ...cell,
        update(value) {
            return Cell(row, column, value);
        }
    };
};

const Grouping = ([rows, columns], [originX, originY], board) => ({
    update() {
        // eslint-disable-next-line no-debugger
        debugger;
        this.cells = COMPLETE_SET.map(index => board.getCell({
            row: Math.floor(index / rows) + originY,
            column: (index % columns) + originX
        }));
    },
    cells: [],
    complete() {
        return this.cells.every(cell => cell.complete);
    },
    values() {
        return this.cells.filter(c => c.complete).map(c => c.value);
    },
    valid() {
        const values = this.values();
        return values.every(value => values.filter(v => v === value).length < 2);
    },
    invalidCells() {
        return this.cells.filter(c => this.values().filter(v => v === c.value).length > 1);
    },
    contains({row, column}) {
        return this.cells.find(c => c.row === row && c.column === column);
    }
});

const initData = () => Object.fromEntries([...Array(BOARD_SIZE ** 2).keys()].map(index => {
    const column = index % BOARD_SIZE;
    const row = Math.floor(index / BOARD_SIZE);
    return [`${row}-${column}`, Cell(row, column)];
}));

export default () => ({
    cells: initData(),
    clearCells() {
        this.cells = initData();
    },
    groups: [
        ...COMPLETE_SET.map(index => Grouping([1, BOARD_SIZE], [0, index], this)),
        ...COMPLETE_SET.map(index => Grouping([BOARD_SIZE, 1], [index, 0], this)),
        ...COMPLETE_SET.map(index => {
            const boardRoot = BOARD_SIZE ** 0.5;
            const row = (index / boardRoot) * boardRoot;
            const column = Math.floor(index % boardRoot) * boardRoot;
            return Grouping(Array(2).fill(BOARD_SIZE ** 0.5), [row, column], this);
        })
    ],
    updateCell({row, column, value}) {
        const key = `${row}-${column}`;
        const cell = this.cells[key].update(value);
        this.cells[key] = cell;
        this.updateGroups(cell);
        return this.cells[key];
    },
    getCell({row, column}) {
        return this.cells[`${row}-${column}`];
    },
    updateGroups(changedCell) {
        const targetGroups = [];
        if (changedCell) {
            targetGroups.push(...this.groups.filter(group => {
                group.contains(changedCell);
            }));
        } else {
            targetGroups.push(...this.groups);
        }
        targetGroups.map(group => group.update());
    },
    valid() {
        return this.groups.every(group => group.valid());
    },
    complete() {
        return this.groups.every(group => group.valid() && group.complete());
    },
    invalidCells() {
        return this.groups.every(group => group.invalidCells());
    }
});
