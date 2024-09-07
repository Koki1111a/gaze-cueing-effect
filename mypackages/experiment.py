import random
import winsound
from mypackages.save_data import save_to_csv
from mypackages import screen_info as si
from psychopy import visual, core, event
from datetime import datetime


class Experiment:

    def __init__(self,
                 win: visual.Window,
                 ratio_left_gaze = 0.5, # 左を見ている顔画像の割合
                 trials_per_set = 8, # 1セットあたりの試行回数
                 sets_per_block = 1, # 1ブロックあたりのセット数
                 n_block = 1, # ブロック数
                 SOUND = True, # 間違えたときにビープ音を鳴らすか
                 output_dir = None # 出力ファイルのディレクトリパス
                 ):
    
        self.win = win
        self.ratio_left_gaze = ratio_left_gaze
        self.trials_per_set = trials_per_set
        self.sets_per_block = sets_per_block
        self.n_block = n_block
        self.SOUND = SOUND
        self.output_dir = output_dir

        self.left_gaze = "./assets/face_l.png" # 左を見ている顔画像のパス
        self.right_gaze = "./assets/face_r.png" # 右を見ている顔画像のパス
        self.magnification_image = 0.3 # 画像の拡大率
        self.y_image = -0.5 # 画像のy座標(単位：cm)
        self.current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") # 現在の日時を取得
        self.data = [["Trial number", "Gaze", "Target location", "Congruency", "Target identity", "Response", "Correct", "Response time"]] # 記録するデータ
        
        if self.output_dir is not None:
            save_to_csv(self.output_dir, [self.data[0]], self.current_time)

        self.trials_left_gaze = [
            [self.left_gaze, "T", 6.0],
            [self.left_gaze, "F", 6.0],
            [self.left_gaze, "T", -6.0],
            [self.left_gaze, "F", -6.0]
        ]

        self.trials_right_gaze = [
            [self.right_gaze, "T", 6.0],
            [self.right_gaze, "F", 6.0],
            [self.right_gaze, "T", -6.0],
            [self.right_gaze, "F", -6.0]
        ]

        self.block = ( 
                self.trials_left_gaze * int(self.ratio_left_gaze * self.trials_per_set / len(self.trials_left_gaze) + 0.01)
                    + self.trials_right_gaze * int( (1.0-self.ratio_left_gaze) * self.trials_per_set / len(self.trials_right_gaze) + 0.01)
                ) * self.sets_per_block

        self.fixation_stim = visual.TextStim(self.win, "+", pos=(0, 0), height=0.6)
        self.letter_stim = visual.TextStim(self.win)
        self.text1_stim = visual.TextStim(self.win, units="norm", wrapWidth=si.get_screen_width_cm())
        self.text2_stim = visual.TextStim(self.win, units="norm", wrapWidth=si.get_screen_width_cm())
        self.text3_stim = visual.TextStim(self.win, units="norm", wrapWidth=si.get_screen_width_cm())
        self.image_stim = visual.ImageStim(self.win, pos=(0, self.y_image))
        self.image_stim.setSize([element * self.magnification_image for element in self.image_stim.size]) # 顔画像のサイズ調節
        self.stopwatch = core.Clock()
        event.Mouse(False) # マウスカーソルを非表示にする



    ### 強制終了の設定 ###
    def event_quit(self):
        keys = event.getKeys()

        if "c" in keys and ("lctrl" in keys or "rctrl" in keys):
            print("KeyboardInterrupt")
            self.win.close()
            core.quit()
        
        return
               

    ### 実験 ###
    def experiment(self):
        
        Trial_number = 0
        for i in range(self.n_block):
            if i > 0:
                core.wait(2)
                self.signal_to_start(i+1)

            random.shuffle(self.block) # リストの中身をシャッフルする

            for gaze, letter, x_axis in self.block:
                ## 注視点 ##
                self.fixation_stim.draw()
                self.win.flip()
                core.wait(0.500) # 500ms待つ
                self.event_quit()

                ## 顔刺激 ##
                self.image_stim.setImage(gaze)
                self.image_stim.draw()
                self.win.flip()
                core.wait(0.200) # 200ms待つ
                self.event_quit()

                ## 標的刺激 ##
                self.letter_stim.setText(letter)
                self.letter_stim.setPos([x_axis, 0])
                self.letter_stim.draw()
                self.image_stim.draw()
                self.win.flip()
                self.stopwatch.reset()

                ## 反応時間の計測 ##
                resp = event.waitKeys(keyList = ["a", "l"], timeStamped = self.stopwatch)
                self.event_quit()

                ## 記録 ##
                Trial_number = Trial_number + 1
                Gaze = 1 if gaze == self.left_gaze else 2
                Target_location = 1 if x_axis < 0 else 2
                Congruency = 1 if Gaze == Target_location else 2
                Target_identity = 1 if letter == "F" else 2
                Response = 1 if resp[0][0] == "l" else 2
                Correct = 1 if Target_identity == Response else 2
                Response_time = float(resp[0][1]) * 1000
                self.data.append([Trial_number, Gaze, Target_location, Congruency, Target_identity, Response, Correct, Response_time])
                print(self.data[Trial_number])

                if self.output_dir is not None:
                    save_to_csv(self.output_dir, [self.data[Trial_number]], self.current_time)
                

                if self.SOUND and Correct == 2: # 間違えたときのビープ音
                    winsound.Beep(1000, 1000)

                ## ブランク ##
                self.win.flip()
                core.wait(1.000) # 1000ms待つ
                self.event_quit()


        return self.data


    ### 実験の説明 ###
    def instruct(self):
        self.text1_stim.setPos((0, 0.6))
        self.text1_stim.setHeight(0.1)
        self.text2_stim.setText("< 前に戻る(A)")
        self.text2_stim.setPos((-0.7, -0.7))
        self.text2_stim.setHeight(0.07)
        self.text3_stim.setText("次に進む(L) >")
        self.text3_stim.setPos((0.7, -0.7))
        self.text3_stim.setHeight(0.07)
        flag = 1
        
        while flag <= 5:

            ## Step 1 ##
            if flag == 1:
                self.text1_stim.setText("1. 最初に注視点を見て下さい")
                self.text1_stim.draw()
                self.text3_stim.draw()
                self.fixation_stim.draw()
                self.win.flip()
                key = event.waitKeys(keyList = ["l"])
                flag = flag + 1
                self.event_quit()

            ## Step 2 ##
            if flag == 2:
                self.text1_stim.setText("2. 左右どちらかに視点を向けた顔画像が出てきます")
                self.image_stim.setImage(self.right_gaze)
                self.text1_stim.draw()
                self.text2_stim.draw()
                self.text3_stim.draw()
                self.image_stim.draw()
                self.win.flip()
                key = event.waitKeys(keyList = ["a", "l"])
                flag = flag - 1 if key[0][0] == "a" else flag + 1
                self.event_quit()

            ## Step 3 ##
            if flag == 3:
                self.text1_stim.setText("3. その後，標的刺激が画面の左右どちらかに呈示されます")
                self.letter_stim.setText("T")
                self.letter_stim.setPos([-6, 0])
                self.image_stim.setImage(self.right_gaze)
                self.text1_stim.draw()
                self.text2_stim.draw()
                self.text3_stim.draw()
                self.letter_stim.draw()
                self.image_stim.draw()
                self.win.flip()
                key = event.waitKeys(keyList = ["a", "l"])
                flag = flag - 1 if key[0][0] == "a" else flag + 1
                self.event_quit()

            ## Step 4 ##
            if flag == 4:
                self.text1_stim.setText("4. 顔刺激の視線方向は標的刺激の出現とは無関係です")
                self.text3_stim.setText("次に進む(L) >")
                self.letter_stim.setText("F")
                self.letter_stim.setPos([6, 0])
                self.image_stim.setImage(self.left_gaze)
                self.text1_stim.draw()
                self.text2_stim.draw()
                self.text3_stim.draw()
                self.letter_stim.draw()
                self.image_stim.draw()
                self.win.flip()
                key = event.waitKeys(keyList = ["a", "l"])
                flag = flag - 1 if key[0][0] == "a" else flag + 1
                self.event_quit()

            ## Step 5 ##
            if flag == 5:
                self.text1_stim.setText("5. 標的が何かを判断して，\nFならばLのキーを，TならばAのキーを\nなるべく早くかつ正確に押してください")
                self.text3_stim.setText("説明を終了する(L) >")
                self.text1_stim.draw()
                self.text2_stim.draw()
                self.text3_stim.draw()
                self.letter_stim.draw()
                self.image_stim.draw()
                self.win.flip()
                key = event.waitKeys(keyList = ["a", "l"])
                flag = flag - 1 if key[0][0] == "a" else flag + 1
                self.event_quit()
        
        return
    
    def signal_to_start(self, block_number=None):

        self.text1_stim.setPos((0, 0.3))
        self.text1_stim.setHeight(0.2)

        if block_number is None:
            self.text1_stim.setText("練習試行を実施します")
        else:
            self.text1_stim.setText(f"{block_number}ブロック目の試行を行います．")

        self.text2_stim.setText("Aキー + Lキー\n\nで実験が始まります")
        self.text2_stim.setPos((0, -0.2))
        self.text2_stim.setHeight(0.1)
        
        self.text1_stim.draw()
        self.text2_stim.draw()
        self.win.flip()

        while True:
            self.stopwatch.reset()
            core.wait(0.400, 0.400)
            keys = event.getKeys(timeStamped = self.stopwatch)
            self.event_quit()

            column = [row[0] for row in keys]
            if "a" in column and "l" in column:
                core.wait(0.400-keys[-1][1])
                self.win.flip()
                core.wait(0.600)
                return
