import tkinter as tk
from tkinter import filedialog, messagebox


# ==========================================
# マップ設定
# ==========================================

MAP_WIDTH = 10
MAP_HEIGHT = 5

# 3 × 3 = 9面
MAP_COUNT_X = 3
MAP_COUNT_Y = 3
MAP_COUNT = MAP_COUNT_X * MAP_COUNT_Y


# ==========================================
# 数字ごとの文字色
# ==========================================

TEXT_COLORS = {
    0: "white",
    1: "blue",
    2: "red",
    3: "yellow",
    4: "yellow",
    5: "pink",
    6: "pink",
    7: "red"
}


# ==========================================
# 9面分のマップデータ
#
# map_data[MAP番号][Y][X]
# ==========================================

map_data = [
    [
        [0 for _ in range(MAP_WIDTH)]
        for _ in range(MAP_HEIGHT)
    ]
    for _ in range(MAP_COUNT)
]


# ==========================================
# 現在の状態
# ==========================================

# 現在選択している数字
current_value = 0

# 現在編集しているMAP
current_map = 0

# カーソル位置
cursor_x = 0
cursor_y = 0


# ==========================================
# 完成マップウィンドウ
# ==========================================

preview_window = None
preview_cells = []


# ==========================================
# ステータス表示
# ==========================================

def update_status():

    status_label.config(
        text=f"MAP{current_map + 1}　選択中: {current_value}"
    )


# ==========================================
# 数字を選択
# ==========================================

def select_value(value):

    global current_value

    current_value = value

    update_status()


# ==========================================
# 現在のMAPを画面に表示
# ==========================================

def draw_map():

    for y in range(MAP_HEIGHT):

        for x in range(MAP_WIDTH):

            value = map_data[current_map][y][x]

            buttons[y][x].config(
                text=str(value),
                fg=TEXT_COLORS[value]
            )

    update_cursor()
    update_status()

    # 完成マップが開いていれば更新
    update_preview()


# ==========================================
# マスに数字を配置
# ==========================================

def set_cell(x, y):

    map_data[current_map][y][x] = current_value

    draw_map()


# ==========================================
# カーソル移動
# ==========================================

def move_cursor(direction):

    global cursor_x
    global cursor_y

    if direction == "Left":

        cursor_x = max(
            0,
            cursor_x - 1
        )

    elif direction == "Right":

        cursor_x = min(
            MAP_WIDTH - 1,
            cursor_x + 1
        )

    elif direction == "Up":

        cursor_y = max(
            0,
            cursor_y - 1
        )

    elif direction == "Down":

        cursor_y = min(
            MAP_HEIGHT - 1,
            cursor_y + 1
        )

    update_cursor()


# ==========================================
# カーソル表示
# ==========================================

def update_cursor():

    for y in range(MAP_HEIGHT):

        for x in range(MAP_WIDTH):

            buttons[y][x].config(
                relief="raised"
            )

    buttons[cursor_y][cursor_x].config(
        relief="sunken"
    )


# ==========================================
# MAP切り替え
# ==========================================

def change_map(number):

    global current_map
    global cursor_x
    global cursor_y

    current_map = number

    cursor_x = 0
    cursor_y = 0

    draw_map()


# ==========================================
# 次のMAP
# ==========================================

def next_map():

    global current_map

    current_map += 1

    if current_map >= MAP_COUNT:
        current_map = 0

    change_map(current_map)


# ==========================================
# 前のMAP
# ==========================================

def previous_map():

    global current_map

    current_map -= 1

    if current_map < 0:
        current_map = MAP_COUNT - 1

    change_map(current_map)


# ==========================================
# キーボード操作
# ==========================================

def key_pressed(event):

    # 数字キー
    if event.keysym in "01234567":

        select_value(
            int(event.keysym)
        )

    # 矢印キー
    elif event.keysym in (
        "Left",
        "Right",
        "Up",
        "Down"
    ):

        move_cursor(
            event.keysym
        )

    # Enter
    elif event.keysym == "Return":

        set_cell(
            cursor_x,
            cursor_y
        )

    # Tab
    elif event.keysym == "Tab":

        next_map()

        return "break"

    # Shift + Tab
    elif event.keysym == "ISO_Left_Tab":

        previous_map()

        return "break"


# ==========================================
# 新規作成
# ==========================================

