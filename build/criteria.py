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
"Check whether Junction Type has interchange or ramp values: freeway crashes inside an interchange may not be NON-JUNCTION. Median width (30 ft or less per RDG) is not in the crash data - check against inventory. Wrong-way head-ons can't be removed with crash-level fields. CMF 7040 (0.03) is cross-median only."),

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


# ----------------------------------------------------------------------------
# Same criteria written on MMUCC 6th edition fields (DOT HS 813 525, Feb 2025),
# for when new-form TR-310 reports reach production. Element names are MMUCC's;
# SC's dropdown labels may differ slightly.

M_RD_EXCL = ("AND Related Factors - Crash Level ≠ Obstruction in Roadway\n"
             "AND First Harmful Event ≠ Other Object (not fixed)")
M_SEGMENT = ("Relation to Junction = Non-Junction, Through Roadway\n"
             "                       or Other Location Within an Interchange Area")
M_CURVE = "AND Roadway Alignment = Curve Left or Curve Right"

# Derived fields rebuilt on MMUCC 6 (what Numetric would need to change).
MMUCC_DERIVED = [
 ("Roadway Departure",
  "Manner of Collision = The First Harmful Event Was Not a Collision With a Motor Vehicle In-Transport\n"
  "AND First Harmful Event ≠ Non-Motorist\n"
  "AND First Harmful Event ≠ Live Animal\n"
  "AND First Harmful Event ≠ Ridden Animal or Animal-Drawn Conveyance",
  "Deer and other animals are one attribute (Live Animal) in MMUCC 6."),
 ("Lane Departure",
  "Roadway Departure = Yes\n"
  "OR Manner of Collision = Front to Front\n"
  "OR Manner of Collision = Sideswipe, Opposite Direction",
  "'Head On' is called Front to Front."),
 ("Intersection Related",
  "Relation to Junction = Intersection or Related",
  "Type of Intersection (C13) gives the shape. Driveways are their own value (Driveway Access or Related)."),
 ("Pedestrian",
  "First Harmful Event = Non-Motorist\n"
  "AND (   Person Type = Pedestrian Walking, Running, Jogging, Hiking, Sitting, Lying\n"
  "     OR Person Type = Pedestrian on Personal Conveyance )",
  "First Harmful Event no longer splits pedestrian and bicycle - Person Type (P5) does."),
 ("Bicyclist",
  "Person Type = Bicyclist OR Person Type = Other Cyclist",
  "Or Non-Motorist Device Type (NM9) = Bicycle / Other Cycle."),
 ("Segment (non-intersection)",
  M_SEGMENT,
  "In MMUCC 6, Non-Junction only covers crashes OUTSIDE an interchange area. Freeway mainline crashes "
  "inside an interchange are Through Roadway; median/shoulder/roadside ones are Other Location Within an "
  "Interchange Area."),
]

