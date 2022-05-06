import psycopg2
import sys
from PyQt5.QtWidgets import (QApplication, QWidget,
QTabWidget, QAbstractScrollArea,
QVBoxLayout, QHBoxLayout,
QTableWidget, QGroupBox,
QTableWidgetItem, QPushButton, QMessageBox)

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self._connect_to_db()
        self.setWindowTitle("Shedule")
        self.vbox = QVBoxLayout(self)
        self.tabs = QTabWidget(self)
        self.vbox.addWidget(self.tabs)
        self._create_shedule_tab()
        self._create_teachers_tab()
        self._create_Subjects_tab()

    def _connect_to_db(self):
        self.conn = psycopg2.connect(database="Lab7",user="postgres", password="1111", host="localhost", port="5432")
        self.cursor = self.conn.cursor()

    def _create_teachers_tab(self):
        self.teachers_tab = QWidget()
        self.tabs.addTab(self.teachers_tab, "Teacher")
        self.teachers_gbox = QGroupBox("Subjects")
        self.svboxT = QVBoxLayout()
        self.shbox1T = QHBoxLayout()
        self.shbox2T = QHBoxLayout()
        self.shbox3T = QHBoxLayout()
        self.svboxT.addLayout(self.shbox1T)
        self.svboxT.addLayout(self.shbox2T)
        self.svboxT.addLayout(self.shbox3T)
        self.shbox1T.addWidget(self.teachers_gbox)
        self._create_teachers_table()
        self.update_teachers_button = QPushButton("Update")
        self.insert_teachers_button = QPushButton("Insert")
        self.shbox2T.addWidget(self.update_teachers_button)
        self.shbox3T.addWidget(self.insert_teachers_button)
        self.update_teachers_button.clicked.connect(self._update_tecahers)
        self.insert_teachers_button.clicked.connect(self._insert_teacher)
        self.teachers_tab.setLayout(self.svboxT)


    def _create_Subjects_tab(self):
        self.subjects_tab = QWidget()
        self.tabs.addTab(self.subjects_tab, "Subjects")
        self.subjects_gbox = QGroupBox("Subjects")
        self.svboxSub = QVBoxLayout()
        self.shbox1Sub = QHBoxLayout()
        self.shbox2Sub = QHBoxLayout()
        self.shbox3Sub = QHBoxLayout()
        self.svboxSub.addLayout(self.shbox1Sub)
        self.svboxSub.addLayout(self.shbox2Sub)
        self.svboxSub.addLayout(self.shbox3Sub)
        self.shbox1Sub.addWidget(self.subjects_gbox)
        self._create_subjects_table()
        self.update_subjects_button = QPushButton("Update")
        self.insert_subjects_button = QPushButton("Insert")
        self.shbox2Sub.addWidget(self.update_subjects_button)
        self.shbox3Sub.addWidget(self.insert_subjects_button)
        self.update_subjects_button.clicked.connect(self._update_subjects)
        self.insert_subjects_button.clicked.connect(self._insert_subject)
        self.subjects_tab.setLayout(self.svboxSub)

    def _create_shedule_tab(self):
        self.shcedule_tab = QWidget()
        self.tabs.addTab(self.shcedule_tab, "Shedule")
        self.schedule_gbox = QGroupBox("Schedule")
        self.svboxS = QVBoxLayout()
        self.shbox1S = QHBoxLayout()
        self.shbox2S = QHBoxLayout()
        self.shbox3S = QHBoxLayout()
        self.svboxS.addLayout(self.shbox1S)
        self.svboxS.addLayout(self.shbox2S)
        self.svboxS.addLayout(self.shbox3S)
        self.shbox1S.addWidget(self.schedule_gbox)
        self._create_schedule_table()
        self.update_schedule_button = QPushButton("Update")
        self.insert_schedule_button = QPushButton("Insert")
        self.shbox2S.addWidget(self.update_schedule_button)
        self.shbox3S.addWidget(self.insert_schedule_button)
        self.update_schedule_button.clicked.connect(self._update_shedule)
        self.insert_schedule_button.clicked.connect(self._insert_schedule)
        self.shcedule_tab.setLayout(self.svboxS)

    def _create_schedule_table(self):
        self.monday_table = QTableWidget()
        self.monday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.monday_table.setColumnCount(8)
        self.monday_table.setHorizontalHeaderLabels(["Id", "Day", "Start Time","Room Number","Subject","Tecaher","Update","Delete"])
        self._update_schedule_table()
        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.monday_table)
        self.schedule_gbox.setLayout(self.mvbox)

    def _create_subjects_table(self):
        self.subjects_table = QTableWidget()
        self.subjects_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.subjects_table.setColumnCount(4)
        self.subjects_table.setHorizontalHeaderLabels(["Id", "Name", "Update", "Delete"])
        self._update_subjects_table()
        self.mvboxSub = QVBoxLayout()
        self.mvboxSub.addWidget(self.subjects_table)
        self.subjects_gbox.setLayout(self.mvboxSub)

    def _create_teachers_table(self):
        self.teachers_table = QTableWidget()
        self.teachers_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.teachers_table.setColumnCount(5)
        self.teachers_table.setHorizontalHeaderLabels(["Id", "Full name", "Subject name", "Update", "Delete"])
        self._update_teachers_table()
        self.mvboxT = QVBoxLayout()
        self.mvboxT.addWidget(self.teachers_table)
        self.teachers_gbox.setLayout(self.mvboxT)

    def _update_schedule_table(self):
        self.cursor.execute("select  tt.\"Id\",tt.\"day\",tt.\"startTime\",tt.\"roomNumber\",s.\"name\",tea.\"fullName\" from timetable as tt join subjects as s on s.\"Id\"=tt.\"subjectId\" join teachers as tea on s.\"Id\"=tea.\"subjectId\"")
        records = list(self.cursor.fetchall())
        self.monday_table.setRowCount(len(records) + 1)
        self.monday_table.clear()
        self.monday_table.setColumnCount(8)
        self.monday_table.setHorizontalHeaderLabels(["Id", "Day", "Start Time", "Room Number", "Subject", "Tecaher", "Update", "Delete"])
        for i, r in enumerate(records):
            r = list(r)
            updateScheduleRowButton = QPushButton("Update")
            deleteScheduleRowButton = QPushButton("Delete")
            self.monday_table.setItem(i, 0,QTableWidgetItem(str(r[0])))
            self.monday_table.setItem(i, 1,QTableWidgetItem(str(r[1])))
            self.monday_table.setItem(i, 2,QTableWidgetItem(str(r[2])))
            self.monday_table.setItem(i, 3, QTableWidgetItem(str(r[3])))
            self.monday_table.setItem(i, 4, QTableWidgetItem(str(r[4])))
            self.monday_table.setItem(i, 5, QTableWidgetItem(str(r[5])))
            self.monday_table.setCellWidget(i, 6, updateScheduleRowButton)
            self.monday_table.setCellWidget(i, 7, deleteScheduleRowButton)
            updateScheduleRowButton.clicked.connect(lambda ch, num=i: self._update_schedulRow(num))
            deleteScheduleRowButton.clicked.connect(lambda ch, num=i: self._delete_scheduleRow(num))
            self.monday_table.resizeRowsToContents()

    def _update_subjects_table(self):
        self.cursor.execute("SELECT \"Id\", name FROM public.subjects")
        records = list(self.cursor.fetchall())
        self.subjects_table.clear()
        self.subjects_table.setColumnCount(4)
        self.subjects_table.setHorizontalHeaderLabels(["Id", "Name", "Update", "Delete"])
        self.subjects_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)
            updateSubjectButton= QPushButton("Update")
            deleteSubjectButton = QPushButton("Delete")
            self.subjects_table.setItem(i, 0,QTableWidgetItem(str(r[0])))
            self.subjects_table.setItem(i, 1,QTableWidgetItem(str(r[1])))
            self.subjects_table.setCellWidget(i, 2, updateSubjectButton)
            self.subjects_table.setCellWidget(i, 3, deleteSubjectButton)
            updateSubjectButton.clicked.connect(lambda ch, num=i: self._update_subject(num))
            deleteSubjectButton.clicked.connect(lambda ch, num=i: self._delete_subject(num))
            self.subjects_table.resizeRowsToContents()

    def _update_teachers_table(self):
        self.cursor.execute("SELECT tt.\"Id\", tt.\"fullName\", sub.\"name\" FROM teachers tt join subjects sub on sub.\"Id\"=tt.\"subjectId\"")
        records = list(self.cursor.fetchall())
        self.teachers_table.clear()
        self.teachers_table.setColumnCount(5)
        self.teachers_table.setHorizontalHeaderLabels(["Id", "Full name", "Subject name", "Update", "Delete"])
        self.teachers_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)
            updateTeacherButton = QPushButton("Update")
            deleteTeacherButton = QPushButton("Delete")
            self.teachers_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.teachers_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.teachers_table.setItem(i, 2, QTableWidgetItem(str(r[2])))
            self.teachers_table.setCellWidget(i, 3, updateTeacherButton)
            self.teachers_table.setCellWidget(i, 4, deleteTeacherButton)
            updateTeacherButton.clicked.connect(lambda ch, num=i: self._update_teacher(num))
            deleteTeacherButton.clicked.connect(lambda ch, num=i: self._delete_teacher(num))
            self.teachers_table.resizeRowsToContents()

    def _update_subject(self, rowNum):
        if self.subjects_table.item(rowNum, 1) == None or self.subjects_table.item(rowNum, 0) == None:
            QMessageBox.about(self, "Error", f"empty row {rowNum}")
            return
        subjectName = self.subjects_table.item(rowNum, 1).text()
        subjectId = self.subjects_table.item(rowNum, 0).text()
        if subjectName == None or len(subjectName) == 0 or subjectId == None or len(subjectId) == 0:
            QMessageBox.about(self, "Error", f"empty row {rowNum}")
            return
        self.cursor.execute(f"UPDATE subjects SET name='{subjectName}' WHERE \"Id\"={subjectId}")
        self.conn.commit()
        self._update_subjects()

    def _delete_subject(self, rowNum):
        if self.subjects_table.item(rowNum, 0) == None:
            QMessageBox.about(self, "Error", f"empty row {rowNum}")
            return
        subjectId = self.subjects_table.item(rowNum, 0).text()
        if subjectId != None and len(subjectId) != 0:
            QMessageBox.about(self, "Error", f"empty row {rowNum}")
            return
        self.cursor.execute(f"DELETE FROM subjects WHERE \"Id\"={subjectId}")
        self.conn.commit()
        self._update_subjects()

    def _update_teacher(self, rowNum):
        if self.teachers_table.item(rowNum, 1) == None or self.teachers_table.item(rowNum, 0) == None or self.teachers_table.item(rowNum, 2) == None:
            QMessageBox.about(self, "Error", f"empty row {rowNum}")
            return
        assignetSubject = self.teachers_table.item(rowNum, 2).text()
        teacherName = self.teachers_table.item(rowNum, 1).text()
        teacherId = self.teachers_table.item(rowNum, 0).text()
        if assignetSubject == None or len(assignetSubject) == 0 or teacherName == None or len(teacherName) == 0 or teacherId == None or len(teacherId) == 0:
            QMessageBox.about(self, "Error", f"empty row {rowNum}")
        self.cursor.execute(f"SELECT \"Id\", name FROM public.subjects where name='{assignetSubject}'")
        reader = list(self.cursor.fetchall())
        if len(reader) == 0:
            QMessageBox.about(self, "Error", f"subject is not found{rowNum}")
            return
        subjectid = reader[0][0]
        self.cursor.execute(f"UPDATE teachers SET \"fullName\"='{teacherName}', \"subjectId\"={subjectid} WHERE \"Id\"={teacherId}")
        self.conn.commit()
        self._update_tecahers()

    def _delete_teacher(self, rowNum):
        if self.teachers_table.item(rowNum, 0) == None:
            QMessageBox.about(self, "Error", f"empty row {rowNum}")
            return
        teacherId = self.teachers_table.item(rowNum, 0).text()
        if teacherId == None or len(teacherId) == 0:
            QMessageBox.about(self, "Error", f"teacher id is incorrect in row {rowNum}")
            return
        self.cursor.execute(f"DELETE FROM teachers WHERE \"Id\"={teacherId}")
        self.conn.commit()
        self._update_tecahers()

    def _update_schedulRow(self,rowNum):
        if self.monday_table.item(rowNum, 0) == None or self.monday_table.item(rowNum, 1) == None or self.monday_table.item(rowNum, 2) == None or self.monday_table.item(rowNum, 3) == None or self.monday_table.item(rowNum, 4) == None or self.monday_table.item(rowNum, 5) == None:
            QMessageBox.about(self, "Error", f"empty row {rowNum}")
            return
        scheduleRowId = self.monday_table.item(rowNum, 0).text()
        Day = self.monday_table.item(rowNum, 1).text()
        StartTime = self.monday_table.item(rowNum, 2).text()
        RoomNumber = self.monday_table.item(rowNum, 3).text()
        Subject = self.monday_table.item(rowNum, 4).text()
        if Subject == None or len(Subject) == 0:
            QMessageBox.about(self, "Error", f"subject is empty in row {rowNum}")
            return
        self.cursor.execute(f"SELECT \"Id\", name FROM subjects where name='{Subject}'")
        readerSub = list(self.cursor.fetchall())
        if len(readerSub) == 0:
            QMessageBox.about(self, "Error", f"subject is not found")
            return
        subjectid = readerSub[0][0]
        if scheduleRowId == None or len(scheduleRowId) == 0 or Day != None and len(Day) == 0 or StartTime == None or len(StartTime) == 0 or RoomNumber == None or len(RoomNumber) == 0:
            QMessageBox.about(self, "Error", f"some filed is empty in row {rowNum}")
            return
        self.cursor.execute(f"UPDATE timetable SET day='{Day}', \"subjectId\"={subjectid}, \"roomNumber\"={rowNum}, \"startTime\"='{StartTime}' WHERE \"Id\"={scheduleRowId}")
        self.conn.commit()
        self._update_shedule()

    def _delete_scheduleRow(self, rowNum):
        if self.monday_table.item(rowNum, 0) == None:
            QMessageBox.about(self, "Error", f"empty row {rowNum}")
            return
        scheduleRowId = self.monday_table.item(rowNum, 0).text()
        if scheduleRowId == None or len(scheduleRowId) == 0:
            QMessageBox.about(self, "Error", f"incorrect id in row {rowNum}")
            return
        self.cursor.execute(f"DELETE FROM timetable WHERE \"Id\"={scheduleRowId}")
        self.conn.commit()
        self._update_shedule()

    def _update_shedule(self):
        self._update_schedule_table()
    def _update_subjects(self):
        self._update_subjects_table()
    def _update_tecahers(self):
        self._update_teachers_table()

    def _insert_subject(self):
        if self.subjects_table.item(self.subjects_table.rowCount()-1,1)==None:
            QMessageBox.about(self, "Error", f"empty inserted row")
            return
        subjectName = self.subjects_table.item(self.subjects_table.rowCount()-1,1).text()
        if subjectName==None and len(subjectName) != 0:
            QMessageBox.about(self, "Error", f"incorrect fileds")
            return
        self.cursor.execute(f"INSERT INTO subjects(name) VALUES ('{subjectName}')")
        self.conn.commit()
        self._update_subjects()

    def _insert_teacher(self):
        if self.teachers_table.item(self.teachers_table.rowCount()-1,1)==None or  self.teachers_table.item(self.teachers_table.rowCount()-1,2)==None:
            QMessageBox.about(self, "Error", f"empty inserted row")
            return
        teacherName = self.teachers_table.item(self.teachers_table.rowCount()-1,1).text()
        assignetSubject = self.teachers_table.item(self.teachers_table.rowCount() - 1, 2).text()
        if assignetSubject==None or len(assignetSubject) == 0:
            QMessageBox.about(self, "Error", f"subcet name empty")
            return
        self.cursor.execute(f"SELECT \"Id\", name FROM public.subjects where name='{assignetSubject}'")
        reader=list(self.cursor.fetchall())
        if len(reader)==0:
            QMessageBox.about(self, "Error", f"subject is not found")
            return
        subjectid = reader[0][0]
        if teacherName==None or len(teacherName) == 0:
            QMessageBox.about(self, "Error", f"fileds is incorrect")
            return
        self.cursor.execute(f"INSERT INTO teachers(\"fullName\", \"subjectId\")VALUES ('{teacherName}',{subjectid})")
        self.conn.commit()
        self._update_tecahers()

    def _insert_schedule(self):
        if self.monday_table.item(self.monday_table.rowCount()-1,1)==None or  self.monday_table.item(self.monday_table.rowCount()-1,2)==None or  self.monday_table.item(self.monday_table.rowCount()-1,3)==None or  self.monday_table.item(self.monday_table.rowCount()-1,4)==None or  self.monday_table.item(self.monday_table.rowCount()-1,5)==None:
            QMessageBox.about(self, "Error", f"empty inserted row")
            return
        Day = self.monday_table.item(self.monday_table.rowCount()-1,1).text()
        StartTime = self.monday_table.item(self.monday_table.rowCount() - 1, 2).text()
        RoomNumber = self.monday_table.item(self.monday_table.rowCount() - 1, 3).text()
        Subject = self.monday_table.item(self.monday_table.rowCount() - 1, 4).text()
        if Subject==None or len(Subject) == 0:
            QMessageBox.about(self, "Error", f"subject name empty")
            return
        self.cursor.execute(f"SELECT \"Id\", name FROM subjects where name='{Subject}'")
        readerSub=list(self.cursor.fetchall())
        if len(readerSub)==0:
            QMessageBox.about(self, "Error", f"subject is not found")
            return
        subjectid = readerSub[0][0]
        if Day==None or len(Day) == 0 or StartTime==None or len(StartTime) == 0 or RoomNumber==None or len(RoomNumber) == 0:
            QMessageBox.about(self, "Error", f"fileds is incorrect")
            return
        self.cursor.execute(f"INSERT INTO timetable(day, \"subjectId\", \"roomNumber\", \"startTime\") VALUES ( '{Day}', {subjectid}, {RoomNumber}, {StartTime})")
        self.conn.commit()
        self._update_shedule()


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())




