class solver:
    def __init__(self, correct_matrix: list[int], sqaure_height:int):
        self.correct_matrix = correct_matrix
        self.square_height = sqaure_height
        self.length = len(correct_matrix)
        self.all_nums = {i for i in range(1, self.length + 1)}
        self.all_rows_or_columns = {i for i in range(0, self.length)}
        self.all_squares = {(i, j) for i in range(0, int(self.length/sqaure_height)) for j in range(0, int(self.length/sqaure_height))}

    def find_element_coordinates(self, target: int) -> list[tuple[int, int]]:
        locations = []
        for row_i, row in enumerate(self.correct_matrix):
            try:
                col_i = row.index(target)
                locations.append((row_i, col_i))
            except:
                pass
        
        return locations

    def find_columns_missing(self, locations: list[tuple[int, int]]) -> list[int]:
        columns_with_ele = {ele[1] for ele in locations}
        return self.all_rows_or_columns ^ columns_with_ele


    def find_rows_missing(self, locations: list[tuple[int, int]]) -> list[int]:
        rows_with_ele = {ele[0] for ele in locations}
        return self.all_rows_or_columns ^ rows_with_ele

    def find_squares_missing(self, locations: list[tuple[int, int]]) -> list[tuple[int, int]]:
        squares_with_ele = {(int(ele[0] / self.square_height), int(ele[1] / self.square_height)) for ele in locations}
 
        return self.all_squares ^ squares_with_ele

    def find_appeared_once(self, potential_matrix) -> list[tuple[int, int, int]]: # (target, i, j)
        ans =[]
        
        potential_matrix_rotated = [[] for i in range(self.length)]

        for row_i, row in enumerate(potential_matrix):
            occurences_dict = {}
            targets = []

            for j, potentials in enumerate(row):
                potential_matrix_rotated[j].append(potentials)

                for num in potentials:
                    if num in occurences_dict:
                        occurences_dict[num] += 1
                    else:
                        occurences_dict[num] = 1

            # if only occured once
            for key in occurences_dict.keys():
                if occurences_dict[key] == 1:
                    targets.append(key)
            
            
            if targets == []: continue

            for col_i, potentials in enumerate(row):
                for num in potentials:
                    if num in targets and correct_matrix[row_i][col_i] == 0:
                        ans.append((num, row_i, col_i))


        for col_i, col in enumerate(potential_matrix_rotated):
            occurences_dict = {}
            targets = []

            for potentials in col:
                for num in potentials:
                    if num in occurences_dict:
                        occurences_dict[num] += 1
                    else:
                        occurences_dict[num] = 1

            # if only occured once
            for key in occurences_dict.keys():
                if occurences_dict[key] == 1:
                    targets.append(key)

            if targets == []: continue

            for row_i, potentials in enumerate(col):
                for num in potentials:
                    if num in targets and correct_matrix[row_i][col_i] == 0:
                        ans.append((num, row_i, col_i))

        return ans


    def print_correct_matrix(self):
        print("Correct Matrix:")
        for row in self.correct_matrix:
            for ele in row: 
                if ele != 0: print(ele, end=" ")
                else: print(".", end= " ")
            print()

    def print_potential_matrix(self, matrix): 
        print("Potentail Matrix:")
        for row in matrix:
            print("[", end = "")
            for ele in row: 
                ele = str(ele)
                print(f'{ele: <20}', end=", ")
            print("],", end = "")
            print()

    def is_solved(self) -> bool:
        for row in correct_matrix:
            try: 
                row.index(0)
                return False
            except:
                pass
        
        return True



    def solve(self):
        stop = 0

        while not self.is_solved() and stop != self.length * self.length:
            stop += 1
            print(f'iteration {stop}', end = "")
            self.print_correct_matrix()
            if stop == self.length * self.length:
                print("solver failed to solve the puzzle...")
                break

            potential_matrix = []
            for i, row in enumerate(correct_matrix):
                potential_matrix.append([])
                for ele in row:
                    if ele == 0:
                        potential_matrix[i].append([])
                    else:
                        potential_matrix[i].append([ele])

            for num in self.all_nums:
                locations = self.find_element_coordinates(num)
                rows_missing = self.find_rows_missing(locations)
                columns_missing = self.find_columns_missing(locations)
                squares_missing = self.find_squares_missing(locations)

                for row in rows_missing:
                    for col in columns_missing:
                        square = (int(row / self.square_height), int(col / self.square_height))
                        if square in squares_missing and correct_matrix[row][col] == 0:
                            potential_matrix[row][col].append(num)

            for i, row in enumerate(potential_matrix):
                for j, potentials in enumerate(row):
                    if len(potentials) == 1 and self.correct_matrix[i][j] == 0:
                        self.correct_matrix[i][j] = potentials[0]
                        print(f'added {potentials[0]}@ ({i}, {j}) ')


            targets = self.find_appeared_once(potential_matrix)
            for target in targets:
                i = target[1]
                j = target[2]
                self.correct_matrix[i][j] = target[0]
                print(f'added {target[0]}@ ({i}, {j}) ')          

        print(f'solved!!!')
        self.print_correct_matrix()  
        


