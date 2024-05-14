import sys

def get_battery_level():
    platform = sys.platform.lower()
    if platform.startswith('linux') or platform.startswith('darwin'):
        try:
            import psutil
            battery = psutil.sensors_battery()
            if battery is not None:
                return battery.percent
        except ImportError:
            pass
    elif platform.startswith('win'):
        try:
            import psutil
            battery = psutil.sensors_battery()
            if battery is not None:
                return battery.percent
        except ImportError:
            import ctypes
            class SYSTEM_POWER_STATUS(ctypes.Structure):
                _fields_ = [
                    ('ACLineStatus', ctypes.c_byte),
                    ('BatteryFlag', ctypes.c_byte),
                    ('BatteryLifePercent', ctypes.c_byte),
                    ('Reserved1', ctypes.c_byte),
                    ('BatteryLifeTime', ctypes.c_ulong),
                    ('BatteryFullLifeTime', ctypes.c_ulong),
                ]
            SYSTEM_POWER_STATUS_P = ctypes.POINTER(SYSTEM_POWER_STATUS)
            GetSystemPowerStatus = ctypes.windll.kernel32.GetSystemPowerStatus
            GetSystemPowerStatus.argtypes = [SYSTEM_POWER_STATUS_P]
            GetSystemPowerStatus.restype = ctypes.c_bool

            status = SYSTEM_POWER_STATUS()
            if GetSystemPowerStatus(ctypes.pointer(status)):
                return status.BatteryLifePercent
            else:
                return None
        except:
            pass
    elif platform == 'android':
        try:
            from plyer import battery
            info = battery.status
            return info["percentage"]
        except ImportError:
            pass
    return None

if __name__ == "__main__":
    battery_level = get_battery_level()
    if battery_level is not None:
        print(f"Battery Level: {battery_level}%")
    else:
        print("Unable to retrieve battery level.")
