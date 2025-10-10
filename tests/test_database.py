import hac_analysis.database as db
import json
from datetime import datetime
from math import isclose


def test_database_connect():
    success = False

    with open("./res/database.json", "r") as f:
        db_info = json.load(f)

    try:
        db.connect(db_info)
        success = True
    except Exception as e:
        print(f"An exception occured! {e}")

    assert success


def test_query_tag_list():
    with open("./res/database.json", "r") as f:
        db_info = json.load(f)

    conn = db.connect(db_info)
    table_info = {"name": "Nov13th2017", "database": "HAC", "tags": "TagItemID"}
    start_time = datetime.fromisoformat("2018-01-29 10:51:41")
    end_time = datetime.fromisoformat("2018-01-29 11:55:49")

    result = db.query_tag_list(conn, table_info, start_time, end_time)
    want = "Power metering.CVM2.U_12"

    want = [
        ("Power metering.CVM2.U_12",),
        ("ABB_Test.VFD#2.SpeedREF-2",),
        ("ABB_Test.VFD#2.CW-2",),
        ("GTW-1 Port 3 (T+RH) Top.Temp/RH 1.TT1",),
        ("GTW-1 Port 1.Pump_2.RTR2",),
        ("Analogue Inputs.I/O-1.DPT-2",),
        ("Analogue Inputs.I/O-2.LT-1",),
        ("Analogue Inputs.I/O-2.LT-2",),
        ("ABB_Test.VFD#2.TorqPerc-2",),
        ("Power metering.CVM1.kW_Tot",),
        ("Analogue Inputs.I/O-2.LT-3",),
        ("Analogue Inputs.I/O-1.FT-5",),
        ("Power metering.CVM2.I_2",),
        ("GTW-1 Port 4 (T+RH) Bottom.Temp/RH 2.GT2",),
        ("GTW-1 Port 1.DowncomerShaft.RTR1",),
        ("GTW-1 Port 1.Pump_1.RTR2",),
        ("Power metering.CVM2.U_23",),
        ("GTW-1 Port 4 (T+RH) Bottom.Temp/RH 2.TT2",),
        ("GTW-1 Port 1.Pump_1.In89",),
        ("Power metering.CVM1.U_31",),
        ("Analogue Inputs.I/O-1.FT-2",),
        ("ABB_Test.VFD#1.TorqPerc-1",),
        ("Power metering.CVM2.PF_Tot",),
        ("Power metering.CVM1.I_1",),
        ("GTW-1 Port 1.Pump_2.RTR1",),
        ("Power metering.CVM2.U_31",),
        ("Power metering.CVM2.I_1",),
        ("GTW-1 Port 3 (T+RH) Top.Temp/RH 1.GT1",),
        ("GTW-1 Port 1.Pump_1.In67",),
        ("Analogue Inputs.I/O-3.FCV-2",),
        ("Power metering.CVM1.Hz",),
        ("Analogue Inputs.I/O-1.FT-1",),
        ("Power metering.CVM1.PF_Tot",),
        ("GTW-1 Port 1.Pump_2.In89",),
        ("Power metering.CVM1.I_2",),
        ("ABB_Test.VFD#1.CW-1",),
        ("Analogue Outputs.I/O-4.FCV-1",),
        ("Analogue Inputs.I/O-1.FT-4",),
        ("GTW-1 Port 1.Pump_1.RTR1",),
        ("Power metering.CVM2.kW_Tot",),
        ("Power metering.CVM1.U_23",),
        ("GTW-1 Port 1.DowncomerShaft.RTR2",),
        ("Power metering.CVM1.I_3",),
        ("GTW-1 Port 1.Pump_2.In67",),
        ("ABB_Test.VFD#2.SpeedACT-2",),
        ("ABB_Test.VFD#1.SpeedREF-1",),
        ("Power metering.CVM2.Hz",),
        ("ABB_Test.VFD#1.SW-1",),
        ("ABB_Test.VFD#1.SpeedACT-1",),
        ("Power metering.CVM2.I_3",),
        ("Analogue Inputs.I/O-2.PT-17",),
        ("Power metering.CVM1.U_12",),
        ("ABB_Test.VFD#2.SW-2",),
        ("Analogue Inputs.I/O-1.DPT-1",),
        ("Analogue Inputs.I/O-1.DPT-3",),
    ]

    assert all([x[0] == y[0] for x, y in zip(result, want)])


