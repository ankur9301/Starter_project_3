"""
Name: Ankur Gyawali
Student ID: @03070757
"""


class Boggle:
    def __init__(self, grid, dictionary):
        """
        Initialize the Boggle game with the given grid and dictionary.
        """
        if not self._is_valid_grid(grid):
            self.board = []
            self.size = 0
        else:
            self.board = [[letter.upper() for letter in row] for row in grid]
            self.size = len(grid)

        self.word_dictionary = set(word.upper() for word in dictionary)
        self.valid_prefixes = self._generate_prefixes(self.word_dictionary)
        self.move_directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),          (0, 1),
            (1, -1),  (1, 0), (1, 1)
        ]

    def _is_valid_grid(self, grid):
        """
        Validate that the grid is properly formatted.
        """
        if not grid or not all(grid):
            return False
        row_lengths = {len(row) for row in grid}
        return len(row_lengths) == 1  # Ensure all rows have the same length

    def _generate_prefixes(self, word_set):
        """
        Create a set of all possible prefixes from the word dictionary.
        """
        prefixes = set()
        for word in word_set:
            for i in range(1, len(word)):
                prefixes.add(word[:i])
        return prefixes

    def _depth_first_search(self, row, col, visited, current_path):
        """
        Perform DFS starting from the specified cell to find valid words.
        """
        if row < 0 or row >= self.size:
            return
        if col < 0 or col >= len(self.board[row]):
            return
        if visited[row][col]:
            return

        letter = self.board[row][col]
        current_path.append(letter)
        additional_chars = 0

        # Handle special case for 'Q' representing 'QU'
        if letter == 'Q':
            current_path.append('U')
            additional_chars += 1

        # Handle special case for 'S'
        if letter == 'S':
            if len(current_path) >= 2 and current_path[-2] == 'Q':
                pass
            else:
                current_path.append('T')
                additional_chars += 1

        formed_word = ''.join(current_path)

        # Prune the search if the current word is not a valid prefix or word
        if (
            formed_word not in self.valid_prefixes and
            formed_word not in self.word_dictionary
        ):
            for _ in range(1 + additional_chars):
                if current_path:
                    current_path.pop()
            return

        # Add to found words if it's a valid word of sufficient length
        if len(formed_word) >= 3 and formed_word in self.word_dictionary:
            self.solutions.add(formed_word)

        visited[row][col] = True

        # Explore all adjacent cells
        for delta_row, delta_col in self.move_directions:
            new_row, new_col = row + delta_row, col + delta_col
            self._depth_first_search(new_row, new_col, visited, current_path)

        visited[row][col] = False

        # Backtrack the current path
        for _ in range(1 + additional_chars):
            if current_path:
                current_path.pop()

    def getSolution(self):
        """
        Find and return all valid words present on the Boggle board.
        """
        self.solutions = set()
        if self.size == 0:
            return []

        visited_cells = [[False for _ in row] for row in self.board]

        for row_index in range(self.size):
            for col_index in range(len(self.board[row_index])):
                self._depth_first_search(
                  row_index, col_index, visited_cells, []
                  )

        return sorted(self.solutions)


if __name__ == "__main__":
    main()


def main():
    grid = [
        ["T", "W", "Y", "R"],
        ["E", "N", "P", "H"],
        ["G", "Z", "Q", "R"],
        ["O", "N", "T", "A"]
    ]
    dictionary = [
        "art", "ego", "gent", "get", "net", "new", "newt", "prat",
        "pry", "qua", "quart", "quartz", "rat", "tar", "tarp",
        "ten", "went", "wet", "arty", "rhr", "not", "quar"
    ]

    mygame = Boggle(grid, dictionary)
    print(mygame.get_solution())


if __name__ == "__main__":
    main()
