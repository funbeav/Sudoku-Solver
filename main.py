import time


def listOutput(sheet, text=''):
    print(text)
    for i in range(9):
        for j in range(9):
            if isinstance(sheet[i][j], list):
                print("'" + ''.join(map(str, sheet[i][j])), end='\t')
            else:
                print(sheet[i][j], end='\t')
        print()


def reBuildList(sheet):
    for i in range(9):
        for j in range(9):
            if sheet[i][j] == 0:
                sheet[i][j] = [1, 2, 3, 4, 5, 6, 7, 8, 9]


def removeFromList(target_list, elements):
    result_list = list(target_list)
    for element in elements:
        if isinstance(element, int) and element in result_list:
            result_list.remove(element)
    if len(result_list) == 1:
        result_list = result_list[0]
    return result_list


def getUniqElement(target_list, elements):
    remove_try = removeFromList(target_list, elements)
    if isinstance(remove_try, int):
        return remove_try
    else:
        return target_list


def isEqualLists(list1, list2):
    for i in range(9):
        for j in range(9):
            if list1[i][j] != list2[i][j]:
                return False
    return True


def isContentsMistakes(sheet):
    # rows
    for i in range(9):
        row_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        exist_elements = []
        for j in range(9):
            if isinstance(sheet[i][j], int):
                if sheet[i][j] in row_list:
                    row_list.remove(sheet[i][j])
                if sheet[i][j] in exist_elements:
                    return True
                else:
                    exist_elements.append(sheet[i][j])
            else:
                for element in sheet[i][j]:
                    if element in row_list:
                        row_list.remove(element)
        if row_list:
            return True
    # columns
    for j in range(9):
        col_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        exist_elements = []
        for i in range(9):
            if isinstance(sheet[i][j], int):
                if sheet[i][j] in col_list:
                    col_list.remove(sheet[i][j])
                if sheet[i][j] in exist_elements:
                    return True
                else:
                    exist_elements.append(sheet[i][j])
            else:
                for element in sheet[i][j]:
                    if element in col_list:
                        col_list.remove(element)
        if col_list:
            return True
    # clusters
    if clusterMistakeCheck(sheet, 0, 3, 0, 3) or clusterMistakeCheck(sheet, 0, 3, 3, 6) or clusterMistakeCheck(sheet, 0, 3, 6, 9) or \
            clusterMistakeCheck(sheet, 3, 6, 0, 3) or clusterMistakeCheck(sheet, 3, 6, 3, 6) or clusterMistakeCheck(sheet, 3, 6, 6, 9) or \
            clusterMistakeCheck(sheet, 6, 9, 0, 3) or clusterMistakeCheck(sheet, 6, 9, 3, 6) or clusterMistakeCheck(sheet, 6, 9, 6, 9):
        return True
    return False


def clusterMistakeCheck(sheet, x1, x2, y1, y2):
    cluster_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    exist_elements = []
    for i in range(x1, x2):
        for j in range(y1, y2):
            if isinstance(sheet[i][j], int):
                if sheet[i][j] in cluster_list:
                    cluster_list.remove(sheet[i][j])
                if sheet[i][j] in exist_elements:
                    return True
                else:
                    exist_elements.append(sheet[i][j])
            else:
                for element in sheet[i][j]:
                    if element in cluster_list:
                        cluster_list.remove(element)
    if cluster_list:
        return True
    return False


def simpleExclude(x, y, sheet):
    result = sheet[x][y]
    # row
    result = removeFromList(result, sheet[x])
    if isinstance(result, int):
        return result
    # column
    column_elements = []
    for i2 in range(9):
        column_elements.append(sheet[i2][y])
    result = removeFromList(result, column_elements)
    if isinstance(result, int):
        return result
    # cluster
    cluster_elements = []
    x1, y1 = x // 3 * 3, y // 3 * 3
    for i3 in range(x1, x1 + 3):
        for j3 in range(y1, y1 + 3):
            cluster_elements.append(sheet[i3][j3])
    result = removeFromList(result, cluster_elements)
    if isinstance(result, int):
        return result
    return result


