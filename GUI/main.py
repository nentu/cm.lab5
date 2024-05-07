import sys

import numpy as np
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from sympy import latex, Lambda
from sympy.abc import x

from GUI.gui_consts import formulas
from GUI.math_text_label import MathTextLabel
from GUI.plot import MyFuncPlot, colors
from GUI.utils import show_error, save_to_file
from logic.UniformNuton import UniformNutonInterpolator
from logic.interpolator import interpolate, names, class_list


# TODO doc
def round_points(x_list, y_list, k=4):
    return [
        x_list.astype(float).round(k),
        y_list.astype(float).round(k)
    ]


class UI(QMainWindow):

    def __init__(self):
        super(UI, self).__init__()
        self.prop_plot_graph = None
        self.funcs_list = None
        self.input_field_arg = None
        uic.loadUi("GUI.ui", self)

        self.widget_start = self.findChild(QWidget, 'start_widget')
        self.widget_input_text = self.findChild(QWidget, 'input_text_widget')
        self.widget_input_func = self.findChild(QWidget, 'function_widget')
        self.widget_res = self.findChild(QWidget, 'res_widget')

        self.eq_box = self.findChild(QComboBox, 'select_func_comboBox')
        self.start_box = self.findChild(QDoubleSpinBox, 'spin_start')
        self.stop_box = self.findChild(QDoubleSpinBox, 'spin_end')
        self.count_box = self.findChild(QSpinBox, 'spin_count')
        self.text_field_input = self.findChild(QTextEdit, 'textEdit_input')

        self.findChild(QPushButton, 'btn_func_input').clicked.connect(self.function_input)
        self.findChild(QPushButton, 'btn_text_input').clicked.connect(self.text_input)
        self.findChild(QPushButton, 'select_func_btn').clicked.connect(self.select_func)
        self.findChild(QPushButton, 'solve_text_btn').clicked.connect(self.input_text)

        self.start_box.valueChanged.connect(self.start_changed)
        self.stop_box.valueChanged.connect(self.end_changed)

        self.findChild(QPushButton, 'load_file_btn').clicked.connect(self.insert_text_from_file)

        self.widget_input_text.setVisible(False)
        self.widget_input_func.setVisible(False)
        self.widget_res.setVisible(False)

        self.show()

    def start_changed(self):
        val = self.start_box.value()
        self.stop_box.setRange(val, 1000)

    def end_changed(self):
        val = self.stop_box.value()
        self.start_box.setRange(-1000, val)

    def input_text(self):
        self.solve(self.text_field_input.toPlainText().replace(',', '.'))

    def solve(self, text):
        x_list = list()
        y_list = list()
        try:

            for row in text.split('\n'):
                if row == '':
                    continue
                if row.count(' ') > 1:
                    show_error(f'Неправильный формат: слишком много пробелов в строке "{row}"')
                    return
                x_list.append(float(row.split()[0]))
                y_list.append(float(row.split()[1]))

            if len(x_list) == 0:
                show_error('Неправильный формат: пустое поле')
                return
        except Exception:
            show_error('Неправильный формат')
            return

        self.do_interpolate(np.array(x_list), np.array(y_list))

    def select_func(self):
        start = self.start_box.value()
        stop = self.stop_box.value()
        count = self.count_box.value()

        id = int(self.eq_box.currentText()) - 1

        func = Lambda(x, formulas[id])
        print(func)

        x_list = np.linspace(start, stop, count)
        v_func = np.vectorize(func)
        y_list = v_func(x_list)

        self.do_interpolate(x_list, y_list, [func])

    def insert_text_from_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*)", options=options)
        if fileName:
            try:
                text = open(fileName, 'r').read()
                self.text_field_input.setText(text)
            except IOError as e:
                show_error(f"Ошибка открытия файла: {e}")

    def text_input(self):
        self.widget_start.setVisible(False)
        self.widget_input_text.setVisible(True)

    def function_input(self):
        self.widget_start.setVisible(False)
        self.widget_input_func.setVisible(True)

        self.show_equations()

    def show_equations(self):
        l = self.findChild(QVBoxLayout, 'formulas_layout')
        for i in range(len(formulas)):
            row = QHBoxLayout()
            row.addWidget(QLabel(f'{i + 1}) '))
            row.addWidget(MathTextLabel('$' + latex(formulas[i]) + '=0$', self),
                          alignment=Qt.AlignHCenter)
            l.addLayout(row)
            self.eq_box.addItem(str(i + 1))

        # row = QHBoxLayout()
        # row.addWidget(QLabel(f'{len(self.usualFormulas) + 1}) '))
        # row.addLayout(FormulaInput(self.addFormula))
        # l.addLayout(row)

    def update_table_arg(self):
        for i, func in enumerate(self.funcs_list):
            self.table_args.setItem(0, i, QTableWidgetItem(f'{round(func(self.input_field_arg.value()), 2)}'))

    def do_interpolate(self, x_list, y_list, added_funcs=[]):
        # Получение индексов для сортировки
        sorted_indices = np.argsort(x_list)

        # Применение индексов к обоим массивам для сортировки
        x_list = x_list[sorted_indices]
        y_list = y_list[sorted_indices]
        print(y_list)
        text = ''

        text += f'X: {x_list}\n'
        text += f'Y: {y_list}\n'
        self.funcs_list = interpolate(x_list, y_list)

        text += 'Interpolated functions:\n\t'
        text += '\n\t'.join(list(map(str, self.funcs_list)))
        text += '\n'*2
        self.funcs_list = added_funcs + self.funcs_list
        res_layout = self.findChild(QVBoxLayout, 'res_layout')

        self.prop_plot_graph = graph = MyFuncPlot()
        round_n = 3
        graph.paint_graph(self.funcs_list, round_points(x_list, y_list))
        res_layout.addWidget(graph)

        map_lables = QHBoxLayout()
        for i in range(len(names)):
            q = QLabel(names[i])
            r, g, b = colors[i + 1]
            q.setStyleSheet(f"background-color: rgb({r}, {g}, {b}); color: rgb(100, 100, 100);")
            map_lables.addWidget(q)
        res_layout.addLayout(map_lables)  # add check argument

        layout_func_arg = QHBoxLayout()
        self.input_field_arg = QDoubleSpinBox()
        self.input_field_arg.valueChanged.connect(self.update_table_arg)
        self.input_field_arg.setRange(-1000, 1000)
        self.table_args = QTableWidget()
        self.table_args.setRowCount(1)
        self.table_args.setColumnCount(len(self.funcs_list))

        layout_func_arg.addWidget(self.input_field_arg)
        layout_func_arg.addWidget(self.table_args)

        res_layout.addLayout(layout_func_arg)

        self.update_table_arg()

        table = QTableWidget()
        n = x_list.size + 1
        table.setRowCount(
            n
        )
        table.setColumnCount(
            n
        )

        text += '\nTable\n'
        header_list = ['xi'] + [f'd{i}yi' for i in range(n)]
        text += '\t'.join(header_list)

        table.setHorizontalHeaderLabels(header_list)
        for i in range(n):
            table.setItem(i, 0, QTableWidgetItem(f'x{i}'))

        nuton = UniformNutonInterpolator(x_list, y_list)

        for k in range(x_list.size):
            row = ''
            for i in range(x_list.size - k):
                s = str(round(nuton.d_k_y_i(k, i), 3))
                row += s + '\t'
                table.setItem(i, k + 1, QTableWidgetItem(s))
            text += row + '\n'
        table.setMinimumHeight(300)

        res_layout.addWidget(table)

        table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.widget_input_func.setVisible(False)
        self.widget_res.setVisible(True)

        save_to_file(self, text)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UI()
    app.exec_()