def test_query_insturment_data():
    FLOAT_TOL = 1e-6

    with open("./res/database.json", "r") as f:
        db_info = json.load(f)

    conn = db.connect(db_info)
    table_info = {
        "name": "Nov13th2017",
        "database": "HAC",
        "tags": "TagItemID",
        "values": "TagValue",
        "times": "TagTimestamp",
    }
    start_time = datetime.fromisoformat("2018-01-29 10:53:11")
    end_time = datetime.fromisoformat("2018-01-29 10:53:13")

    result = db.query_instrument_data(conn, table_info, start_time, end_time)
    want = [
        ("2018-01-29 10:53:11.593", "Analogue Inputs.I/O-2.LT-3", 39318),
        ("2018-01-29 10:53:11.593", "ABB_Test.VFD#1.CW-1", 1151),
        ("2018-01-29 10:53:11.593", "ABB_Test.VFD#1.SpeedACT-1", 13638),
        ("2018-01-29 10:53:11.593", "ABB_Test.VFD#1.SpeedREF-1", 13636),
        ("2018-01-29 10:53:11.593", "ABB_Test.VFD#1.SW-1", 5943),
        ("2018-01-29 10:53:11.597", "ABB_Test.VFD#2.CW-2", 1151),
        ("2018-01-29 10:53:11.597", "ABB_Test.VFD#2.SpeedACT-2", 13627),
        ("2018-01-29 10:53:11.597", "ABB_Test.VFD#2.SpeedREF-2", 13636),
        ("2018-01-29 10:53:11.597", "ABB_Test.VFD#2.SW-2", 5943),
        ("2018-01-29 10:53:11.593", "Analogue Inputs.I/O-1.DPT-1", 32261),
        ("2018-01-29 10:53:11.593", "Analogue Inputs.I/O-1.DPT-2", 52795),
        ("2018-01-29 10:53:11.593", "Analogue Inputs.I/O-1.DPT-3", 53121),
        ("2018-01-29 10:53:11.593", "Analogue Inputs.I/O-1.FT-1", 33485),
        ("2018-01-29 10:53:11.593", "Analogue Inputs.I/O-1.FT-2", 33899),
        ("2018-01-29 10:53:11.593", "Analogue Inputs.I/O-1.FT-4", 5),
        ("2018-01-29 10:53:11.593", "Analogue Inputs.I/O-1.FT-5", 2698),
        ("2018-01-29 10:53:11.593", "Analogue Inputs.I/O-2.LT-1", 35498),
        ("2018-01-29 10:53:11.593", "Analogue Inputs.I/O-2.LT-2", 65535),
        ("2018-01-29 10:53:11.593", "Analogue Inputs.I/O-2.PT-17", 43140),
        ("2018-01-29 10:53:11.593", "Analogue Inputs.I/O-3.FCV-2", 924),
        ("2018-01-29 10:53:11.687", "GTW-1 Port 1.DowncomerShaft.RTR1", 0.6092976),
        ("2018-01-29 10:53:11.687", "GTW-1 Port 1.DowncomerShaft.RTR2", 0.6098579),
        ("2018-01-29 10:53:11.737", "GTW-1 Port 1.Pump_1.In67", 32251),
        ("2018-01-29 10:53:11.737", "GTW-1 Port 1.Pump_1.In89", 34819),
        ("2018-01-29 10:53:11.787", "GTW-1 Port 1.Pump_1.RTR1", 0.6116602),
        ("2018-01-29 10:53:11.787", "GTW-1 Port 1.Pump_1.RTR2", 0.612303),
        ("2018-01-29 10:53:11.890", "GTW-1 Port 1.Pump_2.In67", 39011),
        ("2018-01-29 10:53:11.890", "GTW-1 Port 1.Pump_2.In89", 40959),
        ("2018-01-29 10:53:11.840", "GTW-1 Port 1.Pump_2.RTR1", 0.6471379),
        ("2018-01-29 10:53:11.840", "GTW-1 Port 1.Pump_2.RTR2", 0.6514329),
        ("2018-01-29 10:53:11.607", "Power metering.CVM1.Hz", 59.97357),
        ("2018-01-29 10:53:11.620", "Power metering.CVM1.I_1", 8.411773),
        ("2018-01-29 10:53:11.620", "Power metering.CVM1.I_2", 9.481759),
        ("2018-01-29 10:53:11.620", "Power metering.CVM1.I_3", 9.947979),
        ("2018-01-29 10:53:11.633", "Power metering.CVM1.kW_Tot", 6.999224),
        ("2018-01-29 10:53:11.647", "Power metering.CVM1.PF_Tot", 0.954798),
        ("2018-01-29 10:53:11.660", "Power metering.CVM1.U_12", 610.0701),
        ("2018-01-29 10:53:11.660", "Power metering.CVM1.U_23", 612.9949),
        ("2018-01-29 10:53:11.660", "Power metering.CVM1.U_31", 609.5645),
        ("2018-01-29 10:53:11.663", "Power metering.CVM2.Hz", 59.97394),
        ("2018-01-29 10:53:11.663", "Power metering.CVM2.I_1", 8.605847),
        ("2018-01-29 10:53:11.663", "Power metering.CVM2.I_2", 9.705224),
        ("2018-01-29 10:53:11.663", "Power metering.CVM2.I_3", 10.20335),
        ("2018-01-29 10:53:11.667", "Power metering.CVM2.kW_Tot", 7.196939),
        ("2018-01-29 10:53:11.667", "Power metering.CVM2.PF_Tot", 0.955294),
        ("2018-01-29 10:53:11.667", "Power metering.CVM2.U_12", 609.6976),
        ("2018-01-29 10:53:11.667", "Power metering.CVM2.U_23", 612.6187),
        ("2018-01-29 10:53:11.667", "Power metering.CVM2.U_31", 609.1956),
        ("2018-01-29 10:53:12.477", "GTW-1 Port 3 (T+RH) Top.Temp/RH 1.GT1", 164),
        ("2018-01-29 10:53:12.477", "GTW-1 Port 3 (T+RH) Top.Temp/RH 1.TT1", 44),
        ("2018-01-29 10:53:12.413", "GTW-1 Port 4 (T+RH) Bottom.Temp/RH 2.GT2", 992),
        ("2018-01-29 10:53:12.413", "GTW-1 Port 4 (T+RH) Bottom.Temp/RH 2.TT2", 86),
        ("2018-01-29 10:53:11.603", "ABB_Test.VFD#1.TorqPerc-1", 4319),
        ("2018-01-29 10:53:11.613", "ABB_Test.VFD#2.TorqPerc-2", 4477),
        ("2018-01-29 10:53:11.593", "Analogue Outputs.I/O-4.FCV-1", 200),
    ]

    assert all([x[0] == datetime.fromisoformat(y[0]) for x, y in zip(result, want)])
    assert all([x[1] == y[1] for x, y in zip(result, want)])
    assert all(
        [
            x[2] == y[2] if x[2] is int else isclose(x[2], y[2], rel_tol=FLOAT_TOL)
            for x, y in zip(result, want)
        ]
    )