def difficultExclude(x, y, sheet):
    result = sheet[x][y]
    # row
    row_elements = set()
    for j1 in range(9):
        if isinstance(sheet[x][j1], list) and j1 != y:
            for element in sheet[x][j1]:
                row_elements.add(element)
    result = getUniqElement(result, list(row_elements))
    if isinstance(result, int):
        return result
    # column
    column_elements = set()
    for i1 in range(9):
        if isinstance(sheet[i1][y], list) and i1 != x:
            for element in sheet[i1][y]:
                column_elements.add(element)
    result = getUniqElement(result, list(column_elements))
    if isinstance(result, int):
        return result
    # cluster
    cluster_elements = set()
    x1, y1 = x // 3 * 3, y // 3 * 3
    for i3 in range(x1, x1 + 3):
        for j3 in range(y1, y1 + 3):
            if isinstance(sheet[i3][j3], list) and (i3 != x or j3 != y):
                for element in sheet[i3][j3]:
                    cluster_elements.add(element)
    result = getUniqElement(result, list(cluster_elements))
    if isinstance(result, int):
        return result
    return result


def isIntegerList(sheet):
    for i in range(9):
        for j in range(9):
            if not isinstance(sheet[i][j], int):
                return False
    return True


def findSolution(sheet):
    same_lists = False
    while not same_lists:
        prev_sheet = [x[:] for x in sheet]
        for i in range(9):
            for j in range(9):
                if isinstance(sheet[i][j], list):
                    sheet[i][j] = simpleExclude(i, j, sheet)
                    if not sheet[i][j]:
                        if _debug: print("Empty list")
                        return False, []
                    if isinstance(sheet[i][j], list):
                        sheet[i][j] = difficultExclude(i, j, sheet)
                        if not sheet[i][j]:
                            if _debug: print("Empty list")
                            return False, []
        same_lists = isEqualLists(prev_sheet, sheet)
    if _debug: listOutput(sheet, "Sheet")

    if isIntegerList(sheet):
        if not isContentsMistakes(sheet):
            if _debug: print("Correct")
            return True, sheet
        else:
            if _debug: print("Wrong solution")
            return False, []
    else:
        if isContentsMistakes(sheet):
            if _debug: print("Contents Mistakes")
            return False, []
        # get new sheet
        for i in range(9):
            for j in range(9):
                if isinstance(sheet[i][j], list):
                    for digit in sheet[i][j]:
                        new_sheet = [x[:] for x in sheet]
                        new_sheet[i][j] = digit
                        if _debug: print("sheet[{}][{}]({}) -> {}".format(i, j, sheet[i][j], digit))
                        rec_res, rec_sheet = findSolution(new_sheet)
                        if rec_res:
                            return True, rec_sheet
                    if _debug: print("Every digit doesn't match Solution")
                    return False, []
        return False, []


def Run(sheet):
    if _debug: listOutput(sheet, "Source:")
    reBuildList(sheet)
    success, new_sheet = findSolution(sheet)
    if success:
        if _debug: listOutput(new_sheet, "\nResult:")
        return True, new_sheet
    else:
        if _debug: print("\nNo Solution :(")
        return False, sheet

# empty
'''
main_sheet = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]
'''
# World's Hardest Sudoku

main_sheet = [
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 6, 0, 0, 0, 0, 0],
    [0, 7, 0, 0, 9, 0, 2, 0, 0],
    [0, 5, 0, 0, 0, 7, 0, 0, 0],
    [0, 0, 0, 0, 4, 5, 7, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 3, 0],
    [0, 0, 1, 0, 0, 0, 0, 6, 8],
    [0, 0, 8, 5, 0, 0, 0, 1, 0],
    [0, 9, 0, 0, 0, 0, 4, 0, 0]
]

_debug = False

if _debug:
    start_time = time.time()
    Run(main_sheet)
    print("--- %s seconds ---" % (time.time() - start_time))