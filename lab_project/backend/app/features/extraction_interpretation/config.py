import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.abspath(
    os.path.join(BASE_DIR, "../../../models/clinicalbert")
)

TEST_KNOWLEDGE = {
    # ----- Glucose -----
    "FASTING BLOOD SUGAR": {
        "unit": "mg/dl",
        "range": "70-110",
        "meaning": "Measures blood sugar after fasting for at least 8 hours.",
        "advice_high": "Reduce sugar intake, increase physical activity, maintain a healthy weight, and monitor regularly. Consult a doctor if persistently high.",
        "advice_low": "May indicate hypoglycemia. Consult a doctor."
    },
    "POST PRANDIAL BLOOD GLUCOSE": {
        "unit": "mg/dl",
        "range": "70-140",
        "meaning": "Measures blood sugar after meals.",
        "advice_high": "Limit carbohydrates and monitor glucose.",
        "advice_low": "May indicate hypoglycemia."
    },
    "HBA1C": {
        "unit": "%",
        "range": "4.5-6.5",
        "meaning": "Reflects average blood glucose over the past 2 to 3 months.",
        "advice_high": "Indicates poor long-term glucose control.",
        "advice_low": "Usually not clinically concerning."
    },
    "VENOUS BLOOD GLUCOSE": {
        "unit": "mg/dl",
        "range": "70-110",
        "meaning": "Measures blood sugar in venous blood, usually fasting.",
        "advice_high": "May indicate hyperglycemia; monitor diet and consult a doctor.",
        "advice_low": "May indicate hypoglycemia; consult a doctor."
    },
    "RANDOM BLOOD SUGAR": {
        "unit": "mg/dl",
        "range": "70-140",
        "meaning": "Measures blood sugar at any random time of the day.",
        "advice_high": "May indicate diabetes; monitor blood sugar and consult a doctor.",
        "advice_low": "May indicate hypoglycemia; monitor and consult a doctor."
    },
    "OGTT 2-HOUR": {
        "unit": "mg/dl",
        "range": "70-140",
        "meaning": "Measures blood sugar 2 hours after oral glucose.",
        "advice_high": "May indicate impaired glucose tolerance or diabetes.",
        "advice_low": "May indicate hypoglycemia."
    },

    # ----- Kidney -----
    "CREATININE": {
        "unit": "mg/dl",
        "range": "0.7-1.3",
        "meaning": "Assesses kidney function.",
        "advice_high": "May indicate kidney impairment.",
        "advice_low": "Usually not concerning."
    },
    "E-GFR": {
        "unit": "ml/min/1.73m2",
        "range": "90-120",
        "meaning": "Estimated glomerular filtration rate.",
        "advice_high": "Usually not concerning.",
        "advice_low": "May indicate chronic kidney disease."
    },
    "E-GFR MALE": {
        "unit": "ml/min/1.73m2",
        "range": "90-130",
        "meaning": "Estimated GFR for males.",
        "advice_high": "Usually not concerning.",
        "advice_low": "May indicate chronic kidney disease."
    },
    "E-GFR FEMALE": {
        "unit": "ml/min/1.73m2",
        "range": "90-120",
        "meaning": "Estimated GFR for females.",
        "advice_high": "Usually not concerning.",
        "advice_low": "May indicate chronic kidney disease."
    },
    "URINE MICRO ALBUMIN (UMA)": {
        "unit": "mg/L",
        "range": "0-30",
        "meaning": "Measures the amount of albumin in urine, indicating kidney health.",
        "advice_high": "May indicate early kidney damage; consult your doctor.",
        "advice_low": "Normal."
    },
    "URINE CREATININE": {
        "unit": "mg/dl",
        "range": "50-200",
        "meaning": "Creatinine level in urine, used for kidney assessment.",
        "advice_high": "May indicate kidney issues.",
        "advice_low": "Usually normal."
    },
    "UMA/CREATININE": {
        "unit": "mg/g",
        "range": "0-30",
        "meaning": "Ratio of urine microalbumin to creatinine; better indicator of kidney function.",
        "advice_high": "May indicate kidney damage; consult your doctor.",
        "advice_low": "Normal."
    },

    # ----- Lipid Profile -----
    "TOTAL CHOLESTEROL": {
        "unit": "mg/dl",
        "range": "125-200",
        "meaning": "Measures total cholesterol in blood.",
        "advice_high": "Reduce saturated fat intake and increase physical activity.",
        "advice_low": "Usually not clinically significant."
    },
    "HDL CHOLESTEROL": {
        "unit": "mg/dl",
        "range": "45-60",
        "meaning": "Good cholesterol that protects heart health.",
        "advice_high": "Protective for heart health.",
        "advice_low": "Increase exercise and healthy fats."
    },
    "LDL CHOLESTEROL": {
        "unit": "mg/dl",
        "range": "0-159",
        "meaning": "Bad cholesterol associated with heart disease risk.",
        "advice_high": "Reduce saturated fats and consult a doctor.",
        "advice_low": "Optimal level."
    },
    "VLDL CHOLESTEROL": {
        "unit": "mg/dl",
        "range": "0-39",
        "meaning": "Very Low Density Lipoprotein cholesterol, linked to heart risk.",
        "advice_high": "Reduce sugar, refined carbs, and alcohol.",
        "advice_low": "Usually not concerning."
    },
    "TRIGLYCERIDES": {
        "unit": "mg/dl",
        "range": "0-150",
        "meaning": "Measures fat levels in blood.",
        "advice_high": "Reduce sugar, alcohol, and refined carbs.",
        "advice_low": "Usually not concerning."
    },
    "CHO : HDL CHOL. RATIO": {
        "unit": "ratio",
        "range": "0-4.9",
        "meaning": "Cholesterol to HDL ratio, indicates cardiovascular risk.",
        "advice_high": "Maintain healthy diet, exercise regularly.",
        "advice_low": "Optimal."
    },

    # ----- Proteins & Liver -----
    "TOTAL PROTEINS": {
        "unit": "g/dl",
        "range": "6.0-8.3",
        "meaning": "Measures total serum proteins in blood.",
        "advice_high": "May indicate dehydration or inflammation.",
        "advice_low": "May indicate malnutrition or liver disease."
    },
    "SERUM ALBUMIN": {
        "unit": "g/dl",
        "range": "3.5-5.0",
        "meaning": "Main protein in blood; reflects liver and kidney health.",
        "advice_high": "Usually not concerning.",
        "advice_low": "May indicate liver/kidney disease or malnutrition."
    },
    "SERUM GLOBULIN": {
        "unit": "g/dl",
        "range": "2.0-3.5",
        "meaning": "Globulins are proteins in blood, important for immune function.",
        "advice_high": "May indicate chronic inflammation or infection.",
        "advice_low": "May indicate immune deficiency."
    },
    "A/G RATIO": {
        "unit": "ratio",
        "range": "1.0-2.0",
        "meaning": "Albumin to globulin ratio, indicates liver/kidney health.",
        "advice_high": "May indicate low globulin levels.",
        "advice_low": "May indicate liver/kidney disease."
    },
    "TOTAL BILIRUBIN": {
        "unit": "mg/dl",
        "range": "0.3-1.2",
        "meaning": "Indicates liver function and red blood cell breakdown.",
        "advice_high": "May indicate liver disease or hemolysis.",
        "advice_low": "Usually not concerning."
    },
    "S.G.P.T (AST)": {
        "unit": "U/L",
        "range": "10-40",
        "meaning": "Liver enzyme indicating liver cell injury.",
        "advice_high": "May indicate liver inflammation; consult a doctor.",
        "advice_low": "Usually not concerning."
    },
    "S.G.O.T (AST)": {
        "unit": "U/L",
        "range": "10-40",
        "meaning": "Liver enzyme indicating liver or muscle injury.",
        "advice_high": "May indicate liver/muscle injury.",
        "advice_low": "Usually not concerning."
    },
    "GAMMA GT (GGT)": {
        "unit": "U/L",
        "range": "9-48",
        "meaning": "Enzyme indicating liver or bile duct health.",
        "advice_high": "May indicate liver/bile duct issues.",
        "advice_low": "Usually not concerning."
    },
    "S ALKALINE PHOSPHATASE": {
        "unit": "U/L",
        "range": "40-129",
        "meaning": "Enzyme related to liver and bone health.",
        "advice_high": "May indicate liver or bone disease.",
        "advice_low": "Usually not concerning."
    },

    # ----- Urine -----
    "URINE FULL REPORT (UFR)": {
        "unit": "various",
        "range": "",
        "meaning": "Urine analysis to assess kidney and urinary tract health.",
        "advice_high": "Abnormal values may indicate infection, kidney or liver issues. Consult a doctor.",
        "advice_low": "Normal values."
    },
    "COLOUR": {
        "unit": "description",
        "range": "pale yellow",
        "meaning": "Normal urine color indicates hydration and kidney function.",
        "advice_high": "Abnormal color may indicate dehydration or disease.",
        "advice_low": "Usually normal."
    },
    "APPEARANCE": {
        "unit": "description",
        "range": "clear",
        "meaning": "Clarity of urine; cloudy may indicate infection.",
        "advice_high": "Cloudy urine may indicate infection.",
        "advice_low": "Normal."
    },
    "SPECIFIC GRAVITY": {
        "unit": "",
        "range": "1.005-1.030",
        "meaning": "Measures urine concentration.",
        "advice_high": "May indicate dehydration or high solute concentration.",
        "advice_low": "May indicate dilute urine."
    },
    "PH": {
        "unit": "",
        "range": "4.5-8.0",
        "meaning": "Acidity of urine; reflects kidney function and diet.",
        "advice_high": "May indicate urinary tract infection.",
        "advice_low": "Usually normal."
    },
    "PROTEIN": {
        "unit": "mg/dl",
        "range": "0-15",
        "meaning": "Presence of protein in urine; may indicate kidney damage.",
        "advice_high": "Consult a doctor for possible kidney disease.",
        "advice_low": "Normal."
    },
    "GLUCOSE": {
        "unit": "mg/dl",
        "range": "0",
        "meaning": "Glucose in urine; should normally be absent.",
        "advice_high": "May indicate diabetes; consult a doctor.",
        "advice_low": "Normal."
    },
    "KETONE": {
        "unit": "mg/dl",
        "range": "0",
        "meaning": "Presence of ketones in urine; indicates fat metabolism.",
        "advice_high": "May indicate uncontrolled diabetes or fasting.",
        "advice_low": "Normal."
    },
    "BILIRUBIN": {
        "unit": "mg/dl",
        "range": "0",
        "meaning": "Should be absent; indicates liver function.",
        "advice_high": "May indicate liver disease.",
        "advice_low": "Normal."
    },
    "UROBILINOGEN": {
        "unit": "mg/dl",
        "range": "0.1-1.0",
        "meaning": "Indicates liver function.",
        "advice_high": "May indicate liver disease.",
        "advice_low": "Usually normal."
    },
    "PUS CELLS": {
        "unit": "cells/hpf",
        "range": "0-5",
        "meaning": "White blood cells in urine; indicates infection if high.",
        "advice_high": "May indicate urinary tract infection.",
        "advice_low": "Normal."
    },
    "RED CELLS": {
        "unit": "cells/hpf",
        "range": "0-3",
        "meaning": "Red blood cells in urine; may indicate bleeding.",
        "advice_high": "May indicate urinary tract or kidney bleeding.",
        "advice_low": "Normal."
    },
    "EPITHELIAL CELLS": {
        "unit": "cells/hpf",
        "range": "0-5",
        "meaning": "Cells lining urinary tract; slightly present is normal.",
        "advice_high": "May indicate contamination or infection.",
        "advice_low": "Normal."
    },
    "ORGANISMS": {
        "unit": "description",
        "range": "none",
        "meaning": "Presence of bacteria or yeast in urine; should be absent.",
        "advice_high": "May indicate infection; consult a doctor.",
        "advice_low": "Normal."
    },
    "CRYSTALS": {
        "unit": "description",
        "range": "none",
        "meaning": "Urinary crystals may indicate kidney stones.",
        "advice_high": "May indicate risk of kidney stones.",
        "advice_low": "Normal."
    },

    # ----- Hematology -----
    "WBC": {
        "unit": "10^3/uL",
        "range": "4.0-11.0",
        "meaning": "White blood cell count, indicates immune status.",
        "advice_high": "May indicate infection or inflammation.",
        "advice_low": "May indicate bone marrow issues or immunodeficiency."
    },
    "RBC": {
        "unit": "10^6/uL",
        "range": "4.2-5.9",
        "meaning": "Red blood cell count, important for oxygen transport.",
        "advice_high": "May indicate dehydration or polycythemia.",
        "advice_low": "May indicate anemia."
    },
    "HEMOGLOBIN": {
        "unit": "g/dl",
        "range": "13.5-17.5",
        "meaning": "Oxygen-carrying protein in red blood cells.",
        "advice_high": "May indicate dehydration or polycythemia.",
        "advice_low": "May indicate anemia."
    },
    "HEMATOCRIT": {
        "unit": "%",
        "range": "41-53",
        "meaning": "Proportion of red blood cells in blood.",
        "advice_high": "May indicate dehydration or polycythemia.",
        "advice_low": "May indicate anemia."
    },
    "PLATELETS": {
        "unit": "10^3/uL",
        "range": "150-450",
        "meaning": "Platelet count; important for clotting.",
        "advice_high": "May indicate inflammation or bone marrow disorder.",
        "advice_low": "May indicate risk of bleeding."
    },
    # ----- Hematology differential & RBC indices -----
    "NEU%": {
        "unit": "%",
        "range": "40-70",
        "meaning": "Percentage of neutrophils in white blood cells.",
        "advice_high": "May indicate bacterial infection or inflammation.",
        "advice_low": "May indicate viral infection or bone marrow suppression."
    },
    "LYM%": {
        "unit": "%",
        "range": "20-40",
        "meaning": "Percentage of lymphocytes in white blood cells.",
        "advice_high": "May indicate viral infection or chronic inflammation.",
        "advice_low": "May indicate immune suppression."
    },
    "MON%": {
        "unit": "%",
        "range": "2-8",
        "meaning": "Percentage of monocytes in white blood cells.",
        "advice_high": "May indicate chronic infection or inflammation.",
        "advice_low": "May indicate bone marrow suppression."
    },
    "EOS%": {
        "unit": "%",
        "range": "1-4",
        "meaning": "Percentage of eosinophils in white blood cells.",
        "advice_high": "May indicate allergy or parasitic infection.",
        "advice_low": "Usually normal."
    },
    "BASO%": {
        "unit": "%",
        "range": "0-1",
        "meaning": "Percentage of basophils in white blood cells.",
        "advice_high": "May indicate allergic reaction or inflammation.",
        "advice_low": "Usually normal."
    },
    "NEU#": {
        "unit": "10^3/uL",
        "range": "2.0-7.0",
        "meaning": "Absolute count of neutrophils.",
        "advice_high": "May indicate bacterial infection.",
        "advice_low": "May indicate neutropenia."
    },
    "LYM#": {
        "unit": "10^3/uL",
        "range": "1.0-3.0",
        "meaning": "Absolute count of lymphocytes.",
        "advice_high": "May indicate viral infection.",
        "advice_low": "May indicate immunodeficiency."
    },
    "MON#": {
        "unit": "10^3/uL",
        "range": "0.2-0.8",
        "meaning": "Absolute count of monocytes.",
        "advice_high": "May indicate chronic infection.",
        "advice_low": "May indicate bone marrow suppression."
    },
    "EOS#": {
        "unit": "10^3/uL",
        "range": "0.02-0.5",
        "meaning": "Absolute count of eosinophils.",
        "advice_high": "May indicate allergy or parasitic infection.",
        "advice_low": "Usually normal."
    },
    "BASO#": {
        "unit": "10^3/uL",
        "range": "0-0.1",
        "meaning": "Absolute count of basophils.",
        "advice_high": "May indicate inflammation or allergy.",
        "advice_low": "Usually normal."
    },
    "MCV": {
        "unit": "fL",
        "range": "80-100",
        "meaning": "Mean corpuscular volume; average size of red blood cells.",
        "advice_high": "May indicate macrocytic anemia.",
        "advice_low": "May indicate microcytic anemia."
    },
    "MCH": {
        "unit": "pg",
        "range": "27-33",
        "meaning": "Mean corpuscular hemoglobin; average hemoglobin per RBC.",
        "advice_high": "May indicate macrocytic anemia.",
        "advice_low": "May indicate microcytic anemia."
    },
    "MCHC": {
        "unit": "g/dL",
        "range": "32-36",
        "meaning": "Mean corpuscular hemoglobin concentration.",
        "advice_high": "May indicate spherocytosis.",
        "advice_low": "May indicate iron deficiency."
    },
    "RDW-CV": {
        "unit": "%",
        "range": "11.5-14.5",
        "meaning": "Red cell distribution width coefficient of variation.",
        "advice_high": "May indicate anemia.",
        "advice_low": "Usually normal."
    },
    "MPV": {
        "unit": "fL",
        "range": "7.5-11.5",
        "meaning": "Mean platelet volume; indicates platelet size.",
        "advice_high": "May indicate platelet activation.",
        "advice_low": "Usually normal."
    },
    "*ALY%": {
        "unit": "%",
        "range": "0-0.5",
        "meaning": "Abnormal lymphocytes percentage.",
        "advice_high": "May indicate viral infection.",
        "advice_low": "Usually normal."
    },
    "*LIC%": {
        "unit": "%",
        "range": "0-0.5",
        "meaning": "Large immature cells percentage.",
        "advice_high": "May indicate leukemia.",
        "advice_low": "Usually normal."
    },
    "*ALY#": {
        "unit": "10^3/uL",
        "range": "0-0.05",
        "meaning": "Absolute count of abnormal lymphocytes.",
        "advice_high": "May indicate viral infection or hematologic disorder.",
        "advice_low": "Usually normal."
    },
    "*LIC#": {
        "unit": "10^3/uL",
        "range": "0-0.05",
        "meaning": "Absolute count of large immature cells.",
        "advice_high": "May indicate leukemia or hematologic disorder.",
        "advice_low": "Usually normal."
    }
}