def clear_map():

    for map_number in range(MAP_COUNT):

        for y in range(MAP_HEIGHT):

            for x in range(MAP_WIDTH):

                map_data[map_number][y][x] = 0

    draw_map()

    status_label.config(
        text="9面すべてを新規作成しました"
    )


# ==========================================
# MAP保存
#
# 数字の間に半角スペースを入れる
#
# 例:
# 1 1 1 1 1 1 1 1 1 1
# ==========================================

def save_map():

    filename = filedialog.asksaveasfilename(
        title="マップを保存",
        defaultextension=".map",
        filetypes=[
            ("MAPファイル", "*.map"),
            ("すべてのファイル", "*.*")
        ]
    )

    if not filename:
        return

    try:

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as file:

            for map_number in range(MAP_COUNT):

                # 10 × 4
                for row in map_data[map_number]:

                    file.write(
                        " ".join(
                            str(v)
                            for v in row
                        )
                        + "\n"
                    )

                # MAPの間に空行
                file.write("\n")

        status_label.config(
            text=f"保存しました: {filename}"
        )

    except OSError as e:

        messagebox.showerror(
            "保存エラー",
            str(e)
        )


# ==========================================
# MAP読み込み
# ==========================================

def load_map():

    filename = filedialog.askopenfilename(
        title="マップを読み込み",
        filetypes=[
            ("MAPファイル", "*.map"),
            ("すべてのファイル", "*.*")
        ]
    )

    if not filename:
        return

    try:

        with open(
            filename,
            "r",
            encoding="utf-8"
        ) as file:

            lines = file.readlines()


        # ----------------------------------
        # 読み込み用変数
        # ----------------------------------

        current_file_map = 0
        row_number = 0

        map_rows = [
            0 for _ in range(MAP_COUNT)
        ]


        # ----------------------------------
        # 1行ずつ読む
        # ----------------------------------

        for line in lines:

            line = line.strip()


            # ----------------------------------
            # 空行
            # → 次のMAPへ
            # ----------------------------------

            if not line:

                if row_number > 0:

                    if row_number != MAP_HEIGHT:

                        raise ValueError(
                            f"MAP{current_file_map + 1}の高さが"
                            f"{MAP_HEIGHT}行ではありません。"
                        )

                    current_file_map += 1
                    row_number = 0

                continue


            # ----------------------------------
            # MAPが9個を超えていないか
            # ----------------------------------

            if current_file_map >= MAP_COUNT:

                raise ValueError(
                    "MAPが9個を超えています。"
                )


            # ----------------------------------
            # 5行を超えていないか
            # ----------------------------------

            if row_number >= MAP_HEIGHT:

                raise ValueError(
                    f"MAP{current_file_map + 1}の高さが"
                    f"{MAP_HEIGHT}行を超えています。"
                )


            # ----------------------------------
            # 半角スペースで分割
            # ----------------------------------

            values = line.split()


            # ----------------------------------
            # 10個あるか確認
            # ----------------------------------

            if len(values) != MAP_WIDTH:

                raise ValueError(
                    f"MAP{current_file_map + 1}の"
                    f"{row_number + 1}行目は"
                    f"{MAP_WIDTH}個の数字が必要です。"
                )


            # ----------------------------------
            # 数字を確認
            # ----------------------------------

            for x, value in enumerate(values):

                if value not in (
                    "0",
                    "1",
                    "2",
                    "3",
                    "4",
                    "5",
                    "6",
                    "7"
                ):

                    raise ValueError(
                        f"MAP{current_file_map + 1}の"
                        f"{row_number + 1}行目に"
                        f"0～7以外の数字があります。"
                    )


                map_data[
                    current_file_map
                ][
                    row_number
                ][x] = int(value)


            row_number += 1

            map_rows[
                current_file_map
            ] = row_number


        # ----------------------------------
        # 最後のMAPを確認
        # ----------------------------------

        if row_number > 0:

            if row_number != MAP_HEIGHT:

                raise ValueError(
                    f"MAP{current_file_map + 1}の高さが"
                    f"{MAP_HEIGHT}行ではありません。"
                )


        # ----------------------------------
        # 9面すべて確認
        # ----------------------------------

        for i in range(MAP_COUNT):

            if map_rows[i] != MAP_HEIGHT:

                raise ValueError(
                    f"MAP{i + 1}の高さが"
                    f"{MAP_HEIGHT}行ではありません。"
                )


        # ----------------------------------
        # 表示更新
        # ----------------------------------

        draw_map()

        status_label.config(
            text=f"読み込みました: {filename}"
        )


    except (OSError, ValueError) as e:

        messagebox.showerror(
            "読み込みエラー",
            str(e)
        )


