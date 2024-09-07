from psychopy import visual, monitors
from mypackages import screen_info as si
from mypackages import experiment


## モニター，ウィンドウの設定 ##
mon = monitors.Monitor("myMonitor")
screen_size = si.get_screen_resolution()
mon.setSizePix(screen_size)  # 解像度をピクセル単位で設定
mon.setWidth(si.get_screen_width_cm())  # モニターの幅をcm単位で設定
win = visual.Window(size=screen_size, fullscr=True, monitor=mon, units="cm")

e = experiment.Experiment(win,
                          ratio_left_gaze = 0.8, # 左を見ている顔画像の割合
                          trials_per_set = 20, # 1セットあたりの試行回数
                          sets_per_block = 2, # 1ブロックあたりのセット数
                          n_block = 10, # ブロック数
                          SOUND = False, # 間違えたときにビープ音を鳴らすか
                          output_dir = "./data/experiment_A" # 出力ファイルのディレクトリパス
                          )

e.instruct()
e.signal_to_start(1)
e.experiment()
win.close()