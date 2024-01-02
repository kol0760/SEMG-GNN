
import py3Dmol
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import plotly.graph_objects as go
import plotly.offline as pyo
from datetime import datetime



def draw_xyz(xyz_file_path):
    # 读取XYZ文件内容
    with open(xyz_file_path, 'r') as file:
        xyz_data = file.read()
    lines = xyz_data.split('\n')
    second_line = lines[1] if len(lines) > 1 else "File does not have a second line."
    # 创建一个3D视图对象
    view = py3Dmol.view(width=800, height=400)
    # 添加XYZ模型
    view.addLabel(second_line, {'position': {'x':4, 'y':4, 'z':4},'fontSize' :'25'})
    view.addModel(xyz_data, 'xyz')
    atom_count = int(lines[0])
    for i in range(atom_count):
    # Parse atom coordinates from lines
        atom_line = lines[i + 2].split()  # Atom lines start from the third line
        if len(atom_line) >= 4:
            try:
                x, y, z = map(float, atom_line[1:4])
                # Add label for each atom
                view.addLabel(str(i+1), {'position': {'x': x, 'y': y, 'z': z}, 'backgroundOpacity': '0', 'fontColor': 'darkred','inFront':'True'})
            except ValueError:
                # Handle parsing error
                print(f"Error parsing coordinates for atom {i+1}")

    # 设置分子的可视化样式
    view.setStyle({'stick': {}})
    view.zoomTo()
    return view.show()

def draw_fig_spms(total_spms,i):
    matrix = total_spms[i]
    # 创建图像
    plt.figure()
    ax = plt.gca()  # 获取当前轴
    cax = plt.imshow(matrix, cmap='RdBu', interpolation='bicubic')
    cbar = plt.colorbar(cax)  # 显示颜色条
    cbar.set_label('d(Å)')  # 为颜色条添加标签
    cbar.formatter.set_powerlimits((0, 0))  # 避免使用科学记数法
    cbar.update_ticks()  # 更新刻度以反映新的格式器设置
    # 设置colorbar的刻度格式为两位小数
    cbar.ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    # 设置横坐标到上面
    ax.xaxis.set_ticks_position('top')  # 将x轴的刻度设置到顶部
    ax.xaxis.set_label_position('top')  # 将x轴的标签设置到顶部
    # 设置横坐标标签为 0 到 2π，分成4段
    plt.xticks(ticks=np.linspace(0, matrix.shape[1]-1, num=5),
               labels=[f'0', f'$\\frac{{\\pi}}{{2}}$', f'$\\pi$', f'$\\frac{{3\\pi}}{{2}}$', f'$2\\pi$'])
    # 设置纵坐标标签为 0 到 π，分成2段
    plt.yticks(ticks=np.linspace(0, matrix.shape[0]-1, num=3),
               labels=[f'0', f'$\\frac{{\\pi}}{{2}}$', f'$\\pi$'])

    plt.xlabel('Theta (θ)')
    plt.ylabel('Phi (φ)')
    plt.title('atom '+str(i))
    plt.show()


def draw_fig_elec(total_elec, i, show_in_lab=1):

    data = total_elec[i]

    x, y, z = np.meshgrid(np.arange(data.shape[0]),
                          np.arange(data.shape[1]),
                          np.arange(data.shape[2]))
    # Volume trace
    fig = go.Figure(data=go.Volume(
        x=x.flatten(),
        y=y.flatten(),
        z=z.flatten(),
        value=data.flatten(),
        isomin=0.1,
        isomax=0.8,
        opacity=0.1,
        surface_count=15,
    ))

    fig.update_layout(
        width=500,
        height=500,
        margin=dict(l=0, r=0, b=0, t=0)
    )

    if show_in_lab == 0:
        name = datetime.now().strftime("%y_%m%d_%H%M")
        pyo.plot(fig, filename=name + "_" + str(i) + ".html")
    else:
        fig.show()




