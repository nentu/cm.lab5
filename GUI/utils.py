from PyQt5.QtWidgets import QMessageBox, QFileDialog


def save_to_file(self, text):
    userResponse = QMessageBox.question(self,
                                        "Тип вывода",
                                        'Хотите сохранить в файл?',
                                        QMessageBox.Save | QMessageBox.Cancel,
                                        QMessageBox.Cancel
                                        )
    if userResponse == QMessageBox.Save:
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "Text Files (*.txt)", options=options)
        if fileName:
            try:
                f = open(fileName + ".txt", 'a')
                f.write(text + '\n')
                f.close()
            except Exception as e:
                print(e)


def show_error(msg_text):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText("Ошибка")
    msg.setInformativeText(msg_text)
    msg.setWindowTitle("Ошибка")
    msg.exec_()