from typing import Dict, List, Union
import datetime
import combilog


def get_channel_list(self):
    """ 
    Overrides Combilog.get_channel_list() 
    Gets channel names using one iteration only 
    """
    self.channel_list = ["Datetime"]
    num_channels = self.device_info().get("nr_channels")
    for chan in range(1, num_channels + 1):
        channel_name = self.get_channel_info(f"{chan:02}").get("channel_notation")
        self.channel_list.append(channel_name)
    return self.channel_list


def read_event(self, pointer: Union[str, int],) -> Dict:
    """
    read the event at the position of the pointer
    returns a dictionary with the timestamp as key
    if there are no events an empty dict is returned
    """
    if str(pointer) == "1":
        call = "E"
    elif str(pointer) == "2":
        call = "e"
    else:
        raise ValueError(f"pointer must be either 1 or 2, not {pointer}")
    with self.ser as ser:
        telegram = f"${self.logger_addr}{call}\r".encode("latin-1")
        ser.write(telegram)
        resp = ser.read_until(b"\r")
    if len(resp) > 3:
        events = resp.decode("latin-1")[1:].split(";")
        # the first char is the address and therefore not needed
        date = datetime.datetime.strptime(events[0][1:], "%y%m%d%H%M%S")
        # remove carriage return at the end
        # and convert from IEE Std 754 Short Real Format
        channel_values = [date]
        for i in events[1:-1]:
            channel_values.append(combilog._hexIEE_to_dec(i))
        event = {key: value for key, value in zip(self.channel_list, channel_values)}
        return event
    else:
        return {}


def read_logger(self, pointer: Union[str, int]):
    """
    reads all bookings starting from the set pointer
    :pointer str|int: the pointer from where to read
    """
    # get number of logs
    logs = self.get_nr_events()
    events = []
    for i in range(logs):
        event = self.read_event(pointer)
        events.append(event)
    return events
