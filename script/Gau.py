import pandas as pd
import re

def get_NPAdata_from_log(path: str) -> pd.DataFrame:
    with open(path, 'r') as file:
        content = file.read()

    elements = ["H", "C", "N", "O", "F", "Cl", "Br", "S"]  # 等等，这里只是一个简化的列表
    
    # 使用 '|'.join(elements) 创建一个正则表达式模式，匹配任何列表中的元素
    coordinate_pattern = r" (" + '|'.join(elements) + r")\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)"
    coordinate_matches = re.findall(coordinate_pattern, content)
    ## coordinate_matches是匹配好的坐标，但是格式我不是很喜欢，因此转换了一下格式
    coordinate_result = [[element[0], tuple(map(float, element[1:]))] for element in coordinate_matches]
    coordinate_result.insert(0,["atom",("x","y","z")])
    
    NPA_pattern = r"Atom\s+No\s+Charge\s+Core\s+Valence\s+Rydberg\s+Total.*?={65,}"
    NPA_matches = re.search(NPA_pattern, content,re.DOTALL)
    # 对匹配到的数据进行清洗
    lines = NPA_matches.group(0).splitlines()
    # 删除第一行、第二行和最后一行
    del lines[0:2]
    del lines[-1]
    # 重新组合为一个字符串
    NPA_str = '\n'.join(lines)
    
    lines = NPA_str.splitlines()
    array = []
    
    for line in lines:
        parts = line.split()
        element = parts[0]
        #print(parts[1:])
        numbers = [float(num) for num in parts[1:]]
        array.append([element] + numbers)
    NAP_result = [row[2:] for row in array]
    NAP_result.insert(0,["Natural_Charge","Pop_Core","Pop_Valence","Pop_Rydberg","Pop_Total"])
    
    total_result = [row1 + row2 for row1, row2  in zip(coordinate_result, NAP_result)]
    
    df = pd.DataFrame(total_result[1:], columns=total_result[0])
    df = df.rename(index=lambda x: x + 1)
    
    return df

def get_NOABdata_from_log(path: str) -> pd.DataFrame:
    with open(path, 'r') as file:
        content = file.read()
    Spin_pattern = r"Atomic\-Atomic\s+Spin\s+Densities\..*?Sum\s+of"
    Spin_matches = re.search(Spin_pattern, content,re.DOTALL)
    # 对匹配到的数据进行清洗
    lines = Spin_matches.group(0).splitlines()
    # 删除第一行、第二行和最后一行
    del lines[0:3]
    del lines[-1]
    # 重新组合为一个字符串
    Spin_str = '\n'.join(lines)
    
    lines = Spin_str.splitlines()
    Spin_result = [["atom","Mulliken_charges","spin_densities"]]
    for line in lines:
        Spin_result.append(line.split()[1:])
    df = pd.DataFrame(Spin_result[1:], columns=Spin_result[0])
    df = df.rename(index=lambda x: x + 1)
    return df

def get_coordinates_from_Gaulog(path: str) -> pd.DataFrame:
    atomicnum2elemnt = {1: 'H', 6: 'C', 7: 'N', 8: 'O', 9: 'F', 17: 'Cl', 35: 'Br', 16: 'S'}
    with open(path, 'r') as fr:
        lines = fr.readlines()
    coord_start_index_list = []

    for i, line in enumerate(lines):
        if 'NAtoms=' in line:
            atom_num = eval(line.split()[1])
        if 'Standard orientation' in line:
            coord_start_index_list.append(i + 5)
        if 'Input orientation' in line:
            coord_start_index_list.append(i + 5)
    coord_string = lines[coord_start_index_list[-1]:coord_start_index_list[-1] + atom_num]
    coord = [[eval(item.strip().split()[3]), eval(item.strip().split()[4]), eval(item.strip().split()[5])] for item in
             coord_string]
    atom_type = [atomicnum2elemnt[eval(item.split()[1])] for item in coord_string]
    Coord = ''
    for tmp_coord, tmp_atom in zip(coord, atom_type):
        Coord += '%2s %15f %15f %15f\n' % (tmp_atom, tmp_coord[0], tmp_coord[1], tmp_coord[2])

    lines = Coord.splitlines()
    # 分割每一行并转换数据类型
    data = []
    for line in lines:
        parts = line.split()
        element = parts[0]
        coords = [float(x) for x in parts[1:]]
        data.append([element] + coords)
    coordinate_result = pd.DataFrame(data, columns=['atom', 'x', 'y', 'z'])
    coordinate_result = coordinate_result.rename(index=lambda x: x + 1)
    return coordinate_result

def get_coordinates_from_xyz(path: str) -> pd.DataFrame:
    with open(path, 'r') as file:
        content = file.read()
    elements = ["H", "C", "N", "O", "F", "Cl", "Br", "S"]  # 等等，这里只是一个简化的列表
    # 使用 '|'.join(elements) 创建一个正则表达式模式，匹配任何列表中的元素
    coordinate_pattern = r"(" + '|'.join(elements) + r")\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)"
    coordinate_matches = re.findall(coordinate_pattern, content)
    ## coordinate_matches是匹配好的坐标，但是格式我不是很喜欢，因此转换了一下格式
    df = pd.DataFrame(coordinate_matches, columns=['atom', 'x', 'y', 'z'])
    df = df.rename(index=lambda x: x + 1)
    df = df.astype({
        'atom': 'str',
        'x': 'float',
        'y': 'float',
        'z': 'float'
    })
    return df