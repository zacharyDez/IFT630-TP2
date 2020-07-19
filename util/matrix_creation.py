from numbers import Real


def create_unique_value_matrix(path: str, num_rows: int, num_cols: int, val: Real) -> None:
    with open(path, "w+") as f:
        for i in range(0, num_rows):
            f.write(" ".join([str(val) for j in range(0, num_cols)]))
            # python handles translation proper newline symbol, see:
            # https://stackoverflow.com/questions/11497376/how-do-i-specify-new-lines-on-python-when-writing-on-files/11497391
            f.write("\n")
        f.close()