# This dictionary is fully ready to:
# 1. Add more tests anytime.
# 2. Combine multiple reports.
# 3. Generate interpretations using `advice_high` and `advice_low`.

TEST_ALIASES = {
    # ---- Glucose ----
    "FASTING BLOOD SUGAR": [
        "FASTING BLOOD SUGAR", "FASTINGBLOODSUGAR", "FBS", "FASTING GLUCOSE", "GLUCOSEFASTING", "FASTINGPLASMAGLUCOSE"
    ],
    "POST PRANDIAL BLOOD GLUCOSE": [
        "POST PRANDIAL BLOOD GLUCOSE", "POSTPRANDIAL", "PPBS", "POSTPRANDIALBLOODSUGAR", "POSTPRANDIAL GLUCOSE"
    ],
    "HBA1C": [
        "HBA1C", "HBAIC", "HBALC", "GLYCATEDHAEMOGLOBIN", "GLYCOSYLATEDHEMOGLOBIN"
    ],
    "VENOUS BLOOD GLUCOSE": [
        "VENOUS BLOOD GLUCOSE", "VBG", "VENOUSGLUCOSE", "VEN BLOOD SUGAR"
    ],
    "RANDOM BLOOD SUGAR": [
        "RANDOM BLOOD SUGAR", "RBS", "RANDOMGLUCOSE", "RANDOMGLUCOSESUGAR"
    ],
    "OGTT 2-HOUR": [
        "OGTT 2-HOUR", "ORAL GLUCOSE TOLERANCE", "OGTT", "OGTT 2HR", "2 HOUR OGTT"
    ],

    # ---- Kidney ----
    "CREATININE": ["CREATININE", "SERUMCREATININE", "S.CREATININE"],
    "E-GFR": ["E-GFR", "EGFR", "ESTIMATED GFR"],
    "E-GFR MALE": ["E-GFR MALE", "EGFR MALE", "ESTIMATED GFR MALE"],
    "E-GFR FEMALE": ["E-GFR FEMALE", "EGFR FEMALE", "ESTIMATED GFR FEMALE"],

    # ---- Lipid Profile ----
    "TOTAL CHOLESTEROL": ["TOTAL CHOLESTEROL", "TOTALCHOLESTEROL", "CHOLESTEROL TOTAL", "TC"],
    "HDL CHOLESTEROL": ["HDL CHOLESTEROL", "HDL-CHOLESTEROL", "CHOLESTEROL HDL", "HDL CHOL", "S HDL", "HDL"],
    "LDL CHOLESTEROL": ["LDL CHOLESTEROL", "LDL-CHOLESTEROL", "CHOLESTEROL LDL", "LDL CHOL", "S LDL", "LDL"],
    "VLDL CHOLESTEROL": ["VLDL CHOLESTEROL", "VLDL-CHOLESTEROL", "VLDL CHOL", "VLDL"],
    "TRIGLYCERIDES": ["TRIGLYCERIDES", "TRIGLYCERIDE", "TG", "TRIG"],
    "CHO : HDL CHOL. RATIO": ["CHO:HDL RATIO", "CHO / HDL RATIO", "TOTAL CHOLESTEROL / HDL RATIO", "CHO/HDL"],

    # ---- Urine Albumin ----
    "URINE MICRO ALBUMIN (UMA)": ["URINE MICRO ALBUMIN", "MICRO ALBUMIN", "URINE MICROALBUMIN", "UMA"],
    "URINE CREATININE": ["URINE CREATININE", "U CREATININE"],
    "UMA/CREATININE": ["UMA / CREATININE", "UMA CREATININE", "URINE MICRO ALBUMIN CREATININE", "MICRO ALBUMIN CREATININE"],

    # ---- Proteins & Liver ----
    "TOTAL PROTEINS": ["TOTAL PROTEINS", "TOTALPROTEINS", "TP"],
    "SERUM ALBUMIN": ["SERUM ALBUMIN", "SERUMALBUMIN", "ALBUMIN", "S.ALB"],
    "SERUM GLOBULIN": ["SERUM GLOBULIN", "SERUMGLOBULIN", "GLOBULIN", "S.GLOB"],
    "A/G RATIO": ["A/G RATIO", "AG RATIO", "AGRATIO"],
    "TOTAL BILIRUBIN": ["TOTAL BILIRUBIN", "TOTALBILIRUBIN", "BILIRUBIN", "TBIL"],
    "S.G.P.T (ALT)": ["SGPT", "SGPT ALT", "S G P T", "ALT"],
    "S.G.O.T (AST)": ["SGOT", "SGOT AST", "S G O T", "AST"],
    "GAMMA GT (GGT)": ["GAMMA GT", "GGT", "GAMMAGT"],
    "S ALKALINE PHOSPHATASE": ["ALKALINE PHOSPHATASE", "ALP", "SAP"],

    # ---- Hematology ----
    "WBC": ["WBC", "WHITE BLOOD CELLS", "WHITE CELL COUNT"],
    "RBC": ["RBC", "RED BLOOD CELLS", "ERYTHROCYTES"],
    "HEMOGLOBIN": ["HEMOGLOBIN", "HGB", "HB"],
    "HEMATOCRIT": ["HEMATOCRIT", "HCT"],
    "PLATELETS": ["PLATELETS", "PLT"],
    "RDW": ["RDW", "RED CELL DISTRIBUTION WIDTH"],
    "RDW-SD": ["RDW-SD", "RDWSD"],
    "MCV": ["MCV", "MEAN CORPUSCULAR VOLUME"],
    "MCH": ["MCH", "MEAN CORPUSCULAR HEMOGLOBIN"],
    "MCHC": ["MCHC", "MEAN CORPUSCULAR HEMOGLOBIN CONCENTRATION"],
    "RDW-CV": ["RDW-CV"],
    "MPV": ["MPV", "MEAN PLATELET VOLUME"],

    # ---- Differential ----
    "NEU%": ["NEU%", "NEUTROPHILS%", "NEUTROPHILS PERCENT"],
    "LYM%": ["LYM%", "LYMPHOCYTES%"],
    "MON%": ["MON%", "MONOCYTES%"],
    "EOS%": ["EOS%", "EOSINOPHILS%"],
    "BASO%": ["BASO%", "BASOPHILS%"],
    "NEU#": ["NEU#", "NEUTROPHILS#"],
    "LYM#": ["LYM#", "LYMPHOCYTES#"],
    "MON#": ["MON#", "MONOCYTES#"],
    "EOS#": ["EOS#", "EOSINOPHILS#"],
    "BASO#": ["BASO#", "BASOPHILS#"],
    "*ALY%": ["*ALY%", "ABNORMAL LYMPHOCYTES%"],
    "*LIC%": ["*LIC%", "LARGE IMMATURE CELLS%"],
    "*ALY#": ["*ALY#", "ABNORMAL LYMPHOCYTES#"],
    "*LIC#": ["*LIC#", "LARGE IMMATURE CELLS#"],

    # ---- Urine Analysis ----
    "URINE FULL REPORT (UFR)": ["URINE FULL REPORT", "UFR", "URINALYSIS"],
    "COLOUR": ["COLOUR", "URINE COLOR"],
    "APPEARANCE": ["APPEARANCE", "URINE APPEARANCE"],
    "SPECIFIC GRAVITY": ["SPECIFIC GRAVITY", "SG"],
    "PH": ["PH", "URINE PH"],
    "PROTEIN": ["PROTEIN", "URINE PROTEIN"],
    "GLUCOSE": ["GLUCOSE", "URINE GLUCOSE"],
    "KETONE": ["KETONE", "URINE KETONE"],
    "BILIRUBIN": ["BILIRUBIN", "URINE BILIRUBIN"],
    "UROBILINOGEN": ["UROBILINOGEN", "URINE UROBILINOGEN"],
    "PUS CELLS": ["PUS CELLS", "WBC IN URINE"],
    "RED CELLS": ["RED CELLS", "RBC IN URINE"],
    "EPITHELIAL CELLS": ["EPITHELIAL CELLS"],
    "ORGANISMS": ["ORGANISMS", "BACTERIA", "YEAST"],
    "CRYSTALS": ["CRYSTALS", "URINE CRYSTALS"]
}
