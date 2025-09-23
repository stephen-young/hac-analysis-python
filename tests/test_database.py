import hac_analysis.database as db
import json
import datetime


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
    start_time = datetime.datetime.fromisoformat("2018-01-29 10:51:41")
    end_time = datetime.datetime.fromisoformat("2018-01-29 11:55:49")

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
