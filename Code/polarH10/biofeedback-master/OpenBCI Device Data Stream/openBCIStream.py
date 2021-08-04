import time

import brainflow
import numpy as np
import pandas as pd
from brainflow.board_shim import BoardIds, BoardShim, BrainFlowInputParams
from brainflow.data_filter import AggOperations, DataFilter, FilterTypes


def scale_magnitude_array(x, ymin, ymax):
    x = np.array(x)
    return (x - ymin) / (ymax - ymin)


def board_2_df(data):
    # data = scale_magnitude_array(data, -396, 433)
    df = pd.DataFrame(data[:, [1, 22]], columns=["ECG", "TIME"])
    return df


class CytonBoard(object):
    def __init__(self, serial_port):
        self.params = BrainFlowInputParams()
        self.params.serial_port = serial_port
        self.board = BoardShim(BoardIds.CYTON_BOARD.value, self.params)

    def start_stream(self):
        self.board.prepare_session()
        self.board.start_stream()

    def stop_stream(self):
        self.board.stop_stream()
        self.board.release_session()

    def poll(self, sample_num):
        try:
            while self.board.get_board_data_count() < sample_num:
                time.sleep(0.02)
        except Exception as e:
            raise (e)
        board_data = self.board.get_board_data()
        df = board_2_df(np.transpose(board_data))
        return df

    def sampling_frequency(self):
        sampling_freq = self.board.get_sampling_rate(BoardIds.CYTON_BOARD.value)
        return sampling_freq
