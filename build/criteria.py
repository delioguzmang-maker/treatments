# Crash criteria per countermeasure, written the way they are entered in the
# SMS / AASHTOWare Safety Condition Builder (field names and dropdown labels).
# Row numbers match the Countermeasures sheet.

RD_EXCL = ("AND Probable Cause ≠ Obstruction in Roadway\n"
           "AND Probable Cause ≠ Debris")

CURVE = ("AND (   Road Character = Curve-Level\n"
         "     OR Road Character = Curve-On Grade\n"
         "     OR Road Character = Curve-Hillcrest )")

# row: (area type, location, crash types, traffic control, site conditions,
#       criteria, notes, open item)
CM = {
3: ("Any", "Any", "Speeding-related", "Any", "-",
"""Probable Cause = Exceeded Speed Limit""",
"Too Fast for Conditions left out on purpose (team decision, Jan 2025). Most CMFs in this group are for all crashes on the corridor, so the benefit comes out low.",
"Ask Numetric what 'Speeding Related' contains. If it leaves out Too Fast for Conditions, use Speeding Related = Yes instead."),

4: ("Urban", "Any", "Bicycle", "Any", "-",
"""(   Unit Type = Pedalcycle
 OR First Harmful Event = Pedalcycle )""",
"Vulnerable Road User Related also pulls in pedestrians, so it is not used here. Pedalcycle is code 26 in the SMS (25 on the new TR-310).",
""),

5: ("Urban / Suburban", "Intersection", "Pedestrian", "Any", "-",
"""Pedestrian Related = Yes
AND Intersection Related = Yes""",
"Bicyclists dropped: all three CMFs are vehicle-pedestrian. CMF 436 is night-only (see Treatments).",
""),

6: ("Urban / Suburban", "Intersection", "Pedestrian", "Signal", "-",
"""Pedestrian Related = Yes
AND Intersection Related = Yes
AND Traffic Control = Traffic Signal""",
"Turning-vehicle filter removed. Both LPI CMFs are for all vehicle-pedestrian crashes at the intersection, not only turning ones.",
"Confirm the dropdown label for signals under Traffic Control."),

7: ("Urban / Suburban", "Midblock", "Pedestrian", "Any", "4+ through lanes",
"""Pedestrian Related = Yes
AND Intersection Related = No
AND Area Type = Urban
AND Through Lanes >= 4""",
"Lanes come from the Roadway data. CMF 2219 (0.29) is for all crashes, not pedestrian crashes.",
""),

8: ("Urban / Suburban", "Midblock", "Pedestrian", "No signal", "Speed limit 35+ or 4+ lanes",
"""Pedestrian Related = Yes
AND Intersection Related = No
AND Traffic Control ≠ Traffic Signal
AND (   Speed Limit >= 35
     OR Through Lanes >= 4 )""",
"PHB and RRFB had identical criteria. Split by speed and lanes following the FHWA STEP guide for uncontrolled crossings. 35-40 mph overlaps on purpose; both are options there.",
"Confirm Speed Limit is available under Roadway."),

9: ("Urban / Suburban", "Midblock", "Pedestrian", "No signal", "Speed limit 40 or less",
"""Pedestrian Related = Yes
AND Intersection Related = No
AND Traffic Control ≠ Traffic Signal
AND Speed Limit <= 40""",
"RRFBs are not recommended on high-speed roads (FHWA STEP). Bicyclists dropped: both CMFs are vehicle-pedestrian.",
"Same Speed Limit check as PHB."),

10: ("Urban", "Segment", "Rear-end, Head-on, Angle, Ped, Bike", "Any", "4 lanes, undivided, AADT 20,000 or less",
"""Area Type = Urban
AND Trafficway = Two-Way, Not Divided
AND Through Lanes = 4
AND AADT <= 20000
AND (   Manner of Collision = Rear End
     OR Manner of Collision = Head On
     OR Manner of Collision = Angle
     OR Pedestrian Related = Yes
     OR Unit Type = Pedalcycle )""",
"AADT limit from the FHWA Road Diet guide. Freeway exclusion dropped: Two-Way, Not Divided already removes them. All three CMFs are for all crashes, so the benefit comes out low.",
"Angle may show as three entries in the dropdown (SMS codes 41, 42, 43). Select all three."),

11: ("Any", "Midblock", "Pedestrian", "Any", "-",
"""Pedestrian Related = Yes
AND Intersection Related = No""",
"Walking-along-the-road filter dropped: the sidewalk CMF (11246) covers all vehicle-pedestrian crashes.",
"If the SMS has a pedestrian action field, add 'walking along roadway' back."),

12: ("Any", "Segment (curve)", "Lane departure", "Any", "Curve",
"""Lane Departure = Yes
AND Junction Type = NON-JUNCTION
""" + CURVE + "\n" + RD_EXCL,
"Changed from Roadway Departure to Lane Departure so head-ons on the curve count; most curve CMFs cover all crashes at the curve. Curve Left / Curve Right do not exist in the SMS - Road Character does.",
"Team: OK with Lane Departure here? 5 of the 9 CMFs are night-only (see Treatments)."),

13: ("Rural", "Segment", "Head-on, Sideswipe opp. direction", "Any", "2 lanes, undivided",
"""Lane Departure = Yes
AND Roadway Departure = No
AND Junction Type = NON-JUNCTION
AND Trafficway = Two-Way, Not Divided
AND Through Lanes = 2
AND Area Type = Rural""",
"Lane Departure minus Roadway Departure leaves Head On + Sideswipe, Opposite Direction, which is what the CMFs measured. Rural added per the meeting; every CMF here is rural.",
""),

14: ("Rural", "Segment", "Run-off-road", "Any", "-",
"""Roadway Departure = Yes
AND Junction Type = NON-JUNCTION
AND Area Type = Rural
""" + RD_EXCL,
"Same crash group as SafetyEdge and Wider Edge Lines. That is fine: they are alternative fixes for the same crashes and AASHTOWare ranks them by B/C.",
""),

15: ("Any", "Segment", "Cross-median, Head-on, Sideswipe opp., median ROR / fixed object", "Any", "Divided, no barrier, AADT over 20,000",
"""Junction Type = NON-JUNCTION
AND Trafficway = Two-Way, Divided, Unprotected Median
AND AADT > 20000
AND (   Manner of Collision = Head On
     OR Manner of Collision = Sideswipe, Opposite Direction
     OR Sequence of Events = Cross Median/Center
     OR Sequence of Events = Ran off Road Left
     OR First Harmful Event Location = Median )
AND First Harmful Event Location ≠ Roadside
AND First Harmful Event Location ≠ Outside Trafficway
AND Crash Harmful Event ≠ Median Barrier""",
"Trafficway drops undivided roads (centerline crashes), one-way ramps and roads that already have a barrier (I-20 crash 23239996). First Harmful Event Location = Median brings in every object in the median - piers, abutments, walls, poles, ditches - in one line. 'First Harmful Event ≠ Ran off Road Right' replaced with Location ≠ Roadside so a driver who goes right, overcorrects and crosses the median stays in. AADT > 20,000 matches AASHTO RDG Fig. 6-1.",
"Median width (30 ft or less per RDG) is not in the crash data - check against inventory. Wrong-way head-ons can't be removed with crash-level fields. CMF 7040 (0.03) is cross-median only."),

16: ("Any", "Segment (curve)", "Run-off-road, fixed object, rollover", "Any", "Curve",
"""Roadway Departure = Yes
AND Junction Type = NON-JUNCTION
""" + CURVE + """
AND (   First Harmful Event Location = Roadside
     OR First Harmful Event Location = Shoulder )
""" + RD_EXCL,
"Object list replaced by First Harmful Event Location. The old codes were wrong in the SMS: Tree is 60, Utility Pole is 61, and 59 is Other (Wall, Bldg, Tunnel). Median crashes go to Median Barriers so nothing is counted twice.",
"CMF 7179 is for median slopes on freeways, not curves."),

17: ("Any", "Segment", "Run-off-road, fixed object", "Any", "-",
"""Roadway Departure = Yes
AND Junction Type = NON-JUNCTION
AND (   First Harmful Event Location = Roadside
     OR First Harmful Event Location = Shoulder )
AND Crash Harmful Event ≠ Guardrail Face
AND Crash Harmful Event ≠ Guardrail End
AND Crash Harmful Event ≠ Median Barrier
""" + RD_EXCL,
"Existing-barrier hits excluded by name. Old codes 41/42/44 were wrong in the SMS (41 = Bridge Parapet End, 42 = Bridge Pier, 44 = Culvert). 'Number of Vehicles = 1' dropped - Roadway Departure is already single-vehicle.",
"Both CMFs are night-only, KA / KAB."),

18: ("Rural", "Segment", "Run-off-road", "Any", "-",
"""Roadway Departure = Yes
AND Junction Type = NON-JUNCTION
AND Area Type = Rural
""" + RD_EXCL,
"Same group as Shoulder Rumble Strips on purpose (see row 14).",
""),

19: ("Rural", "Segment", "Run-off-road", "Any", "-",
"""Roadway Departure = Yes
AND Junction Type = NON-JUNCTION
AND Area Type = Rural
""" + RD_EXCL,
"Four of the five CMFs are for all crashes, so the benefit comes out low. CMF 4739 is daytime only.",
""),

20: ("Any", "Intersection", "Angle, Rear-end", "Signal", "-",
"""Intersection Related = Yes
AND Traffic Control = Traffic Signal
AND (   Manner of Collision = Angle
     OR Manner of Collision = Rear End )""",
"",
""),

21: ("Any", "Intersection or driveway", "Angle, Rear-end, Head-on", "Any", "-",
"""(   Intersection Related = Yes
 OR Junction Type = Driveway )
AND (   Manner of Collision = Angle
     OR Manner of Collision = Rear End
     OR Manner of Collision = Head On )""",
"Intersection Related does not include driveways, so Driveway is added by hand. Pedestrian/bike exclusion dropped: those crashes are Non Collision in Manner of Collision, so the MOC line already removes them.",
"CMF 10375 is for non-intersection crashes."),

22: ("Any", "Intersection", "Rear-end, Angle", "Any", "-",
"""Intersection Related = Yes
AND (   Manner of Collision = Rear End
     OR Manner of Collision = Angle )""",
"'Number of Vehicles >= 2' dropped - Rear End and Angle already mean two vehicles.",
"Two CMFs (8431, 8499) are right-turn crashes only."),

23: ("Any", "Intersection", "Angle, Rear-end, Head-on", "Any", "-",
"""Intersection Related = Yes
AND (   Manner of Collision = Angle
     OR Manner of Collision = Rear End
     OR Manner of Collision = Head On )""",
"",
""),

24: ("Any", "Intersection", "Angle, Head-on", "Any", "-",
"""Intersection Related = Yes
AND (   Manner of Collision = Angle
     OR Manner of Collision = Head On )""",
"",
""),

25: ("Any", "Intersection", "Angle, Head-on, left turn", "Signal", "-",
"""Intersection Related = Yes
AND Traffic Control = Traffic Signal
AND (   Manner of Collision = Angle
     OR Manner of Collision = Head On )
AND Vehicle Maneuver = Turning Left""",
"Turning Left is a unit field; '=' works fine (any unit turning left).",
"Confirm the name of the unit movement field and the 'Turning Left' label."),

26: ("Any", "Intersection", "Angle, Head-on", "Any", "-",
"""Intersection Related = Yes
AND Junction Type ≠ Traffic Circle
AND (   Manner of Collision = Angle
     OR Manner of Collision = Head On )""",
"Existing traffic circles removed. Most roundabout CMFs are for all crashes, so the benefit comes out low.",
""),

27: ("Any", "Intersection", "Angle", "Stop", "-",
"""Intersection Related = Yes
AND Traffic Control = Stop Sign
AND Manner of Collision = Angle""",
"",
"Confirm the dropdown label for stop signs."),

28: ("Rural", "Intersection", "Angle", "Stop", "-",
"""Intersection Related = Yes
AND Traffic Control = Stop Sign
AND Manner of Collision = Angle
AND Area Type = Rural""",
"",
""),

29: ("Any", "Intersection", "All", "Stop", "T, Y or four-way",
"""Traffic Control = Stop Sign
AND (   Junction Type = T-Intersection
     OR Junction Type = Y-Intersection
     OR Junction Type = Four-Way Intersection )""",
"Signalized intersections are out because of the Stop Sign line.",
"CMF 8970 is from signalized intersections - doesn't belong in this group."),

30: ("Any", "Intersection", "Rear-end, Angle (red-light running)", "Signal", "-",
"""Intersection Related = Yes
AND Traffic Control = Traffic Signal
AND (   Manner of Collision = Rear End
     OR Manner of Collision = Angle )
AND Probable Cause = Disregarded Sign/Signal""",
"The SC code list has no 'Ran Red Light'; Disregarded Sign/Signal is the closest.",
"Both CMFs are for all crashes, so this filter makes the benefit very low. Team decision."),

31: ("Any", "Any", "Night, all except rear-end", "Any", "-",
"""(   Light Condition = Dark (No Lights)
 OR Light Condition = Dark (Street Lamps Not Lit)
 OR Light Condition = Dark (Lighting Unspecified)
 OR Light Condition = Dark (Street Lamp Lit) )
AND Manner of Collision ≠ Rear End""",
"SMS light codes are 4-7, not the new-form 04-06 (in the SMS 5 = Street Lamp Lit and 6 = Lamps Not Lit). Take out 'Street Lamp Lit' to look only at roads with no lighting.",
"CMF 7784 is rear-end only, but rear-ends are excluded. Drop one or the other."),

32: ("Any", "Any", "Wet road: run-off-road or curve", "Any", "Wet pavement",
"""Road Surface Condition = Wet
AND (   Roadway Departure = Yes
     OR Road Character = Curve-Level
     OR Road Character = Curve-On Grade
     OR Road Character = Curve-Hillcrest )
""" + RD_EXCL,
"Ice and slush dropped: none of the 8 CMFs measured ice. Fixed a parenthesis that never closed in the old version.",
""),
}

