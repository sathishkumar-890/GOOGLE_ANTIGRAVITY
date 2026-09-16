import openpyxl

wb = openpyxl.load_workbook('VL_IRENE WISDOM.xlsx')
ws = wb['VL_IRENE_WISDOM']

data_updates = [
    # Page 46
    {
        'row': 18,
        'mach': 'SIGNAL LIGHT COLUMN',
        'maker': 'HME',
        'model': 'NA',
        'sno': 'NA',
        'spec': (
            'SIGNAL LIGHT COLUMN : 11 EA\n'
            '- SIGNAL LIGHT COLUMN (FOR 4232 / 4233) : 12 EA\n'
            '- SIGNAL LIGHT COLUMN RELAY BOARD : 1 EA\n'
            '- DEADMAN ALARM ALARM PANEL : 1 EA\n'
            '- DEADMAN ALARM RELAY BOARD : 1 EA\n'
            '- DEADMAN ALARM START/STOP BOX : 1 EA\n'
            '- ELECTRIC HORN : 6 EA\n'
            'WEIGHT : 286 KG'
        ),
        'manual': 'B-23_DATA BOOKLETS (MACHINERY PARTICULAR LIST).pdf',
        'pg': 46
    },
    {
        'row': 148,
        'mach': 'FIRE DETECTION & ALARM SYSTEM',
        'maker': 'AUTRONICA',
        'model': '116-AP-MAR-CAB-BUR',
        'sno': 'NA',
        'spec': (
            'MAIN CABINET : 1 EA\n'
            '- REPEATER PANEL : 1 EA\n'
            '- SMOKE DETECTOR (N.W.T) : 33 EA\n'
            '- SMOKE DETECTOR (W.T) : 50 EA\n'
            '- SMOKE DETECTOR (W.T) (FOR 4232 / 233) : 54 EA\n'
            '- HEAT DETECTOR (N.W.T) : 1 EA\n'
            '- HEAT DETECTOR (W.T) FOR GALLEY : 2 EA\n'
            '- FLAME DETECTOR : 7 EA\n'
            '- MANUAL CALL POINT (N.W.T) : 24 EA\n'
            '- MANUAL CALL POINT (W.T) : 20 EA\n'
            '- TIMER UNIT : 1 EA\n'
            '- ALARM BELL WITH LAMP : 2 EA\n'
            '- ELECTRIC HORN WITH LAMP : 1 EA\n'
            'WEIGHT : 34 KG'
        ),
        'manual': 'B-23_DATA BOOKLETS (MACHINERY PARTICULAR LIST).pdf',
        'pg': 46
    },
    {
        'row': 324,
        'mach': 'PUBLIC ADDRESS SYSTEM',
        'maker': 'MRC',
        'model': 'MPA-9000',
        'sno': 'NA',
        'spec': (
            'MAIN UNIT : 1 EA\n'
            '- REMOTE CONTROLLER : 1 EA\n'
            '- SPEAKER : 96 EA\n'
            '- PORTABLE MIC : 6 EA\n'
            '- RECEP. FOR MIC : 3 EA\n'
            '- RECEP. FOR MIC & SPEAKER : 2 EA\n'
            '- MIC & HEADSET HOOK : 7 EA\n'
            '- GENERAL ALARM PUSH BUTTON : 3 EA\n'
            'WEIGHT : 200 KG'
        ),
        'manual': 'B-23_DATA BOOKLETS (MACHINERY PARTICULAR LIST).pdf',
        'pg': 46
    },

    # Page 47
    {
        'row': 45,
        'mach': 'BRIDGE INTERFACE SYS.',
        'maker': 'JRC',
        'model': 'GRD-921',
        'sno': 'NA',
        'spec': (
            'NQE-1143 NO.1 JUNCTION BOX : 1 EA\n'
            '- NQE-1143 NO.2 JUNCTION BOX : 1 EA\n'
            '- NQE-1143 NO.3 JUNCTION BOX : 1 EA\n'
            '- NQE-1143 NO.4 JUNCTION BOX : 1 EA\n'
            '- NQE-3141-4A INTERSWITCH UNIT : 1 EA\n'
            '- NQA-2443A 16PORT SENSOR LAN SWITCH UNIT : 1 EA'
        ),
        'manual': 'B-23_DATA BOOKLETS (MACHINERY PARTICULAR LIST).pdf',
        'pg': 47
    },
    {
        'row': 113,
        'mach': 'ECDIS',
        'maker': 'JRC',
        'model': 'JAN-9201',
        'sno': 'NA',
        'spec': (
            'NDC-1590 ECDIS CENTRAL CONTROL UNIT : 1 EA\n'
            '- NCE-5605 ECDIS TRACKBALL OPERATION UNIT : 1 EA\n'
            '- NBD-913 ECDIS POWER SUPPLY UNIT : 1 EA\n'
            '- NWZ-208 ECDIS MONITOR UNIT : 1 EA\n'
            '- NCE-5625 ECDIS KEYBOARD OPERATION UNIT : 1 EA\n'
            'WEIGHT : 80 KG'
        ),
        'manual': 'B-23_DATA BOOKLETS (MACHINERY PARTICULAR LIST).pdf',
        'pg': 47
    },
    {
        'row': 114,
        'mach': 'ECDIS',
        'maker': 'JRC',
        'model': 'JAN-9201',
        'sno': 'NA',
        'spec': (
            'NDC-1590 ECDIS CENTRAL CONTROL UNIT : 1 EA\n'
            '- NCE-5605 ECDIS TRACKBALL OPERATION UNIT : 1 EA\n'
            '- NBD-913 ECDIS POWER SUPPLY UNIT : 1 EA\n'
            '- NWZ-208 ECDIS MONITOR UNIT : 1 EA\n'
            '- NCE-5625 ECDIS KEYBOARD OPERATION UNIT : 1 EA\n'
            'WEIGHT : 80 KG'
        ),
        'manual': 'B-23_DATA BOOKLETS (MACHINERY PARTICULAR LIST).pdf',
        'pg': 47
    },
    {
        'row': 294,
        'mach': 'RADAR (JMR-9282-S)',
        'maker': 'JRC',
        'model': 'JMR-9282-S',
        'sno': 'NA',
        'spec': (
            'NDC-1590 S RADAR CENTRAL CONTROL UNIT : 1 EA\n'
            '- NCE-5605 S RADAR TRACKBALL OPERATION UNIT : 1 EA\n'
            '- NBD-913 S RADAR POWER SUPPLY UNIT : 1 EA\n'
            '- NKE-2632 S RADAR SCANNER UNIT : 1 EA\n'
            '- NWZ-208 S RADAR 26 INCH MONITOR UNIT : 1 EA\n'
            '- NCE-5625 S RADAR KEYBOARD OPERATION UNIT : 1 EA\n'
            'WEIGHT : 200 KG (TOTAL RADAR)'
        ),
        'manual': 'B-23_DATA BOOKLETS (MACHINERY PARTICULAR LIST).pdf',
        'pg': 47
    },
    {
        'row': 295,
        'mach': 'RADAR (JMR-9225-6X)',
        'maker': 'JRC',
        'model': 'JMR-9225-6X',
        'sno': 'NA',
        'spec': (
            'NDC-1590 X RADAR CENTRAL CONTROL UNIT : 1 EA\n'
            '- NCE-5605 X RADAR TRACKBALL OPERATION UNIT : 1 EA\n'
            '- NBD-913 X RADAR POWER SUPPLY UNIT : 1 EA\n'
            '- NKE-1125-6 X RADAR SCANNER UNIT : 1 EA\n'
            '- NJU-85 X RADAR PERFORMANCE MONITOR ON SCANNER UNIT : 1 EA\n'
            '- NWZ-208 X RADAR 26 INCH MONITOR UNIT : 1 EA\n'
            '- NCE-5625 X RADAR KEYBOARD OPERATION UNIT : 1 EA\n'
            'WEIGHT : 200 KG (TOTAL RADAR)'
        ),
        'manual': 'B-23_DATA BOOKLETS (MACHINERY PARTICULAR LIST).pdf',
        'pg': 47
    },

    # Page 48
    {
        'row': 115,
        'mach': 'ECHO SOUNDER',
        'maker': 'JRC',
        'model': 'JFE-700',
        'sno': 'NA',
        'spec': (
            'NJA-710 ES DISPLAY PROCESSING UNIT : 1 EA\n'
            '- NQD-2597 ES MATCHING BOX : 1 EA\n'
            '- NKF-341-G2 ES TRANSDUCER : 1 EA\n'
            'WEIGHT : 30 KG'
        ),
        'manual': 'B-23_DATA BOOKLETS (MACHINERY PARTICULAR LIST).pdf',
        'pg': 48
    },
    {
        'row': 177,
        'mach': 'DGPS',
        'maker': 'JRC',
        'model': 'JLR-8400',
        'sno': 'NA',
        'spec': (
            'NWZ-4620 DGPS DISPLAY UNIT : 2 EA\n'
            '- JLR-4350 DGPS SENSOR : 2 EA\n'
            '- NQA-4351 DGPS OUTPUT BUFFER : 2 EA\n'
            '- HBD-904 DGPS POWER SUPPLY UNIT : 2 EA\n'
            '- NCZ-1663 DGPS SELECT SWITCH : 1 EA\n'
            '- NKG-104 PRINTER : 1 EA\n'
            '- NQE-7700A DGPS JUNCTION BOX : 4 EA\n'
            'WEIGHT : 25 KG'
        ),
        'manual': 'B-23_DATA BOOKLETS (MACHINERY PARTICULAR LIST).pdf',
        'pg': 48
    },
    {
        'row': 356,
        'mach': 'SPEED LOG',
        'maker': 'JRC',
        'model': 'JLN-740N',
        'sno': 'NA',
        'spec': (
            'NWZ-4640 SL MAIN DISPLAY UNIT : 1 EA\n'
            '- CGC-300B EXTERNAL BUZZER : 1 EA\n'
            '- CQD-10 JUNCTION BOX : 1 EA\n'
            '- NQA-7040 DISTRIBUTION PROCESSOR : 1 EA\n'
            '- NJC-70S SIGNAL PROCESSOR : 1 EA\n'
            '- NWZ-650SDR COLOR REMOTE DISPLAY : 1 EA\n'
            '- NKF-531E-04 TRANSDUCER : 1 EA\n'
            '- NCM-227 SL DIMMER UNIT : 1 EA\n'
            'WEIGHT : 65 KG'
        ),
        'manual': 'B-23_DATA BOOKLETS (MACHINERY PARTICULAR LIST).pdf',
        'pg': 48
    },
    {
        'row': 467,
        'loc_code': None,
        'loc_desc': 'SATELLITE LOG',
        'mach': 'SATELLITE LOG',
        'sys_code': None,
        'maker': 'JRC',
        'model': 'JLN-720',
        'sno': 'NA',
        'spec': (
            'NNN-21 GPS SENSOR UNIT : 1 EA\n'
            '- NQA-7010 DISTRIBUTION PROCESSOR : 1 EA\n'
            '- NWZ-510SDG MAIN DISPLAY UNIT : 1 EA\n'
            '- NQE-7720 JUNCTION BOX : 1 EA\n'
            'WEIGHT : 22 KG'
        ),
        'manual': 'B-23_DATA BOOKLETS (MACHINERY PARTICULAR LIST).pdf',
        'pg': 48
    },

    # Page 49
    {
        'row': 28,
        'mach': 'AIS',
        'maker': 'JRC',
        'model': 'JHS-183',
        'sno': 'NA',
        'spec': (
            'NTE-183 AIS TRANSPONDER : 1 EA\n'
            '- NCM-983 AIS CONTROLLER : 1 EA\n'
            '- NBD-577C AIS POWER SUPPLY UNIT : 1 EA\n'
            '- HAI-150 PILOT PLUG & RECEPTACLE : 1 EA\n'
            'WEIGHT : 15 KG'
        ),
        'manual': 'B-23_DATA BOOKLETS (MACHINERY PARTICULAR LIST).pdf',
        'pg': 49
    },
    {
        'row': 81,
        'mach': 'CONNING',
        'maker': 'JRC',
        'model': 'JAN-9202',
        'sno': 'NA',
        'spec': (
            'NDC-1590A CENTRAL CONTROL UNIT : 1 EA\n'
            '- NCE-5605 TRACKBALL OPERATION UNIT : 1 EA\n'
            '- NBD-913 POWER SUPPLY UNIT : 1 EA\n'
            '- NWZ-208 26 INCH MONITOR UNIT : 1 EA\n'
            '- CWB-1620 LCD HOOD : 1 EA\n'
            '- NCE-5625 KEYBOARD OPERATION UNIT : 1 EA\n'
            'WEIGHT : 28 KG'
        ),
        'manual': 'B-23_DATA BOOKLETS (MACHINERY PARTICULAR LIST).pdf',
        'pg': 49
    },
    {
        'row': 298,
        'mach': 'GMDSS SYSTEM',
        'maker': 'JRC',
        'model': 'JSS-2150',
        'sno': 'NA',
        'spec': (
            'GMDSS CONSOLE : 1 EA\n'
            '- NTD-2150 MF/HF TRANSCEIVER (ON NCU-531A) : 1 EA\n'
            '- NCM-2150 MF/HF CONTROLLER (ON NCU-531A) : 1 EA\n'
            '- NQW-261 MF/HF HANDSET (ON NCU-531A) : 1 EA\n'
            '- NBD-2150 MF/HF POWER SUPPLY UNIT (ON NCU-531A) : 1 EA\n'
            '- NBB-724 MF/HF BATTERY CHARGER (ON NCU-531A) : 1 EA\n'
            '- NFC-2150 MF/HF ANTENNA TUNER : 1 EA\n'
            '- NQD-2253 MF/HF JUNCTION BOX : 1 EA\n'
            '- NAW-60 MF/HF WHIP ANTENNA : 1 EA\n'
            '- JQD-69C MF/HF JOINT BOX : 1 EA\n'
            '- AT100DS-H MF/HF SELF SUPPORTED ANTENNA : 1 EA\n'
            '- TH-19/1.2 ANTENNA WIRE : 1 EA\n'
            'WEIGHT : 440 KG'
        ),
        'manual': 'B-23_DATA BOOKLETS (MACHINERY PARTICULAR LIST).pdf',
        'pg': 49
    }
]

for item in data_updates:
    r = item['row']
    if 'loc_code' in item:
        ws.cell(r, 1, item['loc_code'])
    if 'loc_desc' in item:
        ws.cell(r, 2, item['loc_desc'])
    ws.cell(r, 3, item['mach'])
    if 'sys_code' in item:
        ws.cell(r, 4, item['sys_code'])
    
    # Formula in Column 5: =_xlfn.CONCAT(C...," ",F...," ",G...," ",L...)
    ws.cell(r, 5, f'=_xlfn.CONCAT(C{r}," ",F{r}," ",G{r}," ",L{r})')
    
    ws.cell(r, 6, item['maker'])
    ws.cell(r, 7, item['model'])
    ws.cell(r, 8, item['sno'])
    ws.cell(r, 9, item['spec'])
    ws.cell(r, 10, item['manual'])
    ws.cell(r, 11, item['pg'])
    ws.cell(r, 12, '(203)')
    print(f'Successfully prepared Row {r}: Pg {item["pg"]}, {item["mach"]}')

wb.save('VL_IRENE WISDOM.xlsx')
print('Successfully saved VL_IRENE WISDOM.xlsx!')
