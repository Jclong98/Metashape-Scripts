import pandas as pd
import pptk
import plyfile

def render(filepath):

    # read ply file as a dataframe
    data = plyfile.PlyData.read(filepath)['vertex']
    df = pd.DataFrame(
        data={
            'x':data['x'],
            'y':data['y'],
            'z':data['z'],
            'r':data['red'],
            'g':data['green'],
            'b':data['blue'],
            'nx':data['nx'],
            'ny':data['ny'],
            'nz':data['nz'],
        }
    )

    # # normalizing a scale for all axes
    # min_x = min(df['x'])
    # max_x = max(df['x'])
    # x_range = max_x - min_x

    # min_y = min(df['y'])
    # max_y = max(df['y'])
    # y_range = max_y - min_y

    # min_z = min(df['z'])
    # max_z = max(df['z'])
    # z_range = max_z - min_z

    # # 100 was chosen for ease of choosing epsilon
    # scale = (1/max(x_range, y_range, z_range))*1000

    # df['x'] = df['x'] * scale
    # df['y'] = df['y'] * scale
    # df['z'] = df['z'] * scale

    # # setting the minimum value for all axes to 0 
    # df['x'] = df['x'] + abs(min(df['x']))
    # df['y'] = df['y'] + abs(min(df['y']))
    # df['z'] = df['z'] + abs(min(df['z']))

    v = pptk.viewer(
        df[['x', 'y', 'z']], 
    )

    v.attributes(
        df[['r', 'g', 'b']] / 255, 
    )

    v.set(point_size=0.001)

if __name__ == "__main__":
    
    import sys

    render(sys.argv[1])