# Fit of each treatment's CMF with its countermeasure criteria.
# OK = same crashes. LOW = CMF is for all crash types -> benefit understated.
# HIGH = CMF is for a narrower group than the criteria -> benefit overstated.
# CHECK = different crashes / facility; needs a decision.
FIT = {
 3: "LOW", 4: "LOW", 5: "LOW", 6: "LOW", 7: "LOW",
 8: ("HIGH", "Single-vehicle crashes only"), 9: "LOW",
 10: ("HIGH", "Single-vehicle, PDO, off-peak only"), 11: "LOW",
 12: "OK", 13: "LOW", 14: "OK", 15: "OK", 16: "LOW", 17: "OK", 18: "OK", 19: "LOW",
 20: "OK", 21: ("HIGH", "Night pedestrian crashes only"), 22: "OK",
 23: "OK", 24: "OK", 25: "OK", 26: "OK", 27: "LOW",
 28: "OK", 29: "OK", 30: "OK", 31: "OK", 32: "OK",
 33: "LOW", 34: "LOW", 35: "LOW", 36: "OK",
 37: ("HIGH", "Night crashes only"), 38: ("CHECK", "Dropped 8/2026"), 39: "LOW",
 40: ("HIGH", "Night crashes only"), 41: "LOW", 42: ("HIGH", "Night crashes only"),
 43: ("HIGH", "Night crashes only"), 44: ("HIGH", "Night crashes only"),
 45: ("HIGH", "Night crashes only"),
 46: "OK", 47: ("CHECK", "Not used"), 48: ("CHECK", "Not used"),
 49: ("OK", "CMF covers all lane departure"), 50: "OK", 51: "OK", 52: "OK",
 53: "LOW", 54: "OK",
 55: ("HIGH", "Cross-median crashes only; criteria also has median rollovers and fixed objects"),
 56: ("CHECK", "Study's 'target crashes' not defined in the Clearinghouse entry"),
 57: "OK", 58: "OK", 59: ("CHECK", "Median slope on freeways, not roadside at curves"),
 60: ("HIGH", "Night run-off-road only"), 61: ("HIGH", "Night run-off-road only"),
 62: "LOW", 63: "OK", 64: "LOW", 65: "LOW", 66: "LOW",
 67: ("CHECK", "Daytime crashes only"), 68: "LOW",
 69: "LOW", 70: ("CHECK", "Not used"), 71: ("CHECK", "Not used"),
 72: ("CHECK", "Non-intersection crashes; criteria is intersection/driveway"),
 73: ("HIGH", "Rear-end only"), 74: "LOW", 75: ("HIGH", "Head-on only"),
 76: "LOW", 77: ("HIGH", "Right-turn crashes only"), 78: ("HIGH", "Right-turn crashes only"),
 79: "LOW", 80: "LOW", 81: "LOW",
 82: "LOW", 83: "LOW", 84: "LOW", 85: ("HIGH", "Rear-end only"), 86: "LOW", 87: "LOW",
 88: ("HIGH", "Angle only"),
 89: "LOW", 90: "LOW", 91: "LOW", 92: ("HIGH", "Angle only"), 93: "LOW",
 94: ("HIGH", "Head-on left-turn only"),
 95: "OK", 96: "LOW", 97: ("CHECK", "Rear-end; criteria is angle / head-on"), 98: "OK", 99: "OK",
 100: "OK",
 101: "LOW", 102: "LOW", 103: "LOW", 104: "LOW", 105: "LOW", 106: "LOW", 107: "LOW", 108: "LOW",
 109: "OK",
 110: "LOW", 111: "LOW", 112: "LOW", 113: "LOW", 114: "LOW", 115: "LOW",
 116: "OK", 117: ("HIGH", "Angle only; criteria is all crashes"),
 118: ("HIGH", "Angle only; criteria is all crashes"),
 119: ("CHECK", "Signalized intersections; criteria is stop-controlled"),
 120: ("HIGH", "Night crashes only"),
 121: "LOW", 122: "LOW",
 123: ("HIGH", "Night pedestrian crashes only"), 124: "OK", 125: "LOW",
 126: ("CHECK", "Rear-end only; criteria excludes rear-end"),
 127: ("HIGH", "Rural intersection angle crashes only"),
 128: "LOW", 129: "LOW", 130: "OK", 131: "OK", 132: "OK", 133: "OK", 134: "OK", 135: "OK",
}

FIT_TEXT = {
 "OK": "OK",
 "LOW": "Understates",
 "HIGH": "Overstates",
 "CHECK": "Check",
}
FIT_DEFAULT_WHY = {
 "OK": "",
 "LOW": "CMF is for all crash types",
 "HIGH": "",
 "CHECK": "",
}
