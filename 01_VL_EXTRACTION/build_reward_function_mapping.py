import openpyxl

wb_fun = openpyxl.load_workbook('01_VL_EXTRACTION/C.V. IRENES REWARD_FUN.xlsx', data_only=True)
ws_fun = wb_fun['Allocation Sheet']

valid_funcs = set()
for r in range(12, ws_fun.max_row + 1):
    f = ws_fun.cell(r, 9).value
    if f and f != 'Folder':
        valid_funcs.add(str(f).strip())

def get_function_for_reward_row(row_idx, loc_code, loc_desc, sys_desc, maker, model, particulars):
    ld = str(loc_desc or '').upper().strip()
    sd = str(sys_desc or '').upper().strip()
    lc = str(loc_code or '').upper().strip()
    maker_u = str(maker or '').upper().strip()
    model_u = str(model or '').upper().strip()
    part_u = str(particulars or '').upper().strip()

    # 1. Loading Computer
    if 'LOADING COMPUTER' in ld or 'LCMP' in lc:
        return 'MEASUREMENT INSTRUMENTS', 'LAODING COMPUTER'

    # 2. ICCP & MGPS
    if 'I.C.C.P' in ld or 'ICCP' in ld or 'ICCP' in lc:
        return 'ICCP SYSTEM', 'ICCP'
    if 'ANTI-FOULING' in ld or 'MGPS' in ld or 'ANTIF' in lc:
        return 'M.G.P.S, I.C.C.P., ANODES, ANTI-FOULING', 'MGPS'

    # 3. Anchor & Chain
    if 'ANCHOR CHAIN' in ld or 'ANCCHAIN' in lc:
        return 'ANCHOR CHAIN', 'ANCHOR CHAIN'
    if 'ANCHOR' in ld or 'ANCHOR' in lc:
        return 'ANCHOR&MOORING WINDLASS', 'ANCHOR'

    # 4. Steering Gear (ensure Fans are excluded)
    if ('STEERING GEAR' in ld or 'SGR' in lc) and 'FAN' not in ld:
        return 'STEERING SYSTEM', 'STEERING GEAR'

    # 5. Mooring Winch & Windlass
    if 'MOORING WINCH' in ld or 'YMRWC' in lc:
        return 'MOORING WINCH', 'MOORING SYSTEM'
    if 'WINDLASS' in ld or 'YWDLS' in lc:
        return 'WINDLASS', 'WINCH & WINDLASS'

    # 6. Bow Thruster (exclude Fans, Starters, Transformers)
    if 'BOW THRUSTER' in ld or 'BOWTH' in lc:
        if 'TRANSFORMER' in ld:
            return 'ELECTRICAL SYSTEM', 'POWER & LIGHTING TRANSFORMER'
        if 'PANEL' in ld or 'STARTER' in ld or 'BTCPSTAR' in lc:
            return 'PROPELLER, THRUSTER, STERN TUBE, SHAFTING', 'BOW THRUSTER'
        if 'FAN' in ld:
            return 'HEATING, VENTILATION & AIR CONDITIONING', 'VENTILATION FAN'
        return 'PROPELLER, THRUSTER, STERN TUBE, SHAFTING', 'BOW THRUSTER'

    # 7. Davits & Cranes
    if 'F.O HOSE DAVIT' in ld or 'FOHDAV' in lc:
        return 'DAVIT', 'F.O HOSE DAVIT'
    if 'MONORAIL' in ld or 'MONHCR' in lc:
        return 'CRANES', 'MONORAIL HOIST CRANE'
    if 'LIFE BOAT DAVIT' in ld or 'LIFEBOAT DAVIT' in ld or 'LBDS' in lc:
        return 'LIFE BOAT DAVITS', 'LIFE BOAT DAVIT'
    if 'RESCUE AND LIFERAFT DAVIT' in ld or 'RESLFDAV' in lc or 'RESCUE BOAT DAVIT' in ld:
        return 'LIFE BOAT DAVITS', 'RESCUE BOAT DAVIT'
    if 'E/R CRANE' in ld or 'ENGINE ROOM CRANE' in ld or 'ERCR' in lc or 'CRENG' in lc:
        return 'CRANES', 'E/R OVERHEAD CRANE'

    # 8. Boats & Rafts
    if 'LIFEBOAT' in ld or 'LIFE BOAT' in ld or 'LIFBP' in lc:
        return 'LIFE BOATS', 'LIFE BOAT'
    if 'RESCUE BOAT' in ld or 'LRSCBO' in lc:
        return 'LIFE BOATS', 'RESCUE BOAT'
    if 'LIFERAFT' in ld or 'LIFE RAFT' in ld or 'LIFERA' in lc:
        return 'LIFE RAFTS', 'LIFE RAFT'

    # 9. Ladders (must NOT trigger on AUTO PILOT)
    if 'ACCOMMOD' in ld or 'ALRP' in lc or 'ALRS' in lc:
        return 'LIFTING APPLIANCES, DERRICKS, LADDERS', 'ACCOMMODATION LADDER'
    if 'PILOT LADDER' in ld or 'PILOT SLANT' in ld or 'PISLAD' in lc:
        return 'LIFTING APPLIANCES, DERRICKS, LADDERS', 'PILOT LADDER'

    # 10. Cargo Hatch Cover
    if 'HATCH COVER' in ld or 'CAHACOV' in lc:
        return 'HOLDS', 'CARGO HATCH COVER'

    # 11. Fans & Ventilation (All Supply, Exhaust, Vent Fans)
    if 'FAN' in ld or 'VENT' in ld:
        return 'HEATING, VENTILATION & AIR CONDITIONING', 'VENTILATION FAN'

    # 12. Galley & Laundry
    if 'GALLEY' in ld or 'LAUNDRY' in ld or 'GLE' in lc:
        return 'GALLEY', 'GALLEY & LAUNDRY EQUIPMENT'

    # 13. Window Wiper & CVS
    if 'CLEAR VIEW' in ld or 'CVS' in ld or 'WINDOW WIPER' in ld or 'WIPER' in ld or 'WINWIP' in lc:
        return 'NAVIGATION EQUIPMENT', 'WINDOW WIPER & CLEAR VIEW SCREEN'

    # 14. Air Conditioning & Refrigeration
    if 'AIR CONDITIONING UNIT' in ld or 'AIR HANDLING UNIT' in ld or 'A/C PLANT' in ld or 'ACPLACO' in lc or 'AHU' in lc or 'AC1' in lc or 'AC2' in lc:
        return 'AIR CONDITION', 'AIR CONDITIONING PLANT'
    if 'AIR CONDITION FOR ENGINE CONTROL ROOM' in ld or ('ECR' in ld and 'AIR' in ld) or 'ECRF' in lc:
        return 'AIR CONDITION', 'ECR PACKAGED AC'
    if 'REFRIGERATING' in ld or 'PROVISION REF' in ld or 'PROREF' in lc:
        return 'REFRIGERATION', 'PROVISION REFRIGERATING PLANT'
    if 'ROOM UNIT COOLER' in ld or ('COOLER' in ld and ('FISH' in ld or 'MEAT' in ld or 'VEGETABLES' in ld)):
        return 'REFRIGERATION', 'COLD PROVISION CHAMBER'

    # 15. Elevator
    if 'ELEVATOR' in ld or 'CREL' in lc:
        return 'ELEVATOR', 'ELEVATOR'

    # 16. Fire Fighting & Alarms
    if 'CO2' in ld and ('FIRE' in ld or 'EXT' in ld or 'SYSTEM' in ld):
        return 'FIRE FIGHTING', 'CO2 EXTINGUISHING SYSTEM'
    if 'FIRE ALARM' in ld or 'FIRE DETECTION' in ld or 'FIDES' in lc:
        return 'FIRE FIGHTING', 'FIRE ALARM & DETECTION SYSTEM'
    if 'LOCAL FIRE' in ld or 'FIRE FIGHTING' in ld or 'LOFFS' in lc or 'LFFS' in lc:
        return 'FIRE FIGHTING', 'LOCAL FIRE EXTINGUISHING SYSTEM'
    if 'LOOSE FIRE' in ld or 'LOOSEFFA' in lc:
        return 'FIRE FIGHTING', 'LOOSE FIRE FIGHTING APPLIANCE'
    if 'HOSPITAL CALLING' in ld or 'REF. CHAMBER ALARM' in ld or 'HOSPCAL' in lc or 'REFCHALM' in lc:
        return 'FIRE DETECTION & ALARM SYSTEM', 'HOSPITAL & REF CHAMBER ALARM'

    # 17. Valves & Remote Control
    if 'VALVE REMOTE CONTROL' in ld or 'VRCS' in lc:
        return 'HYDRAULIC CONTROL UNIT', 'VALVE REMOTE CONTROL SYSTEM'
    if 'SHIPSIDE VALVES' in ld or 'SHIP SIDE' in ld or 'MAHYDSHV' in lc:
        return 'PIPING, VALVES, FILTERS, EJECTOR, FITTINGS', 'SHIP SIDE V/V & E/R PIPING & SEA CHEST'
    if 'PRESSURE CONTROL VALVE' in ld or 'CONTROL VALVE' in ld:
        return 'VALVES', 'CONTROL VALVE'
    if 'EMERGENCY SHUT-OFF VALVE' in ld or 'SHUT-OFF' in ld:
        return 'VALVES', 'EMERGENCY SHUT-OFF VALVE'

    # 18. Gauging & Monitoring
    if 'LEVEL & DRAFT GAUGING' in ld or 'TANK LEVEL' in ld or 'ELEC. PNEUMATIC TYPE' in sd or 'RELEDGS' in lc:
        return 'TANK LEVEL, GAUGING & MONITORING SYSTEM', 'ELEC. PNEUMATIC TYPE TANK LEVEL GAUGE'
    if 'LEVEL SWITCH' in ld or 'LEVEL SENSOR' in ld or 'ELS' in lc:
        return 'LEVEL INDICATORS', 'LEVEL SWITCH'
    if 'ALARM & MONITORING' in ld or 'AMS' in lc or 'ERAMS' in lc:
        return 'FIRE DETECTION & ALARM SYSTEM', 'ER ALARM AND MONITORING SYSTEM'

    # 19. Shafting & Stern Tube
    if 'STERN TUBE SEAL' in ld or 'STSAFT' in lc or 'STSFWD' in lc:
        return 'PROPELLER, THRUSTER, STERN TUBE, SHAFTING', 'STERN TUBE SEAL'
    if 'STERN TUBE BEARING' in ld or 'STBAFT' in lc or 'STBFWD' in lc:
        return 'PROPELLER, THRUSTER, STERN TUBE, SHAFTING', 'STERN TUBE BEARING'
    if 'INTERMEDIATE SHAFT' in ld or 'PROPELLER SHAFT' in ld or ('SHAFT' in ld and 'BEARING' in ld) or 'INTSHAFT' in lc or 'PROPSHFT' in lc or 'PSHFTNUT' in lc or 'INTSHABE' in lc:
        return 'PROPELLER, THRUSTER, STERN TUBE, SHAFTING', 'INTERMEDIATE SHAFT BEARING'
    if 'PROPELLER' in ld and 'PUMP' not in ld:
        return 'PROPELLER, THRUSTER, STERN TUBE, SHAFTING', 'PROPELLER'
    if 'TOP BRACING' in ld or 'HYDTOPB' in lc:
        return 'MAIN ENGINE', 'MAIN ENGINE TOP BRACING'

    # 20. Engines & Generators
    if 'MAIN ENGINE' in ld or ('M/E' in ld and ('ENGINE' in ld or lc == 'ME')):
        return 'MAIN ENGINE', 'MAIN ENGINE'
    if 'DIESEL GENERATOR' in ld and ('ALTERNATOR' not in ld and 'FAN' not in ld and 'CHOCK' not in ld):
        return 'DIESEL GENERATOR', 'DIESEL GENERATOR ENGINE'
    if 'D/G ENGINE ALTERNATOR' in ld or ('MAIN DIESEL GENERATOR' in sd and 'ALTERNATOR' in ld) or 'DGENGAL' in lc:
        return 'ALTERNATOR', 'SYNCHRONOUS GENERATOR (D/G ALTERNATOR)'
    if 'EMERGENCY GENERATOR' in ld or 'EM\'CY DIESEL GENERATOR' in sd or 'EMEG' in lc:
        return 'EMERGENCY GENERATOR', 'EM\'CY DIESEL GENERATOR SET'
    if 'EMERGENCY ALTERNATOR' in ld or 'EM\'CY GENERATOR SET ALTERNATOR' in sd or 'EARL' in lc:
        return 'EMERGENCY GENERATOR', 'EM\'CY DIESEL GENERATOR ALTERNATOR'

    # 21. Air Compressors & Reservoirs
    if 'AIR COMPR' in ld or 'AIR COMPRESSOR' in ld:
        if 'EM\'CY' in ld or 'EMERGENCY' in ld or 'EACR' in lc:
            return 'AIR COMPRESSOR', 'EMERGENCY AIR COMPRESSOR'
        if 'WORKING' in ld or 'WORKCOMP' in lc:
            return 'AIR COMPRESSOR', 'WORKING AIR COMPRESSOR'
        return 'AIR COMPRESSOR', 'AIR COMPRESSOR'
    if 'AIR RESERV' in ld or 'AIR RESERVOIR' in ld or 'WAR' in lc or 'CAMRS' in lc or 'AXAIRRES' in lc:
        return 'AIR RESERVOIR', 'AIR RESEVOIR'
    if 'AIR DRYER' in ld or 'ADRY' in lc:
        return 'AIR DRYER', 'AIR DRYER'

    # 22. Purifiers
    if 'PURIFIER' in ld and 'HEATER' not in ld and 'PUMP' not in ld:
        if 'L.F.O' in ld or 'H.F.O' in ld or 'FO' in ld or 'LFOPR' in lc:
            return 'PURIFIER', 'LFO PURIFIER'
        return 'PURIFIER', 'MAIN LO PURIFIER'

    # 23. Boilers, Coolers & Heaters
    if 'BOILER' in ld and 'COOLER' not in ld and 'PUMP' not in ld:
        return 'BOILER', 'COMPOSITE BOILER'
    if 'HEAT EXCHANGER' in ld or 'COOLER' in ld or 'CFWC' in lc or 'HTFWCOOL' in lc or 'MGOCOOL' in lc or 'MALOCO' in lc or 'CBMGOCO' in lc or 'DMDNCOOL' in lc:
        return 'HEAT EXCHANGER', 'SHELL & TUBE HEAT EXCHANGER'
    if 'HEATER' in ld or 'PREHEATER' in ld or 'LFOPH' in lc or 'MELOPUH' in lc or 'MJFWP' in lc or 'ELECHEAT' in lc:
        return 'F.W. GENERATOR, HEAT EXCHANGER', 'F.W. GENERATOR'
    if 'FRESH WATER GENERATOR' in ld or 'F.W. GENERATOR' in ld or 'FWGR' in lc:
        return 'F.W. GENERATOR, HEAT EXCHANGER', 'F.W. GENERATOR'

    # 24. Workshop
    if 'LATHE' in ld or 'LEU' in lc:
        return 'WORKSHOP MACHINERY, TOOLS, PORTABLE INSTRUMENTS', 'LATHE MACHINE'
    if 'GRINDER' in ld or 'GRINDING' in ld or 'TOGRIN' in lc:
        return 'WORKSHOP MACHINERY, TOOLS, PORTABLE INSTRUMENTS', 'GRINDING MACHINE'
    if 'DRILLING' in ld or 'DRM' in lc:
        return 'WORKSHOP MACHINERY, TOOLS, PORTABLE INSTRUMENTS', 'DRILLING MACHINE'
    if 'GAS WELDER' in ld or 'TOGWL' in lc:
        return 'WORKSHOP MACHINERY, TOOLS, PORTABLE INSTRUMENTS', 'OXYGEN ACETYLENE GAS WELDING'
    if 'ELECTRIC ARC WELDER' in ld or 'ELECTRIC WELDER' in ld or 'ELARCWEL' in lc:
        return 'ELECTRICAL SYSTEM', 'ELECTRIC WELDING MACHINE'

    # 25. Domestic & Sanitary
    if 'SEWAGE' in ld and 'PUMP' not in ld:
        return 'SEWAGE SYSTEM', 'SEWAGE TREATMENT PLANT'
    if 'F.W. SUPPLY' in ld or 'HYDROPHORE' in ld or 'FWSUPU' in lc:
        return 'HYDROPHORE TANK', 'FW HYDROPHORE SUPPLY UNIT'
    if 'TOILET' in ld or 'VACT' in lc:
        return 'VACUUM TOILET SYSTEM & SANITARY EQUIPMENT', 'VACUUM TOILET'

    # 26. Environmental, Scrubber & Fuel Conditioning
    if 'BALLAST WATER' in ld or 'BWMS' in ld or 'BWTS' in lc:
        return 'BALLAST WATER TREATMENT SYSTEM', 'BWMS PLAN'
    if 'BILGE SEPARATOR' in ld or 'OILY BILGE' in ld or '5 PPM' in ld or '5PPMBILS' in lc:
        return 'OIL SPILL EQUIPMENT', 'OILY BILGE SEPARATOR'
    if 'INCINERATOR' in ld or 'INCINERA' in lc:
        return 'INCINERATORS', 'INCINERATOR'
    if 'F.O.SUPPLY UNIT' in ld or 'F.O SUPPLY' in ld or 'FOSUPU' in lc:
        return 'FUEL SUPPLY SYSTEM', 'FO SUPPLY UNIT ME & AE'
    if 'EXHAUST GAS CLEANING' in ld or 'SCRUBBER' in ld or 'EGCS' in lc:
        return 'SCRUBBER SYSTEM', 'EXHAUST GAS CLEANING SYSTEM'
    if 'HP SCR' in ld:
        return 'MAIN ENGINE', 'MAIN ENGINE HP SCR'
    if 'AUTO L.O. FILTER' in ld or 'FILTER' in ld or 'MELF' in lc:
        return 'MISCELLANEOUS SYSTEMS', 'ME L.O AUTO-BACK FLUSHING FINE FILTER'

    # 27. Pumps
    if 'PUMP' in ld:
        if 'ANTI-HEELING' in ld:
            return 'PUMP', 'ANTI-HEELING PUMP'
        if 'EMERGENCY FIRE' in ld:
            return 'PUMP', 'EMERGENCY FIRE PUMP'
        return 'PUMP', 'ALL PUMPS'

    # 28. Switchboards, Transformers & Electrical
    if 'AMP SYSTEM' in ld or 'AMPSYS' in lc or 'ALTERNATIVE MARINE' in ld:
        return 'ELECTRICAL SYSTEM', 'SHORE CONNECTION SYSTEM'
    if 'SWITCHBOARD' in ld or 'SWITCH BOARD' in ld:
        if 'EMERGENCY' in ld or 'EM\'CY' in ld or 'ESW' in lc:
            return 'SWITCHBOARDS', 'EM\'CY SWITCH BOARD'
        return 'SWITCHBOARDS', 'MAIN SWITCH BOARD'
    if 'DISTRIBUTION BOARD' in ld or 'DNBD' in lc:
        return 'ELECTRICAL SYSTEM', 'DISTRIBUTION BOARD'
    if 'STARTER' in ld or 'PANEL' in ld or 'LOCGRSTP' in lc or 'GRPCPAN' in lc:
        return 'ELECTRICAL SYSTEM', 'GROUP STARTER & FEEDER PANEL'
    if 'STOP SWITCH' in ld or 'EMSTSWBX' in lc:
        return 'ELECTRICAL SYSTEM', 'EMERGENCY STOP SWITCH BOX'
    if 'TRANSFORMER' in ld:
        return 'ELECTRICAL SYSTEM', 'POWER & LIGHTING TRANSFORMER'
    if 'REEFER' in ld or 'REEFMONS' in lc or 'REEFSOCK' in lc:
        return 'CARGO CONTAINER SYSTEM', 'CARGO HOLD'
    if 'SIGNAL LIGHT COLUMN' in ld or 'LIGHT SIGNAL' in ld or 'SIGLTCOL' in lc:
        return 'FIRE DETECTION & ALARM SYSTEM', 'LIGHT SIGNAL COLUMN, ER DEAD-MAN ALARM'
    if 'LIGHT' in ld or 'LAMP' in ld or 'CHTABLT' in lc or 'LFX' in lc or 'PORTALMP' in lc or 'SCSRCHPL' in lc:
        return 'ELECTRICAL SYSTEM', 'LIGHTING FIXTURE'
    if 'RECEPTACLE' in ld or 'PLUG' in ld:
        return 'ELECTRICAL SYSTEM', 'LIGHTING SYSTEM'
    if 'BATTERY CHARGER' in ld or 'BTCR' in lc:
        return 'ELECTRONIC EQ.', 'BATTERY CHARGER & DIST. BOARD'
    if 'BATTERY' in ld:
        return 'ELECTRONIC EQ.', 'BATTERY CHARGER & DIST. BOARD'
    if 'GAUGE BOARD' in ld or 'WHGAUGE' in lc:
        return 'MEASUREMENT INSTRUMENTS', 'GAUGE & CONTROL SYSTEM'

    # 29. Instrumentation & Automation
    if 'HORSEPOWER METER' in ld or 'HORSE POWER' in ld or 'SHAHOMET' in lc:
        return 'MEASUREMENT INSTRUMENTS', 'ME HORSE POWER METER'
    if 'WING CONSOLE' in ld or 'BRIWICON' in lc:
        return 'E/R CONSOLE', 'BRIDGE WING CONTROL CONSOLE'
    if 'BRIDGE CONTROL CONSOLE' in ld or 'ENGINE CONTROL CONSOLE' in ld or 'ECC' in lc:
        return 'E/R CONSOLE', 'ENGINE CONTROL CONSOLE'
    if 'SHIP\'S COMPUTER' in ld or 'PERFORMANCE SYSTEM' in sd or 'ISS' in sd or 'SHIPCOMS' in lc:
        return 'MEASUREMENT INSTRUMENTS', 'INTEGRATED MONITORING AND CONTROL SYSTEM'
    if 'CCTV' in ld or 'CCTVS' in lc:
        return 'ELECTRONIC EQ.', 'C.C.T.V.'
    if 'EARTHING' in ld or 'GROUNDING' in ld or 'SED' in lc:
        return 'ELECTRONIC EQ.', 'SHAFT EARTHING DEVICE'

    # 30. Navigation & Communication
    if 'RADAR' in ld or 'NARADS' in lc or 'NARADX' in lc:
        if 'TRANSPONDER' in ld or 'SART' in ld:
            return 'NAVIGATION EQUIPMENT', 'SART'
        return 'NAVIGATION EQUIPMENT', 'RADAR TRANSPONDER'
    if 'BRIDGE INTERFACE' in ld or 'BRIDGINT' in lc:
        return 'NAVIGATION EQUIPMENT', 'CONNING DISPLAY'
    if 'GPS' in ld or 'DGPS' in ld or 'NGPS' in lc:
        return 'NAVIGATION EQUIPMENT', 'GPS NAVIGATOR'
    if 'SATELLITE LOG' in ld or 'SPEED LOG' in ld or 'SATLOG' in lc or 'SPLG' in lc:
        return 'NAVIGATION EQUIPMENT', 'DOPPLER SPEED LOG'
    if 'MF/HF' in ld or 'GMDSS' in ld or 'MFHFRADE' in lc:
        return 'COMMUNICATIONS', 'MF HF TRANSRECEIVER'
    if 'AIS' in ld:
        return 'NAVIGATION EQUIPMENT', 'AIS'
    if 'CONNING' in ld or 'CONDISPL' in lc:
        return 'NAVIGATION EQUIPMENT', 'CONNING DISPLAY'
    if 'INM C' in ld or 'INMARSAT' in ld or 'INMC' in lc:
        return 'NAVIGATION EQUIPMENT', 'INMARSAT-C'
    if 'NAVTEX' in ld:
        return 'NAVIGATION EQUIPMENT', 'NAVTEX RECEIVER'
    if 'EPIRB' in ld or 'SATEPIRB' in lc:
        return 'NAVIGATION EQUIPMENT', 'EPIRB'
    if 'TWO-WAY VHF' in ld or 'PORTABLE VHF' in sd or 'TWVHFRN' in lc:
        return 'COMMUNICATIONS', '2 WAY VHF'
    if 'VHF' in ld or 'VHFRAD' in lc:
        return 'COMMUNICATIONS', 'VHF'
    if 'VOYAGE DATA' in ld or 'VDR' in ld:
        return 'NAVIGATION EQUIPMENT', 'VDR'
    if 'WEATHER FAX' in ld or 'FAX' in ld or 'WEAFAX' in lc:
        return 'NAVIGATION EQUIPMENT', 'WEATHER FACSIMILE RECEIVER'
    if 'AUTOPILOT' in ld or 'AUTO PILOT' in ld or 'AP' == lc:
        return 'NAVIGATION EQUIPMENT', 'AUTO PILOT'
    if 'GYRO' in ld or 'GC' == lc:
        return 'NAVIGATION EQUIPMENT', 'GYROCOMPASS'
    if 'MAGNETIC COMPASS' in ld or 'MACO' == lc:
        return 'NAVIGATION EQUIPMENT', 'MAGNETIC COMPASS'
    if 'ECDIS' in ld:
        return 'NAVIGATION EQUIPMENT', 'ECDIS'
    if 'ECHO SOUNDER' in ld or 'ES' == lc:
        return 'NAVIGATION EQUIPMENT', 'ECHO SOUNDER'
    if 'BNWAS' in ld or 'BRIDGE NAVIGATION WATCH' in ld:
        return 'NAVIGATION EQUIPMENT', 'BRIDGE WATCH ALARM SYSTEM'
    if 'RUDDER ANGLE' in ld or 'RUDANGIN' in lc:
        return 'RUDDER', 'RUDDER ANGLE INDICATOR'
    if 'ANEMOMETER' in ld or 'AMAS' in lc:
        return 'NAVIGATION EQUIPMENT', 'ANEMOMETER & ANEMOSCOPE'
    if 'WHISTLE' in ld or 'WHI' == lc:
        return 'WHISTLES', 'WHISTLE'
    if 'PUBLIC ADDRESS' in ld or 'PA SYSTEM' in ld or 'PAS' == lc:
        return 'COMMUNICATIONS', 'COMMUNICATION SYSTEM'
    if 'TELEPHONE' in ld or 'TEL' in lc:
        return 'COMMUNICATIONS', 'COMMUNICATION SYSTEM'
    if 'NETWORK' in ld or 'AERIAL' in ld or 'IRIDIUM' in ld or 'V-SAT' in ld or 'VSAT' in ld or 'UHF' in ld or 'SHIPNETW' in lc or 'IRIDSYS' in lc or 'COMAESYS' in lc or 'VOIPAUTS' in lc or 'UHFCOMS' in lc:
        return 'COMMUNICATIONS', 'COMMUNICATION SYSTEM'
    if 'CLOCK' in ld or 'MARCLOS' in lc:
        return 'COMMUNICATIONS', 'COMMUNICATION SYSTEM'

    return None, None