# ==========================================
# 完成マップウィンドウを開く
# ==========================================

def open_preview():

    global preview_window
    global preview_cells


    # すでに開いている場合
    if (
        preview_window is not None
        and preview_window.winfo_exists()
    ):

        preview_window.lift()

        return


    # --------------------------------------
    # 別ウィンドウ作成
    # --------------------------------------

    preview_window = tk.Toplevel(root)

    preview_window.title(
        "完成マップ - 3×3"
    )

    preview_window.geometry(
        "700x600"
    )

    preview_window.configure(
        bg="#202020"
    )

    preview_window.resizable(
        False,
        False
    )


    # --------------------------------------
    # タイトル
    # --------------------------------------

    tk.Label(
        preview_window,
        text="完成マップ（3×3）",
        font=(
            "Yu Gothic UI",
            18,
            "bold"
        ),
        fg="white",
        bg="#202020"
    ).pack(
        pady=(10, 5)
    )


    # --------------------------------------
    # 全体フレーム
    # --------------------------------------

    preview_frame = tk.Frame(
        preview_window,
        bg="#101010",
        padx=5,
        pady=5
    )

    preview_frame.pack(
        pady=5
    )


    # 前回のデータを消す
    preview_cells = []


    # --------------------------------------
    # 9面を3×3で作成
    # --------------------------------------

    for map_number in range(MAP_COUNT):

        small_map_frame = tk.Frame(
            preview_frame,
            bg="#101010",
            bd=2,
            relief="solid"
        )

        small_map_frame.grid(
            row=map_number // 3,
            column=map_number % 3,
            padx=5,
            pady=5
        )


        # MAP番号
        tk.Label(
            small_map_frame,
            text=f"MAP{map_number + 1}",
            font=(
                "Consolas",
                10,
                "bold"
            ),
            fg="white",
            bg="#101010"
        ).grid(
            row=0,
            column=0,
            columnspan=MAP_WIDTH,
            pady=(3, 2)
        )


        map_cells = []


        # ----------------------------------
        # 10 × 4
        # ----------------------------------

        for y in range(MAP_HEIGHT):

            row_cells = []

            for x in range(MAP_WIDTH):

                value = map_data[
                    map_number
                ][
                    y
                ][
                    x
                ]


                cell = tk.Label(
                    small_map_frame,
                    text=str(value),
                    font=(
                        "Consolas",
                        9,
                        "bold"
                    ),
                    fg=TEXT_COLORS[value],
                    bg="#101010",
                    width=2,
                    height=1
                )

                cell.grid(
                    row=y + 1,
                    column=x,
                    padx=0,
                    pady=0
                )

                row_cells.append(cell)


            map_cells.append(row_cells)


        preview_cells.append(
            map_cells
        )


    # --------------------------------------
    # 閉じるボタン
    # --------------------------------------

    tk.Button(
        preview_window,
        text="閉じる",
        width=12,
        command=preview_window.destroy
    ).pack(
        pady=8
    )


    # 閉じたときの処理
    def on_close():

        global preview_window
        global preview_cells

        preview_cells = []

        preview_window.destroy()

        preview_window = None


    preview_window.protocol(
        "WM_DELETE_WINDOW",
        on_close
    )


    # 初期表示
    update_preview()


# ==========================================
# 完成マップ更新
# ==========================================

def update_preview():

    # ウィンドウが存在しない場合は何もしない
    if (
        preview_window is None
        or not preview_window.winfo_exists()
    ):

        return


    # プレビューがまだ作られていない場合
    if not preview_cells:

        return


    # 9面すべて更新
    for map_number in range(MAP_COUNT):

        for y in range(MAP_HEIGHT):

            for x in range(MAP_WIDTH):

                value = map_data[
                    map_number
                ][
                    y
                ][
                    x
                ]


                preview_cells[
                    map_number
                ][
                    y
                ][
                    x
                ].config(
                    text=str(value),
                    fg=TEXT_COLORS[value]
                )


# ==========================================
# メインウィンドウ
# ==========================================

root = tk.Tk()

root.title(
    "マップエディター"
)

root.geometry(
    "650x610"
)

root.configure(
    bg="#202020"
)

root.resizable(
    False,
    False
)

root.bind(
    "<Key>",
    key_pressed
)


# ==========================================
# タイトル
# ==========================================

