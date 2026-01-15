import pandas as pd
import os

# Paths
csv_path = os.path.join(os.path.dirname(__file__), 'emoji_similarity.csv')
html_path = os.path.join(os.path.dirname(__file__), 'emoji_similarity.html')

# Image directories

# Relative paths for HTML (from output/emoji_similarity.html)
line_dir_rel = '../data/line/'
fluentui_dir_rel = '../data/fluentui/'
noto_dir_rel = '../data/noto/128/'

# Absolute paths for existence check
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
line_dir_abs = os.path.join(base_dir, 'data', 'line')
fluentui_dir_abs = os.path.join(base_dir, 'data', 'fluentui')
noto_dir_abs = os.path.join(base_dir, 'data', 'noto', '128')


def get_img_tag(abs_path, rel_path):
    if os.path.exists(abs_path):
        return f'<img src="{rel_path}" />'
    else:
        return '<span style="color:red">Not found</span>'

def main():
    df = pd.read_csv(csv_path)
    rows = []

    for _, row in df.iterrows():
        # Ensure all values are strings and handle NaN
        lp = str(row['line_product_id']) if pd.notna(row['line_product_id']) else ''
        le = str(row['line_emoji_id']) if pd.notna(row['line_emoji_id']) else ''
        fluent_vals = [str(row[c]) if pd.notna(row[c]) else '' for c in ['fluent1','fluent2','fluent3']]
        noto_vals = [str(row[c]) if pd.notna(row[c]) else '' for c in ['noto1','noto2','noto3']]


        # LINE: use only line_product_id if line_emoji_id is empty
        if le:
            line_filename = f"{lp}_{le}.png"
        else:
            line_filename = f"{lp}.png"
        line_abs = os.path.join(line_dir_abs, line_filename)
        line_rel = line_dir_rel + line_filename
        line_img = get_img_tag(line_abs, line_rel)

        # FluentUI: search for PNG in subfolder named after the emoji (before '__')
        fluent_imgs = []
        for f in fluent_vals:
            if f:
                # f is like 'Dango__dango_3d', folder is before '__', file is after '__' + '.png'
                if '__' in f:
                    folder, file = f.split('__', 1)
                    fluent_abs = os.path.join(fluentui_dir_abs, folder, file + '.png')
                    fluent_rel = fluentui_dir_rel + folder + '/' + file + '.png'
                else:
                    fluent_abs = os.path.join(fluentui_dir_abs, f + '.png')
                    fluent_rel = fluentui_dir_rel + f + '.png'
                fluent_imgs.append(get_img_tag(fluent_abs, fluent_rel))
            else:
                fluent_imgs.append('<span style="color:red">Not found</span>')

        # Noto
        noto_imgs = []
        for n in noto_vals:
            if n:
                noto_abs = os.path.join(noto_dir_abs, n + '.png')
                noto_rel = noto_dir_rel + n + '.png'
                noto_imgs.append(get_img_tag(noto_abs, noto_rel))
            else:
                noto_imgs.append('<span style="color:red">Not found</span>')

        rows.append(f'<tr><td>{line_img}</td>' + ''.join(f'<td>{img}</td>' for img in fluent_imgs + noto_imgs) + '</tr>')
    
    # Insert rows into HTML
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    html = html.replace('<!-- ROWS WILL BE INSERTED BY PYTHON SCRIPT -->', '\n'.join(rows))
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    main()
