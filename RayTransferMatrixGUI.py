import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QScrollArea,QSlider,QRadioButton,QComboBox,QLineEdit,QCheckBox,QFrame,QStatusBar
from PyQt5.QtGui import QDoubleValidator
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from PyQt5.QtCore import Qt
from optics_data import optics_data
from RTM import rvec

# 근축근사
# 2023-11-27  ver.1
# plano-convex lens에 대해서만 계산
# optics None => 길이만 추가

class ClickWidget(QWidget):
    def __init__(self, update_total_widgets_callback,optics_data):
        super().__init__()
        self.optics_data = optics_data
        self.first_key =  next(iter(self.optics_data))
        self.first_data = self.optics_data[self.first_key]  
        self.n_air =  self.first_data["n_air"]
        self.n_N_BK7 =  self.first_data["n_N_BK7"]
        self.rad_curv = self.first_data["rad_curv"]
        self.c_thick = self.first_data["c_thick"]
        self.f =  self.first_data["f"]
        self.fb =  self.first_data["fb"]
        self.isfilp = False
        self.distance = 0
        self.initUI()
        self.update_total_widgets_callback = update_total_widgets_callback

    def initUI(self):

        # qframe 추가
        self.frame = QFrame(self)
        self.frame.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.frame.setLineWidth(1)
        
        
        self.main_layout = QVBoxLayout()
       

        # 드롭박스 
        self.optics_dropdown = QComboBox()
        self.optics_dropdown.addItems(self.optics_data.keys())
        self.optics_dropdown.currentIndexChanged.connect(self.combobox_change)

        # 플립 버튼
        self.flip_optics_checkbox = QCheckBox("Flip Optics")
        self.flip_optics_checkbox.stateChanged.connect(self.checkbox_change)

        # 삭제 버튼
        delete_button = QPushButton('x', self)
        delete_button.clicked.connect(self.delete_widget)

        # 거리 입력
        self.distance_input = QLineEdit()
        self.distance_input.setValidator(QDoubleValidator())
        self.distance_input.setPlaceholderText("Distance")
        self.distance_input.textChanged.connect(self.edit_change)

        # f 정보
        f_label = QLabel('F =')
        self.f_text = QLabel(f"{self.f}", self)


        layout = QVBoxLayout()
        layout_top = QHBoxLayout()
        layout_btm = QHBoxLayout()

        layout_top.addWidget(self.optics_dropdown)
        layout_top.addWidget(self.flip_optics_checkbox)
        layout_top.addWidget(delete_button)

        layout_btm.addWidget(self.distance_input)
        layout_btm.addWidget(f_label)
        layout_btm.addWidget(self.f_text)

        layout.addLayout(layout_top)
        layout.addLayout(layout_btm)

        self.main_layout.addLayout(layout)


        self.frame.setLayout(self.main_layout)
        top_level_layout = QVBoxLayout(self)  # Pass self to set the layout for the widget
        top_level_layout.addWidget(self.frame) 


        # # 레이아웃 적용
     
        


        
        

    def delete_widget(self):
        self.setParent(None)
        self.update_total_widgets_callback()

    def combobox_change(self):
        ''''''
        self.first_key = self.optics_dropdown.currentText()
        self.first_data = self.optics_data[self.first_key]
        self.n_air =  self.first_data["n_air"]
        self.n_N_BK7 =  self.first_data["n_N_BK7"]
        self.rad_curv = self.first_data["rad_curv"]
        self.c_thick = self.first_data["c_thick"]
        self.f =  self.first_data["f"]
        self.fb =  self.first_data["fb"]
        self.f_text.setText(f"{self.f}")
        self.update_total_widgets_callback()

    def checkbox_change(self):
        self.isfilp =  self.flip_optics_checkbox.isChecked()
        self.update_total_widgets_callback()

    def edit_change(self):

        if self.distance_input.text() == "":
            self.distance = 0
        try:
            self.distance = float(self.distance_input.text())
        except:
            self.disconce = 0
        
        self.update_total_widgets_callback()
        

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.optics_data_list = []
        self.optics_data_list_flip = []
        self.optics_data_list_distance = []
        self.widget_count = 0
        self.initUI()

    def initUI(self):
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)

        scroll_area = QScrollArea(self)
        scroll_area.setWidget(self.scroll_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        # QScrollArea의 내용들이 항상 위로 정렬되고 최소 크기를 갖도록 설정
        self.scroll_layout.setAlignment(Qt.AlignTop)
        


        control_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        add_button = QPushButton('추가', self)
        add_button.clicked.connect(self.add_click_widget)
        button_layout.addWidget(add_button)

        delete_all_button = QPushButton('모두 삭제', self)
        delete_all_button.clicked.connect(self.delete_all_widgets)
        button_layout.addWidget(delete_all_button)


        # # 현재 optics 전체 갯수
        # self.total_widgets_label = QLabel('위젯 개수: 0', self)
        # control_layout.addWidget(self.total_widgets_label)

    
        # 레이아웃 설정
        plot_layout = QVBoxLayout()
      

        # 슬라이더 설정 start position
        slider_layout_pos = QHBoxLayout()
        pos_label = QLabel("Position")
        pos_label.setMinimumWidth(100)
        min_pos_label = QLabel("-10")
        min_pos_label.setMinimumWidth(50)
        max_pos_label = QLabel("10")
        max_pos_label.setMinimumWidth(50)
        self.slider_pos = QSlider(Qt.Horizontal)
        self.slider_pos.setMinimum(-10)
        self.slider_pos.setMaximum(10)
        self.slider_pos.setTickInterval(1)  # 1 단위로 틱 간격 설정
        self.slider_pos.setTickPosition(QSlider.TicksBelow)
        self.slider_pos.valueChanged.connect(self.update_plot)
        slider_layout_pos.addWidget(pos_label)
        slider_layout_pos.addWidget(min_pos_label)
        slider_layout_pos.addWidget(self.slider_pos)
        slider_layout_pos.addWidget(max_pos_label)
        control_layout.addLayout(slider_layout_pos)

        # 슬라이더 설정 start angle
        slider_layout_ang = QHBoxLayout()
        ang_label = QLabel("Angle")
        ang_label.setMinimumWidth(100)
        min_ang_label = QLabel("-5")
        min_ang_label.setMinimumWidth(50)
        max_ang_label = QLabel("5")
        max_ang_label.setMinimumWidth(50)
        self.slider_ang = QSlider(Qt.Horizontal)
        self.slider_ang.setMinimum(-10)
        self.slider_ang.setMaximum(10)
        self.slider_ang.setTickInterval(1)  # 1 단위로 틱 간격 설정
        self.slider_ang.setTickPosition(QSlider.TicksBelow)
        self.slider_ang.valueChanged.connect(self.update_plot)
        slider_layout_ang.addWidget(ang_label)
        slider_layout_ang.addWidget(min_ang_label)
        slider_layout_ang.addWidget(self.slider_ang)
        slider_layout_ang.addWidget(max_ang_label)
        control_layout.addLayout(slider_layout_ang)

        # 라디오 버튼 설정
        radio_layout = QHBoxLayout()
        self.radio_point = QRadioButton("Point Light Source")
        self.radio_laser = QRadioButton("Laser")
        self.total_mode = QRadioButton("Total Mode")
        self.radio_point.setChecked(True)  # 기본값 설정
        self.radio_point.toggled.connect(self.update_plot)
        self.radio_laser.toggled.connect(self.update_plot)
        self.total_mode.toggled.connect(self.update_plot)
        radio_layout.addWidget(self.radio_point)
        radio_layout.addWidget(self.radio_laser)
        radio_layout.addWidget(self.total_mode)
        control_layout.addLayout(radio_layout)

        # 그래프 캔버스 설정
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        plot_layout.addWidget(self.canvas)

        # 초기 그래프 업데이트
        self.update_plot()

        optics_layout = QVBoxLayout()
        optics_layout.addLayout(control_layout)
        optics_layout.addWidget(scroll_area)
        optics_layout.addLayout(button_layout)

        main_layout = QHBoxLayout()

        main_layout.addLayout(plot_layout,3)
        main_layout.addLayout(optics_layout,1)
        

        self.setLayout(main_layout)
        self.resize(2400, 1200)  # 
        self.update_total_widgets()


        # status bar 추가
        self.statuslabel = QLabel()
        control_layout.addWidget(self.statuslabel)
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)

    def add_click_widget(self):
        new_widget = ClickWidget( self.update_total_widgets, optics_data)
        self.scroll_layout.insertWidget(-1, new_widget)  # 위젯을 위쪽에 추가
        self.update_total_widgets()

    def delete_all_widgets(self):
            for widget in self.scroll_widget.findChildren(ClickWidget):
                widget.deleteLater()
            self.update_total_widgets()

    def update_total_widgets(self):
        self.optics_data_list=[]
        self.optics_data_list_flip = []
        self.optics_data_list_distance = []
        self.optics_data_list_first_key = []
        for widget in self.scroll_widget.findChildren(ClickWidget):
            self.optics_data_list.append(widget.first_data)
            self.optics_data_list_flip.append(widget.isfilp)
            self.optics_data_list_distance.append(widget.distance)
            self.optics_data_list_first_key.append(widget.first_key)
            
        self.widget_count = len(self.optics_data_list)
        self.update_plot()

        # print(self.widget_count)
        # print(self.optics_data_list)
        # print(self.optics_data_list_flip)
        # print(self.optics_data_list_distance)
        


    # plot Layout

    def update_plot(self):

        # -10 ~ 10
        start_point = self.slider_pos.value()

        # -5 ~ 5
        start_angle = self.slider_ang.value()/2


        self.ax.clear()

        # lens specific
        # n_air = 1.0
        # n_N_BK7 = 1.5106
        # rad_curv = 38.6
        # c_thick = 4.1
        # f = 74.8
        # fb = 72.0

        # thick_lens (n_ait , n_N_BK7, rad_curv, -np.inf , c_thick)   오른쪽이 평면인 

        if self.radio_laser.isChecked():
            self.draw_laser(start_point,start_angle)

        elif self.radio_point.isChecked():
            self.draw_point_light_source(start_point,start_angle)

        else:
            self.draw_laser(0,0)
            self.draw_qunatum(start_point,start_angle)
            
             
        # 선 그리기 렌즈선, 
        vertical_lines = []
        lens_lins = []
        temp = 0
        line_pos = np.zeros(2)
        for  i ,optics in enumerate(self.optics_data_list) : 
            for k, j in enumerate([0, optics["f"] + self.optics_data_list_distance[i], optics["c_thick"],optics["fb"]]):
                line_pos += j
                
                # lens line 파란색으로 그리기
                if k == 1 or k ==2:
                    self.ax.plot(line_pos,[-25.4/2,25.4/2],'b')

                    # lens 이름 위치 정하기 1
                    if k == 1:
                        temp += line_pos[0]
                    
                    # lens 이름 위치 정하기 2
                    if k == 2: 
                        temp += j/2
                        vertical_lines.append(round(temp))
                        lens_lins.append(round(temp))
                        temp = 0


                else:


                    self.ax.plot(line_pos,[-25.4/2,25.4/2],'k')
                    vertical_lines.append(round(line_pos[0]))

        self.ax.set_xticks(vertical_lines)
        self.ax.set_title("Ray Transfer Plot (right side is flat)")

        # 렌즈 위치 라벨링 하기
        for i , pos in enumerate(lens_lins):
            self.ax.text(pos, self.ax.get_ylim()[0] - (self.ax.get_ylim()[1] - self.ax.get_ylim()[0]) * 0.1,
                        self.optics_data_list_first_key[i], fontsize=15, color='black', ha='center')

        self.ax.axhline(0 , color = 'gray' , linestyle = 'dashed' , linewidth = 1)

        self.canvas.draw()


    def toggle_source(self):
        if self.source_type == 'point light source':
            self.source_type = 'laser'
        else:
            self.source_type = 'point light source'
        self.update_plot()

    def draw_laser(self,start_point,start_angle):
        # 레이저
        for j in [(-0.25 + start_point,'g'),(0.25 + start_point,'g')]: #beam start point
            for i in [start_angle]: #beam angle (deg)
                p = [rvec(j[0],np.deg2rad(i))] # 시작 위치 및 각도

                # # Calculations optics 갯수만큼
                for  i ,optics in enumerate(self.optics_data_list) :

                    p.append(p[-1].propagate(optics["f"] + self.optics_data_list_distance[i]))

                    if self.optics_data_list_flip[i]:
                        p.append(p[-1].thick_lens(optics["n_air"], optics["n_N_BK7"], optics["rad_curv"],-np.inf, optics["c_thick"]))
                    else:
                        p.append(p[-1].thick_lens(optics["n_air"], optics["n_N_BK7"], np.inf, -optics["rad_curv"], optics["c_thick"]))


                    p.append(p[-1].propagate(optics["fb"]))

                z = np.linspace(p[0].z,p[-1].z,100)
                x = np.interp(z,[rv.z for rv in p],[rv.x for rv in p])
                self.ax.plot(z,x,j[1])

    def draw_point_light_source(self,start_point,start_angle):
        # 점광원
            for j in [( start_point,'y')]: #,beam start point
                for i in np.linspace(-start_angle,start_angle,2):  # 광선의 각도
                    p = [rvec(j[0],np.deg2rad(i))]  # 시작 위치 및 각도

                    for  i ,optics in enumerate(self.optics_data_list) :

                        p.append(p[-1].propagate(optics["f"] + self.optics_data_list_distance[i]))

                        if self.optics_data_list_flip[i]:
                            p.append(p[-1].thick_lens(optics["n_air"], optics["n_N_BK7"], optics["rad_curv"],-np.inf, optics["c_thick"]))
                        else:
                            p.append(p[-1].thick_lens(optics["n_air"], optics["n_N_BK7"], np.inf, -optics["rad_curv"], optics["c_thick"]))


                        p.append(p[-1].propagate(optics["fb"]))

                    # Draw
                    z = np.linspace(p[0].z,p[-1].z,100)
                    x = np.interp(z,[rv.z for rv in p],[rv.x for rv in p])
                    self.ax.plot(z,x,j[1])


    def draw_qunatum(self,start_point,start_angle):
        # start_point를 가지는 두개의 빔 생성
        # 각각의 빔에 대해서 start_angle만큼의 각도를 가지는 빔 생성
        # 생성된 각각의 빔에서 start_angle 만큼 각도를 가지는 밤을 또 생성
        # 생성된 빔들을 각각의 optics에 대해서 계산
        # 계산된 결과를 그래프에 표시

        for j in [( 0,'r')]:
            for i in [-start_angle]:
                    # k 좌표를 기준으로 start_point만큼 떨어진 각도에 빔 생성

                    p = [rvec(j[0],np.deg2rad(i))]

                    for  i ,optics in enumerate(self.optics_data_list) :

                        p.append(p[-1].propagate(optics["f"] + self.optics_data_list_distance[i]))

                        if self.optics_data_list_flip[i]:
                            p.append(p[-1].thick_lens(optics["n_air"], optics["n_N_BK7"], optics["rad_curv"],-np.inf, optics["c_thick"]))
                        else:
                            p.append(p[-1].thick_lens(optics["n_air"], optics["n_N_BK7"], np.inf, -optics["rad_curv"], optics["c_thick"]))


                        p.append(p[-1].propagate(optics["fb"]))

                    z = np.linspace(p[0].z,p[-1].z,100)
                    x = np.interp(z,[rv.z for rv in p],[rv.x for rv in p])
                    self.ax.plot(z,x,j[1])

        for j in [( 0,'r--')]:
            for k in [start_angle]:
                for i in [-k-start_point,-k + start_point]:
                    p = [rvec(j[0],np.deg2rad(i))]

                    for  i ,optics in enumerate(self.optics_data_list) :

                        p.append(p[-1].propagate(optics["f"] + self.optics_data_list_distance[i]))

                        if self.optics_data_list_flip[i]:
                            p.append(p[-1].thick_lens(optics["n_air"], optics["n_N_BK7"], optics["rad_curv"],-np.inf, optics["c_thick"]))
                        else:
                            p.append(p[-1].thick_lens(optics["n_air"], optics["n_N_BK7"], np.inf, -optics["rad_curv"], optics["c_thick"]))


                        p.append(p[-1].propagate(optics["fb"]))

                    z = np.linspace(p[0].z,p[-1].z,100)
                    x = np.interp(z,[rv.z for rv in p],[rv.x for rv in p])
                    # -- 모양 plot
                    self.ax.plot(z,x,j[1])

        for j in [( 0,'b')]:
            for i in [start_angle]:
                    # k 좌표를 기준으로 start_point만큼 떨어진 각도에 빔 생성

                    p = [rvec(j[0],np.deg2rad(i))]

                    for  i ,optics in enumerate(self.optics_data_list) :

                        p.append(p[-1].propagate(optics["f"] + self.optics_data_list_distance[i]))

                        if self.optics_data_list_flip[i]:
                            p.append(p[-1].thick_lens(optics["n_air"], optics["n_N_BK7"], optics["rad_curv"],-np.inf, optics["c_thick"]))
                        else:
                            p.append(p[-1].thick_lens(optics["n_air"], optics["n_N_BK7"], np.inf, -optics["rad_curv"], optics["c_thick"]))


                        p.append(p[-1].propagate(optics["fb"]))

                    z = np.linspace(p[0].z,p[-1].z,100)
                    x = np.interp(z,[rv.z for rv in p],[rv.x for rv in p])
                    self.ax.plot(z,x,j[1])

        for j in [( 0,'b--')]:
            for k in [start_angle]:
                for i in [-start_point, start_point]:
                    p = [rvec(j[0],(np.deg2rad(k) - np.deg2rad(i)))]

                    for  i ,optics in enumerate(self.optics_data_list) :

                        p.append(p[-1].propagate(optics["f"] + self.optics_data_list_distance[i]))

                        if self.optics_data_list_flip[i]:
                            p.append(p[-1].thick_lens(optics["n_air"], optics["n_N_BK7"], optics["rad_curv"],-np.inf, optics["c_thick"]))
                        else:
                            p.append(p[-1].thick_lens(optics["n_air"], optics["n_N_BK7"], np.inf, -optics["rad_curv"], optics["c_thick"]))


                        p.append(p[-1].propagate(optics["fb"]))

                    z = np.linspace(p[0].z,p[-1].z,100)
                    x = np.interp(z,[rv.z for rv in p],[rv.x for rv in p])
                    # -- 모양 plot
                    self.ax.plot(z,x,j[1])

    # 마우스 이동 이벤트 처리기 메소드
    def on_mouse_move(self, event):
        if event.inaxes:
            # 마우스 위치 정보 업데이트
            self.statuslabel.setText(f"X: {event.xdata:.2f}, Y: {event.ydata:.2f}")

        else:
            self.statuslabel.setText("")
       

def main():
    app = QApplication(sys.argv)
    main_widget = MainWidget()
    main_widget.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    plt.rcParams['font.size'] = 15
    plt.rcParams['axes.titlesize'] = 30  # 축 타이틀 폰트 크기
    main()
