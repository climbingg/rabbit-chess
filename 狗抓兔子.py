import random
import pickle


def print_point() -> None:
    print("參考代號:")
    print("    1    4    7")
    print("0   2    5    8   10")
    print("    3    6    9")
    print("---------------------")
    print("局面:")
    print("    ", table[point[1]], "    ", table[point[4]], "    ", table[point[7]], sep="")
    print(table[point[0]], "  ", table[point[2]], "    ", table[point[5]], "    ", table[point[8]], "   ", table[point[10]], sep="")
    print("    ", table[point[3]], "    ", table[point[6]], "    ", table[point[9]], sep="")
    print(f"{len(history) + 1}/30步")


def dfs() -> int:
    """深度優先搜索"""
    if (tuple(point), len(history)) in dic:
        return [max, min][len(history) % 2 == 0](dic[(tuple(point), len(history))])
    res = {}
    for move in gen_move():
        n = move_func(*move)
        if n != 0:
            if n in res:
                res[n].append(move)
            else:
                res[n] = [move]
        else:
            n = dfs()
            if n in res:
                res[n].append(move)
            else:
                res[n] = [move]
        undo()
    dic[(tuple(point), len(history))] = res
    return [max, min][len(history) % 2 == 0](res.keys())


def undo() -> None:
    """從history來undo"""
    before, after = history.pop()
    point[before] = point[after]
    point[after] = None


def gen_move() -> list[tuple[int, int]]:
    """生成合法走法清單"""
    ret = []
    if len(history) % 2 == 0:
        for i, val in enumerate(point):
            if val is None:
                continue
            if not val:
                for j in dog_point[i]:
                    if point[j] is None:
                        ret.append((i, j))
    else:
        for i, val in enumerate(point):
            if val is True:
                for j in rabbit_point[i]:
                    if point[j] is None:
                        ret.append((i, j))
                break
    return ret


def move_func(before: int, after: int) -> int:
    """移動並檢查勝負並新增history"""
    point[after] = point[before]
    point[before] = None
    history.append((before, after))
    if point[after] is True and after == 10:
        return 1
    if point[after] is True and len(gen_move()) == 0:
        return 1
    if point[after] is False and len(gen_move()) == 0:
        return -1
    return [0, 1][len(history) == 30]


table = {None: "〇", True: "兔", False: "狗"}
rabbit_point = (
    (1, 2, 3),
    (0, 2, 4, 5),
    (0, 1, 3, 5),
    (0, 2, 5, 6),
    (1, 5, 7),
    (1, 2, 3, 4, 6, 7, 8, 9),
    (3, 5, 9),
    (4, 5, 8, 10),
    (5, 7, 9, 10),
    (5, 6, 8, 10),
)
dog_point = (
    (),
    (0, 2),
    (0, 1, 3),
    (0, 2),
    (1, 5),
    (1, 2, 3, 4, 6),
    (3, 5),
    (4, 5, 8),
    (5, 7, 9),
    (5, 6, 8),
    (7, 8, 9),
)
move_point = [dog_point, rabbit_point]
point = [None] * 11
point[0] = True
point[7] = False
point[9] = False
point[10] = False
history = []
dic: dict[tuple, dict] = {}

dfs()

with open("data.pkl", "wb") as file:
    pickle.dump(dic, file)

def main() -> None:
    """主程式"""
    print("你先:")
    while True:
        print_point()
        moves = set([f"{move[0]}-{move[1]}" for move in gen_move()])
        if len(history) % 2 == 0:
            m = random.choice(min(dic[(tuple(point), len(history))].items(), key=lambda x: x[0])[1])
        else:
            m = input("輸入(要輸入原代號然後-後來代號):")
            while m not in moves:
                m = input("輸入有誤(要輸入原代號然後-後來代號):")
            m = tuple(map(int, m.split("-")))
        if move_func(*m):
            break
    print_point()
    print("game over!!!!")


main()
