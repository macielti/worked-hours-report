import os 
import json

FILE_PATH="config.json"

class Config:
    @staticmethod
    def creates_config_file():
        if not os.path.exists("config.json"):
            initial_content = {
                                "format-week": "Início Expediente: <start>\nSaída para almoço: <lunch-start>\nRetorno do almoço: <lunch-end>\nEncerramento do Expediente: <end>\n\nHoras trabalhadas hoje: <worked-hours-today>",
                                "format-weekend": "Início Expediente: <start>\nEncerramento do Expediente: <end>\n\nTempo trabalhado hoje: <worked-hours-today>"
                                }
            with open(FILE_PATH, "w") as data_file_obj:
                json.dump(initial_content, data_file_obj)

    @staticmethod
    def load_get_config_object():
        with open(FILE_PATH, 'r') as data_file_obj:
            config = json.load(data_file_obj)
            return config