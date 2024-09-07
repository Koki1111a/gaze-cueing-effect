from psychopy import visual, monitors
from mypackages import screen_info as si
from mypackages import experiment


## モニター，ウィンドウの設定 ##
mon = monitors.Monitor("myMonitor")
screen_size = si.get_screen_resolution()
mon.setSizePix(screen_size)  # 解像度をピクセル単位で設定
mon.setWidth(si.get_screen_width_cm())  # モニターの幅をcm単位で設定
win = visual.Window(size=screen_size, fullscr=True, allowGUI=False, monitor=mon, units="cm")
win.mouseVisible =False

e = experiment.Experiment(win,
                          ratio_left_gaze = 0.5, # 左を見ている顔画像の割合
                          trials_per_set = 8, # 1セットあたりの試行回数
                          sets_per_block = 3, # 1ブロックあたりのセット数
                          n_block = 1, # ブロック数
                          SOUND = True # 間違えたときにビープ音を鳴らすか
                          )

e.instruct()
e.signal_to_start()
e.experiment()
win.close()