correct_matrix = [[9, 0, 4, 6, 0, 0, 3, 0, 0],
                  [0, 0, 0, 0, 0, 0, 4, 6, 9],
                  [6, 0, 0, 5, 4, 0, 0, 0, 0],
                  [3, 7, 8, 0, 0, 5, 0, 0, 2],
                  [0, 0, 0, 7, 6, 3, 0, 1, 5],
                  [0, 6, 0, 0, 2, 8, 7, 0, 4],
                  [0, 3, 0, 1, 5, 7, 9, 0, 6],
                  [0, 4, 5, 3, 0, 0, 1, 2, 0],
                  [1, 0, 0, 0, 8, 0, 5, 0, 0]]


correct_matrix = [[3, 0, 5, 2, 0, 0, 8, 0, 0],
                  [8, 9, 1, 0, 0, 3, 2, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 9],
                  [1, 0, 2, 0, 0, 0, 0, 0, 0],
                  [0, 7, 9, 8, 0, 0, 1, 0, 2],
                  [0, 0, 0, 0, 0, 9, 0, 0, 0],
                  [0, 0, 0, 0, 5, 0, 4, 0, 7],
                  [0, 0, 7, 0, 3, 0, 9, 1, 5],
                  [2, 0, 0, 0, 1, 0, 0, 0, 3]]

potential_matrix = [[[2, 7, 9]           , [7, 9]              , [4]                 , [8]                 , [6]                 , [2, 5, 7]           , [1, 2, 5, 7]        , [3]                 , [2, 7]              , ],
[[2, 3, 6, 7]        , [3, 6, 7]           , [1]                 , [3, 5, 7]           , [2, 3, 5, 7]        , [2, 4, 5, 7]        , [2, 5, 7, 8]        , [9]                 , [2, 4, 7, 8]        , ],
[[8]                 , [3, 7]              , [2, 5]              , [1, 3, 5, 7]        , [1, 2, 3, 5, 7]     , [9]                 , [1, 2, 5, 7]        , [6]                 , [2, 4, 7]           , ],
[[5]                 , [4, 9]              , [3]                 , [2]                 , [7, 8, 9]           , [6]                 , [7, 8, 9]           , [4, 7, 8]           , [1]                 , ],
[[4, 6, 9]           , [2]                 , [7]                 , [5, 9]              , [5, 8, 9]           , [1]                 , [3, 5, 8, 9]        , [4, 5, 8]           , [3, 4, 8, 9]        , ],
[[1, 9]              , [1, 9]              , [8]                 , [5, 7, 9]           , [4]                 , [3]                 , [2, 5, 7, 9]        , [2, 5, 7]           , [6]                 , ],
[[1, 2, 3, 4, 6, 7]  , [5]                 , [2, 6]              , [1, 3, 6, 7, 9]     , [1, 2, 3, 7, 8, 9]  , [2, 7, 8]           , [2, 3, 6, 7, 8, 9]  , [2, 7, 8]           , [2, 3, 7, 8, 9]     , ],
[[1, 2, 3, 6, 7]     , [1, 3, 6, 7, 8]     , [9]                 , [1, 3, 5, 6, 7]     , [1, 2, 3, 5, 7, 8]  , [2, 5, 7, 8]        , [4]                 , [2, 7, 8]           , [2, 3, 7, 8]        , ],
[[2, 3, 6, 7]        , [3, 6, 7, 8]        , [2, 6]              , [4]                 , [2, 3, 7, 8, 9]     , [2, 7, 8]           , [2, 3, 6, 7, 8, 9]  , [1]                 , [5]                 , ],]

solve = solver(correct_matrix, 3)
solve.solve()



