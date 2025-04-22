import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel, QFileDialog, QDialog, QHBoxLayout, QMainWindow
from PyQt6.QtCore import Qt
from datetime import datetime, timedelta
import re

class InputDialog(QDialog):
    def __init__(self, title, text='', parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setGeometry(300, 300, 800, 600)  # 모달 창 크기 설정
        self.layout = QVBoxLayout(self)

        self.text_edit = QTextEdit(self)
        self.text_edit.setPlainText(text)  # 기존 텍스트 설정
        self.layout.addWidget(self.text_edit)

        self.button_layout = QHBoxLayout()
        self.ok_button = QPushButton("확인", self)
        self.ok_button.clicked.connect(self.accept)
        self.button_layout.addWidget(self.ok_button)

        self.cancel_button = QPushButton("취소", self)
        self.cancel_button.clicked.connect(self.reject)
        self.button_layout.addWidget(self.cancel_button)

        self.layout.addLayout(self.button_layout)
        
        self.center()
        
    def center(self):
        screen = QApplication.primaryScreen()  # 기본 화면을 가져옵니다
        screen_geometry = screen.availableGeometry()  # 사용 가능한 화면 크기
        qr = self.frameGeometry()  # 현재 창의 크기
        center_point = screen_geometry.center()  # 화면의 중앙 좌표
        qr.moveCenter(center_point)  # 창의 중앙을 화면 중앙으로 이동
        self.move(qr.topLeft())  # 창의 위치 설정


    def get_text(self):
        return self.text_edit.toPlainText()

class WeeklyReportApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        title_label = QLabel("Rapeech Weekly Report Program", self)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2C3E50; text-align: center; margin-bottom: 20px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        self.start_date, self.end_date = self.get_week_dates()
        self.next_start_date, self.next_end_date = self.get_next_week_dates()
        
        # 금주 실적 입력
        self.current_week_label = QLabel("금주 실적 내용 입력:")
        layout.addWidget(self.current_week_label)
        self.current_week_input = QTextEdit()
        self.current_week_input.setPlaceholderText("여기에 금주 실적 내용을 입력하세요...")
        self.current_week_input.mousePressEvent = lambda event: self.open_current_week_dialog()
        layout.addWidget(self.current_week_input)

        # 차주 계획 입력
        self.next_week_label = QLabel("차주 계획 내용 입력:")
        layout.addWidget(self.next_week_label)
        self.next_week_input = QTextEdit()
        self.next_week_input.setPlaceholderText("여기에 차주 계획 내용을 입력하세요...")
        self.next_week_input.mousePressEvent = lambda event: self.open_next_week_dialog()
        layout.addWidget(self.next_week_input)

        # ISSUE 및 요청사항 입력
        self.issue_label = QLabel("ISSUE 및 요청사항 입력:")
        layout.addWidget(self.issue_label)
        self.issue_input = QTextEdit()
        self.issue_input.setPlaceholderText("여기에 ISSUE 및 요청사항을 입력하세요...")
        self.issue_input.mousePressEvent = lambda event: self.open_issue_dialog()
        layout.addWidget(self.issue_input)

        # RISK 입력
        self.risk_label = QLabel("RISK 입력:")
        layout.addWidget(self.risk_label)
        self.risk_input = QTextEdit()
        self.risk_input.setPlaceholderText("여기에 RISK 내용을 입력하세요...")
        self.risk_input.mousePressEvent = lambda event: self.open_risk_dialog()
        layout.addWidget(self.risk_input)

        self.save_button = QPushButton("HTML 저장", self)
        self.save_button.clicked.connect(self.save_html)
        layout.addWidget(self.save_button)

        self.credit_label = QLabel("made by JeonHyeonJae", self)
        self.credit_label.setStyleSheet("font-size: 12px; color: gray; text-align: right;")
        self.credit_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.credit_label)
        
        self.setLayout(layout)
        self.setWindowTitle("즐거운 금요일~!")
        self.setGeometry(300, 300, 600, 600)
        self.center()
        
    def center(self):
        screen = QApplication.primaryScreen()  # 기본 화면을 가져옵니다
        screen_geometry = screen.availableGeometry()  # 사용 가능한 화면 크기
        qr = self.frameGeometry()  # 현재 창의 크기
        center_point = screen_geometry.center()  # 화면의 중앙 좌표
        qr.moveCenter(center_point)  # 창의 중앙을 화면 중앙으로 이동
        self.move(qr.topLeft())  # 창의 위치 설정
    
    def open_current_week_dialog(self):
        dialog = InputDialog("금주 실적 내용 입력", self.current_week_input.toPlainText(), self)
        if dialog.exec():
            self.current_week_input.setPlainText(dialog.get_text())

    def open_next_week_dialog(self):
        dialog = InputDialog("차주 계획 내용 입력", self.next_week_input.toPlainText(), self)
        if dialog.exec():
            self.next_week_input.setPlainText(dialog.get_text())

    def open_issue_dialog(self):
        dialog = InputDialog("ISSUE 및 요청사항 입력", self.issue_input.toPlainText(), self)
        if dialog.exec():
            self.issue_input.setPlainText(dialog.get_text())

    def open_risk_dialog(self):
        dialog = InputDialog("RISK 입력", self.risk_input.toPlainText(), self)
        if dialog.exec():
            self.risk_input.setPlainText(dialog.get_text())

    def get_week_dates(self):
        today = datetime.today()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=4)
        return start_of_week.strftime('%y.%m.%d'), end_of_week.strftime('%y.%m.%d')

    def get_next_week_dates(self):
        today = datetime.today()
        start_of_next_week = today + timedelta(days=(7 - today.weekday()))
        end_of_next_week = start_of_next_week + timedelta(days=4)
        return start_of_next_week.strftime('%y.%m.%d'), end_of_next_week.strftime('%y.%m.%d')

    def convert_pms_links(self, text):
        text = re.sub(r'#(\d+)', r'* PMS link (<span style="color: rgb(255, 94, 0);"><a href="https://project.test.com/issues/\1" target="_blank">#\1</a></span>)', text)
        text = re.sub(r'\[(.*?)\]', r'<b>[\1]</b>', text)
        text = re.sub(r'^(##.*)$', r'<b>\1</b>', text, flags=re.MULTILINE)
        text = re.sub(r'(\d+)%?\s*(보류)', r'<span style="background-color: #848484; color: white; padding: 2px;"><b>\1% \2</b></span>', text)
        text = re.sub(r'(\d+)%?\s*(완료)', r'<span style="background-color: #4673FF; color: white; padding: 2px;"><b>\1% \2</b></span>', text)
        text = re.sub(r'(\d+)%?\s*(진행중)', r'<span style="background-color: #FFE400; color: black; padding: 2px;"><b>\1% \2</b></span>', text)
        text = re.sub(r'%?\s*(연기)', r'<span style="background-color: #FF4848; color: white; padding: 2px;"><b>연기</b></span>', text)
        text = re.sub(r'(\d+\.\s*.*?)(?=\n|$)', r'<b>\1</b>', text)
        return text

    def save_html(self):
        current_week_content = self.convert_pms_links(self.current_week_input.toPlainText())
        next_week_content = self.convert_pms_links(self.next_week_input.toPlainText())
        issue_content = self.convert_pms_links(self.issue_input.toPlainText())
        risk_content = self.convert_pms_links(self.risk_input.toPlainText())
        
        html_content = f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Dotum, 맑은 고딕; }}
                table {{ width: 100%; border-collapse: collapse; }}
                th, td {{ border: 1px solid rgb(204, 204, 204); padding: 0px; vertical-align: top; min-height: 240px; }}
                th {{ background-color: #D4F4FA; }}
                td.issue-risk {{ background-color: #D4F4FA; }}
                a {{ color: #FF0000; text-decoration: none; }}
                a:hover {{ text-decoration: underline; }}
                .issue-risk-cell {{ min-height: 100px; }}
                footer {{ text-align: right; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <table class="txc-table">
                <tr>
                    <th colspan="2">금주 실적 ({self.start_date} - {self.end_date})</th>
                    <th colspan="2">차주 계획 ({self.next_start_date} - {self.next_end_date})</th>
                </tr>
                <tr>
                    <td colspan="2">
                        <pre style="background-color: white; color: black; border: none;">{current_week_content}</pre>
                    </td>
                    <td colspan="2">
                        <pre style="background-color: white; color: black; border: none;">{next_week_content}</pre>
                    </td>
                </tr>
                <tr>
                    <td colspan="2" class="issue-risk">ISSUE 및 요청사항</td>
                    <td colspan="2" class="issue-risk">RISK</td>
                </tr>
                <tr>
                    <td colspan="2" class="issue-risk-cell">
                        <pre style="background-color: white; color: black; border: none;">{issue_content}</pre>
                    </td>
                    <td colspan="2" class="issue-risk-cell">
                        <pre style="background-color: white; color: black; border: none;">{risk_content}</pre>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """
        
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "weekly_report.html", "HTML Files (*.html)")
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(html_content)
        
        print("HTML 파일이 저장되었습니다.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WeeklyReportApp()
    ex.show()
    sys.exit(app.exec())