tk.Label(
    root,
    text="マップエディター",
    font=(
        "Yu Gothic UI",
        20,
        "bold"
    ),
    fg="white",
    bg="#202020"
).pack(
    pady=(15, 5)
)


# ==========================================
# 説明
# ==========================================

tk.Label(
    root,
    text="数字キー 0～7 で数字を選択 → マスをクリック",
    font=(
        "Yu Gothic UI",
        10
    ),
    fg="#cccccc",
    bg="#202020"
).pack()


# ==========================================
# ステータス
# ==========================================

status_label = tk.Label(
    root,
    text="MAP1　選択中: 0",
    font=(
        "Yu Gothic UI",
        12,
        "bold"
    ),
    fg="white",
    bg="#202020"
)

status_label.pack(
    pady=5
)


# ==========================================
# 数字パレット
# ==========================================

palette_frame = tk.Frame(
    root,
    bg="#202020"
)

palette_frame.pack(
    pady=5
)


for value in range(8):

    tk.Button(
        palette_frame,
        text=str(value),
        width=4,
        font=(
            "Consolas",
            13,
            "bold"
        ),
        fg=TEXT_COLORS[value],
        bg="#303030",
        activebackground="#505050",
        command=lambda v=value:
            select_value(v)
    ).grid(
        row=0,
        column=value,
        padx=2
    )


# ==========================================
# 現在編集中のMAP
# ==========================================

tk.Label(
    root,
    text="現在編集中のMAP",
    font=(
        "Yu Gothic UI",
        11,
        "bold"
    ),
    fg="white",
    bg="#202020"
).pack(
    pady=(5, 2)
)


map_frame = tk.Frame(
    root,
    bg="#101010",
    padx=5,
    pady=5
)

map_frame.pack(
    pady=3
)


buttons = []


for y in range(MAP_HEIGHT):

    row = []

    for x in range(MAP_WIDTH):

        b = tk.Button(
            map_frame,
            text="0",
            width=3,
            height=1,
            font=(
                "Consolas",
                16,
                "bold"
            ),
            fg="white",
            bg="#101010",
            activebackground="#303030",
            relief="raised",
            bd=2,
            command=lambda xx=x, yy=y:
                set_cell(xx, yy)
        )

        b.grid(
            row=y,
            column=x,
            padx=1,
            pady=1
        )

        row.append(b)

    buttons.append(row)


# ==========================================
# MAP選択ボタン
# ==========================================

map_select_frame = tk.Frame(
    root,
    bg="#202020"
)

map_select_frame.pack(
    pady=4
)


for i in range(MAP_COUNT):

    tk.Button(
        map_select_frame,
        text=f"MAP{i + 1}",
        width=7,
        command=lambda n=i:
            change_map(n)
    ).grid(
        row=i // 3,
        column=i % 3,
        padx=3,
        pady=2
    )


# ==========================================
# 操作ボタン
# ==========================================

control_frame = tk.Frame(
    root,
    bg="#202020"
)

control_frame.pack(
    pady=5
)


tk.Button(
    control_frame,
    text="新規作成",
    width=12,
    command=clear_map
).grid(
    row=0,
    column=0,
    padx=5
)


tk.Button(
    control_frame,
    text="読み込み",
    width=12,
    command=load_map
).grid(
    row=0,
    column=1,
    padx=5
)


tk.Button(
    control_frame,
    text="保存",
    width=12,
    command=save_map
).grid(
    row=0,
    column=2,
    padx=5
)


# ==========================================
# 完成マップ表示ボタン
# ==========================================

tk.Button(
    root,
    text="完成マップを表示",
    width=20,
    font=(
        "Yu Gothic UI",
        10,
        "bold"
    ),
    command=open_preview
).pack(
    pady=5
)


# ==========================================
# 操作説明
# ==========================================

tk.Label(
    root,
    text="矢印キー: カーソル移動 / Enter: 配置 / 0～7: 数字選択",
    font=(
        "Yu Gothic UI",
        9
    ),
    fg="#aaaaaa",
    bg="#202020"
).pack(
    pady=(3, 0)
)


tk.Label(
    root,
    text="Tab: 次のMAP / Shift+Tab: 前のMAP",
    font=(
        "Yu Gothic UI",
        9
    ),
    fg="#aaaaaa",
    bg="#202020"
).pack(
    pady=2
)


# ==========================================
# 初期表示
# ==========================================

update_cursor()

update_status()


# ==========================================
# メインループ
# ==========================================

root.mainloop()