# row: (criteria on MMUCC 6 fields, what is different / new options)
MMUCC = {
3: ("Speeding-Related = Yes, Exceeded Speed Limit\n OR Speeding-Related = Yes, Racing",
    "Too Fast for Conditions is its own attribute (D5), so the team's decision maps one to one."),
4: ("Bicyclist = Yes",
    "New option: Non-Motorist Specific Location (NM7) = In Painted Cycle Lane / In Physically Separated Cycle Lane shows whether a bike lane was already there."),
5: ("Pedestrian = Yes\nAND Intersection Related = Yes",
    "New option: Non-Motorist in Crosswalk (NM6) = Yes, Marked / Yes, Unmarked, and Non-Motorist Status (NM2) = Crossing."),
6: ("Pedestrian = Yes\nAND Intersection Related = Yes\nAND Traffic Control Device = Traffic Control Signal",
    "Traffic Control Device (V31) is per vehicle; '=' works. New option: Non-Motorist Traffic Control Device (NM10) = Non-Motorist Crossing Signal - an LPI needs pedestrian signal heads."),
7: ("Pedestrian = Yes\nAND Relation to Junction ≠ Intersection or Related\nAND Area Type = Urban\nAND Through Lanes >= 4",
    "Lanes still from road inventory (V27 counts one direction only on divided roads). New option: NM2 = Crossing."),
8: ("Pedestrian = Yes\nAND Relation to Junction ≠ Intersection or Related\nAND Traffic Control Device ≠ Traffic Control Signal\n"
    "AND (   Motor Vehicle Posted or Statutory Speed Limit >= 35\n     OR Through Lanes >= 4 )",
    "Speed limit is now on the crash report (V24, per vehicle). New option: NM2 = Crossing, NM10 = None."),
9: ("Pedestrian = Yes\nAND Relation to Junction ≠ Intersection or Related\nAND Traffic Control Device ≠ Traffic Control Signal\n"
    "AND Motor Vehicle Posted or Statutory Speed Limit <= 40",
    "Same options as PHB."),
10: ("Area Type = Urban\nAND Median Barrier Presence = Not Applicable (no median)\nAND Trafficway Flow = Two-Way\n"
     "AND Number of Open Lanes = 4\nAND AADT <= 20000\n"
     "AND (   Manner of Collision = Front-to-Rear or Rear-to-Front\n     OR Manner of Collision = Front to Front\n"
     "     OR Manner of Collision = Angle\n     OR Pedestrian = Yes\n     OR Bicyclist = Yes )",
     "Trafficway Flow = Two-Way (not 'With a Continuous Left-Turn Lane') leaves out roads that are already three-lane. On an undivided road V27 counts both directions, so 4 = four-lane undivided."),
11: ("Pedestrian = Yes\nAND Relation to Junction ≠ Intersection or Related",
     "New option: NM2 = Movement Against Traffic / Movement With Traffic - the 'walking along the road' filter becomes possible."),
12: ("Lane Departure = Yes\nAND " + M_SEGMENT + "\n" + M_CURVE + "\n" + M_RD_EXCL,
     "Curve Left / Curve Right exist again (V28, per vehicle). There is no 'Debris' attribute: debris hits are First Harmful Event = Other Object (not fixed)."),
13: ("Lane Departure = Yes\nAND Roadway Departure = No\nAND Relation to Junction = Non-Junction\n"
     "AND Median Barrier Presence = Not Applicable (no median)\nAND Number of Open Lanes = 2\nAND Area Type = Rural",
     "New option: Sequence of Events = Cross Centerline brings in single-vehicle centerline crossings."),
14: ("Roadway Departure = Yes\nAND " + M_SEGMENT + "\nAND Area Type = Rural\n" + M_RD_EXCL,
     "New option: Sequence of Events = Ran Off Roadway Right."),
15: ("" + M_SEGMENT + "\nAND Median Barrier Presence = Median Without a Traffic Barrier\nAND AADT > 20000\n"
     "AND (   Manner of Collision = Front to Front\n     OR Manner of Collision = Sideswipe, Opposite Direction\n"
     "     OR Sequence of Events = Cross Median\n     OR Sequence of Events = Ran Off Roadway Left\n"
     "     OR Location of First Harmful Event = On Median )\n"
     "AND Location of First Harmful Event ≠ On Roadside\nAND Location of First Harmful Event ≠ Non-Trafficway Area",
     "Median Barrier Presence (V26) replaces Trafficway 2/3. Cross Median and Ran Off Roadway Left only exist in Sequence of Events. Without Through Roadway / Other Location Within an Interchange Area every freeway crash inside an interchange drops out. Manner of Collision is only for the FIRST harmful event, so a car that hits a median object and then an opposing car is caught by Sequence of Events, not by Front to Front. Wrong-way drivers: D10 has 'Driving on Wrong Side of Two-Way Trafficway', but it is a driver field, so '≠' won't remove the crash."),
16: ("Roadway Departure = Yes\nAND " + M_SEGMENT + "\n" + M_CURVE +
     "\nAND (   Location of First Harmful Event = On Roadside\n     OR Location of First Harmful Event = On Shoulder )\n" + M_RD_EXCL,
     ""),
17: ("Roadway Departure = Yes\nAND " + M_SEGMENT +
     "\nAND (   Location of First Harmful Event = On Roadside\n     OR Location of First Harmful Event = On Shoulder )\n"
     "AND First Harmful Event ≠ Guardrail Face\nAND First Harmful Event ≠ Guardrail End\n"
     "AND First Harmful Event ≠ Concrete Traffic Barrier\nAND First Harmful Event ≠ Cable Barrier\n" + M_RD_EXCL,
     "MMUCC splits barriers into cable, concrete, guardrail face/end and other."),
18: ("Roadway Departure = Yes\nAND " + M_SEGMENT + "\nAND Area Type = Rural\n" + M_RD_EXCL,
     "New option: Related Factors - Driver Level (D10) = Overcorrecting, which is the edge drop-off crash SafetyEdge targets."),
19: ("Roadway Departure = Yes\nAND " + M_SEGMENT + "\nAND Area Type = Rural\n" + M_RD_EXCL,
     ""),
20: ("Intersection Related = Yes\nAND Traffic Control Device = Traffic Control Signal\n"
     "AND (   Manner of Collision = Angle\n     OR Manner of Collision = Front-to-Rear or Rear-to-Front )", ""),
21: ("(   Intersection Related = Yes\n OR Relation to Junction = Driveway Access or Related )\n"
     "AND (   Manner of Collision = Angle\n     OR Manner of Collision = Front-to-Rear or Rear-to-Front\n"
     "     OR Manner of Collision = Front to Front )", ""),
22: ("Intersection Related = Yes\nAND (   Manner of Collision = Front-to-Rear or Rear-to-Front\n     OR Manner of Collision = Angle )",
     "New option: Vehicle Status Prior to Critical Event (V33) = Turning Right."),
23: ("Intersection Related = Yes\nAND (   Manner of Collision = Angle\n     OR Manner of Collision = Front-to-Rear or Rear-to-Front\n"
     "     OR Manner of Collision = Front to Front )",
     "New option: V33 = Turning Left."),
24: ("Intersection Related = Yes\nAND (   Manner of Collision = Angle\n     OR Manner of Collision = Front to Front )",
     "New option: Median Barrier Presence = Median Without a Traffic Barrier (J-turns and RCUTs need a median). Existing RCUTs are Type of Intersection = Other Intersection Type."),
25: ("Intersection Related = Yes\nAND Traffic Control Device = Traffic Control Signal\n"
     "AND (   Manner of Collision = Angle\n     OR Manner of Collision = Front to Front )\n"
     "AND Vehicle Status Prior to Critical Event = Turning Left", ""),
26: ("Intersection Related = Yes\nAND Type of Intersection ≠ Circular Intersection\n"
     "AND (   Manner of Collision = Angle\n     OR Manner of Collision = Front to Front )", ""),
27: ("Intersection Related = Yes\nAND Traffic Control Device = Stop Sign\nAND Manner of Collision = Angle", ""),
28: ("Intersection Related = Yes\nAND Traffic Control Device = Stop Sign\nAND Manner of Collision = Angle\nAND Area Type = Rural", ""),
29: ("Traffic Control Device = Stop Sign\nAND (   Type of Intersection = T-Intersection\n     OR Type of Intersection = Y-Intersection\n"
     "     OR Type of Intersection = Four-Leg Intersection )",
     "MMUCC adds L-Intersection; left out here."),
30: ("Intersection Related = Yes\nAND Traffic Control Device = Traffic Control Signal\n"
     "AND (   Manner of Collision = Front-to-Rear or Rear-to-Front\n     OR Manner of Collision = Angle )\n"
     "AND Related Factors - Driver Level = Failure to Obey Traffic Control Devices", ""),
31: ("(   Light Condition = Dark - Not Lighted\n OR Light Condition = Dark - Lighted\n OR Light Condition = Dark - Unknown Lighting )\n"
     "AND Manner of Collision ≠ Front-to-Rear or Rear-to-Front",
     "MMUCC has three dark values; the SMS has four."),
32: ("Roadway Surface Condition = Wet\nAND (   Roadway Departure = Yes\n     OR Roadway Alignment = Curve Left\n"
     "     OR Roadway Alignment = Curve Right )\n" + M_RD_EXCL,
     "Water (standing or moving) is its own attribute; left out - that is drainage, not friction."),
}

