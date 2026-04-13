from utils.input_manager import InputManager, OutofRange, InvalidType, EmptyInput
from utils.json_manager import JSONManager, JSONSchemaError
from models.record import Record
from models.quiz import Quiz
class QuizGame:

    def __init__(self, json_manager):
        self.__quizzes = []
        self.__record = []
        self.__score = 0
        self.__json_manager = json_manager
        self.__data_changed_flag = False

    def add_quiz(self, quiz):
        self.__quizzes.append(quiz)
        self.__data_changed_flag = True

    def del_quiz(self, quiz_num):
        del self.__quizzes[quiz_num]

    def play_game(self):
        pass

    def show_quizzes(self):
        return self.__quizzes

    def show_records(self):
        return self.__record

    def __load_data(self):
        pass

    def __save_data(self):
        pass
    
    def close(self):
        self.__save_data()
        pass