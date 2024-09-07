import tkinter as tk

def get_screen_resolution(): # 解像度を取得
    root = tk.Tk()
    root.withdraw()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.destroy()
    return (width, height)


def get_screen_dpi(): # DPIを取得
    root = tk.Tk()
    root.withdraw()  # ウィンドウを非表示にする
    dpi = root.winfo_fpixels('1i')
    root.destroy()
    return dpi


def get_screen_width_cm(): # 画面の幅(単位：cm)を取得
    root = tk.Tk()
    root.withdraw()
    width_pix = root.winfo_screenwidth()
    dpi = get_screen_dpi()
    root.destroy()
    return width_pix / dpi * 2.54