# Field Reference: MMUCC 6 equivalents, keyed by the SMS field name.
MMUCC_FR = {
 "Junction Type":
  "C12 Relation to Junction (Specific Location: Non-Junction, Intersection or Related, Driveway Access or "
  "Related, Crossover-Related, Entrance or Exit Ramp or Related, Through Roadway, Other Location Within an "
  "Interchange Area...) + C13 Type of Intersection (T, Y, L, Four-Leg, Five or More Legs, Circular, Other e.g. RCUT)",
 "Manner of Collision":
  "C9 Manner of Collision of the First Harmful Event: Not a Collision With a MV In-Transport, Angle, Front to "
  "Front, Front-to-Rear or Rear-to-Front, Rear to Rear, Rear-to-Side, Sideswipe Opposite / Same Direction",
 "First Harmful Event / Crash Harmful Event":
  "C7 First Harmful Event. No ran-off-road or cross-median values. Non-Motorist covers peds and bikes; Live "
  "Animal has no deer split. No crash-level 'most harmful event' - V38 is per vehicle.",
 "Sequence of Events":
  "V37 Sequence of Events (per vehicle, multi-select): Cross Centerline, Cross Median, Ran Off Roadway Left / "
  "Right / Direction Unknown, Re-Entering Roadway...",
 "First Harmful Event Location":
  "C8 Location of First Harmful Event: On Roadway, Continuous Left-Turn Lane, On Shoulder, On Roadside, On "
  "Median, Pedestrian Refuge Island or Traffic Island, In Parking Lane, Separator, Gore, Non-Trafficway Area",
 "Trafficway":
  "V25 Trafficway Flow (One-Way, Two-Way, Two-Way With a Continuous Left-Turn Lane) + V26 Median Barrier "
  "Presence (Not Applicable - no median; Median Without a Traffic Barrier; Median With Traffic Barrier). Both per vehicle.",
 "Road Character": "V28 Roadway Alignment (Straight, Curve Left, Curve Right) + V29 Roadway Grade. Per vehicle.",
 "Light Condition": "C11 Light Condition: Dark - Lighted, Dark - Not Lighted, Dark - Unknown Lighting",
 "Road Surface Condition": "V30 Roadway Surface Condition (per vehicle): Wet. Water (standing or moving) is separate.",
 "Traffic Control": "V31 Traffic Control Device (per vehicle): Stop Sign, Traffic Control Signal, Flashing Traffic Control Signal...",
 "Probable Cause":
  "Split in three: D5 Speeding-Related (Yes, Racing / Exceeded Speed Limit / Too Fast for Conditions); D10 "
  "Related Factors - Driver Level (Failure to Obey Traffic Control Devices, Overcorrecting...); C17 Related "
  "Factors - Crash Level (Obstruction in Roadway). No 'Debris' value.",
 "Unit Type": "P5 Person Type (Pedestrian..., Bicyclist, Other Cyclist) + NM9 Non-Motorist Device Type",
 "Vehicle Maneuver (unit movement)": "V33 Vehicle Status Prior to Critical Event: Turning Left, Turning Right, Negotiating a Curve...",
 "Roadway: AADT, Through Lanes, Speed Limit, Area Type":
  "AADT and area type are not on the report (link to road inventory, Ch. 10). Speed limit is V24 and lanes "
  "are V27 Number of Open Lanes, both per vehicle.",
}
