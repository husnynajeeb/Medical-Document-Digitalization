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
        "advice_high": "This could be due to excessive sugar intake, insulin resistance, early diabetes, or stress-related glucose elevation. Reduce sugar intake, increase physical activity, maintain a healthy weight, and monitor regularly. Consult a doctor if persistently high.",
        "advice_low": "This may indicate hypoglycemia due to skipping meals, excessive insulin, adrenal insufficiency, or other metabolic issues. Eat balanced meals and consult a doctor."
    },
    "POST PRANDIAL BLOOD GLUCOSE": {
        "unit": "mg/dl",
        "range": "70-140",
        "meaning": "Measures blood sugar after meals.",
        "advice_high": "Could be due to high carbohydrate intake, delayed insulin response, or early diabetes. Monitor glucose and consult a doctor if persistent.",
        "advice_low": "May indicate hypoglycemia from missed meals, excessive insulin, or metabolic issues. Eat balanced meals and monitor."
    },
    "HBA1C": {
        "unit": "%",
        "range": "4.5-6.5",
        "meaning": "Reflects average blood glucose over the past 2 to 3 months.",
        "advice_high": "Indicates poor long-term glucose control, possibly due to dietary habits, insufficient medication, or undiagnosed diabetes. Work with your doctor or endocrinologist to manage glucose levels.",
        "advice_low": "Usually not clinically concerning, but may result from frequent hypoglycemia, malnutrition, or over-exercising."
    },
    "VENOUS BLOOD GLUCOSE": {
        "unit": "mg/dl",
        "range": "70-110",
        "meaning": "Measures blood sugar in venous blood, usually fasting.",
        "advice_high": "May indicate hyperglycemia due to insulin resistance, stress, or early diabetes. Monitor diet and consult a doctor.",
        "advice_low": "May indicate hypoglycemia caused by skipped meals, excessive insulin, or adrenal insufficiency. Consult a doctor."
    },
    "RANDOM BLOOD SUGAR": {
        "unit": "mg/dl",
        "range": "70-140",
        "meaning": "Measures blood sugar at any random time of the day.",
        "advice_high": "Could indicate diabetes, recent high carbohydrate intake, or stress-related spikes. Monitor and consult a doctor if persistent.",
        "advice_low": "May indicate hypoglycemia due to delayed meals, excessive insulin, or illness. Monitor and consult a doctor."
    },
    "OGTT 2-HOUR": {
        "unit": "mg/dl",
        "range": "70-140",
        "meaning": "Measures blood sugar 2 hours after oral glucose.",
        "advice_high": "May indicate impaired glucose tolerance, early diabetes, or delayed insulin response. Consult a doctor for evaluation.",
        "advice_low": "May indicate hypoglycemia due to excessive insulin or metabolic issues. Monitor and consult a doctor."
    },

    # ----- Kidney -----
     # ----- Kidney -----
    "CREATININE": {
        "unit": "mg/dl",
        "range": "0.7-1.3",
        "meaning": "Assesses kidney function.",
        "advice_high": "May indicate kidney impairment, dehydration, or medication effects. Consult a doctor.",
        "advice_low": "Usually not concerning, but may occur with low muscle mass or certain diets."
    },
    "E-GFR": {
        "unit": "ml/min/1.73m2",
        "range": "90-120",
        "meaning": "Estimated glomerular filtration rate.",
        "advice_high": "Usually not concerning, can be influenced by hydration status or lab variation.",
        "advice_low": "May indicate chronic kidney disease or reduced kidney function; consult a doctor."
    },
    "E-GFR MALE": {
        "unit": "ml/min/1.73m2",
        "range": "90-130",
        "meaning": "Estimated GFR for males.",
        "advice_high": "Usually not concerning; may reflect hydration or lab variance.",
        "advice_low": "May indicate early kidney disease, dehydration, or medication effects."
    },
    "E-GFR FEMALE": {
        "unit": "ml/min/1.73m2",
        "range": "90-120",
        "meaning": "Estimated GFR for females.",
        "advice_high": "Usually not concerning; can be affected by hydration or lab variation.",
        "advice_low": "May indicate chronic kidney disease, dehydration, or medication effects."
    },
    "URINE MICRO ALBUMIN (UMA)": {
        "unit": "mg/L",
        "range": "0-30",
        "meaning": "Measures the amount of albumin in urine, indicating kidney health.",
        "advice_high": "May indicate early kidney damage, high blood pressure, or diabetes; consult your doctor.",
        "advice_low": "Normal, generally not concerning."
    },
    "URINE CREATININE": {
        "unit": "mg/dl",
        "range": "50-200",
        "meaning": "Creatinine level in urine, used for kidney assessment.",
        "advice_high": "May indicate kidney issues, dehydration, or high muscle mass.",
        "advice_low": "Usually normal, can be influenced by low muscle mass or fluid intake."
    },
    "UMA/CREATININE": {
        "unit": "mg/g",
        "range": "0-30",
        "meaning": "Ratio of urine microalbumin to creatinine; better indicator of kidney function.",
        "advice_high": "May indicate kidney damage, early diabetes, or hypertension; consult your doctor.",
        "advice_low": "Normal, typically not concerning."
    },

    # ----- Lipid Profile -----
"TOTAL CHOLESTEROL": {
    "unit": "mg/dl",
    "range": "125-200",
    "meaning": "Measures total cholesterol in blood, including HDL, LDL, and VLDL components, reflecting overall lipid health.",
    "advice_high": "High total cholesterol may result from excessive dietary fats, sedentary lifestyle, obesity, hypothyroidism, diabetes, or genetic factors such as familial hypercholesterolemia. Reduce saturated and trans fats, maintain a healthy diet, increase physical activity, and monitor regularly. Seek medical evaluation if persistently high.",
    "advice_low": "Low total cholesterol may occur due to malnutrition, liver disease, hyperthyroidism, or certain medications. Usually not clinically significant, but discuss with a doctor if symptomatic."
},
"HDL CHOLESTEROL": {
    "unit": "mg/dl",
    "range": "45-60",
    "meaning": "High-density lipoprotein (HDL) is the 'good' cholesterol that helps remove excess cholesterol from the blood, protecting heart health.",
    "advice_high": "High HDL is generally protective for cardiovascular health and may be seen with regular exercise, moderate alcohol consumption, or certain medications.",
    "advice_low": "Low HDL may increase risk for cardiovascular disease. Improve diet with healthy fats, increase regular physical activity, maintain a healthy weight, and consider lifestyle interventions."
},
"LDL CHOLESTEROL": {
    "unit": "mg/dl",
    "range": "0-159",
    "meaning": "Low-density lipoprotein (LDL) is 'bad' cholesterol; high levels increase risk of atherosclerosis and heart disease.",
    "advice_high": "High LDL may result from excessive saturated and trans fat intake, obesity, lack of exercise, diabetes, hypothyroidism, or genetic predisposition. Reduce unhealthy fats, maintain healthy weight, exercise regularly, and consult a doctor for monitoring and possible medications.",
    "advice_low": "Optimal LDL is usually not concerning; extremely low LDL is rare but may occur with certain genetic conditions or malabsorption."
},
"VLDL CHOLESTEROL": {
    "unit": "mg/dl",
    "range": "0-39",
    "meaning": "Very low-density lipoprotein (VLDL) carries triglycerides in the blood and is linked to cardiovascular risk.",
    "advice_high": "High VLDL may be caused by high sugar intake, refined carbohydrates, alcohol consumption, obesity, or metabolic syndrome. Reduce sugars and refined carbs, maintain a healthy weight, and consult a doctor if persistently elevated.",
    "advice_low": "Usually not concerning; low VLDL may occur with malnutrition or certain medications."
},
"TRIGLYCERIDES": {
    "unit": "mg/dl",
    "range": "0-150",
    "meaning": "Measures triglyceride levels in the blood, which are fats stored for energy.",
    "advice_high": "High triglycerides may result from obesity, excessive sugar or alcohol intake, sedentary lifestyle, hypothyroidism, diabetes, or genetic factors. Reduce sugar, alcohol, and refined carbs, maintain healthy weight, and increase physical activity. Consult a doctor if persistently elevated.",
    "advice_low": "Low triglycerides are usually not concerning; may occur with malnutrition or hyperthyroidism."
},
"CHO : HDL CHOL. RATIO": {
    "unit": "ratio",
    "range": "0-4.9",
    "meaning": "Ratio of total cholesterol to HDL; higher values indicate greater cardiovascular risk.",
    "advice_high": "High ratio may occur with elevated LDL, low HDL, obesity, poor diet, or metabolic syndrome. Improve diet, increase physical activity, maintain healthy weight, and consult a doctor if persistently high.",
    "advice_low": "Optimal ratio is usually not concerning and indicates lower cardiovascular risk."
},
    # ----- Proteins & Liver -----
    
    # ----- Proteins & Liver -----
    "TOTAL PROTEINS": {
        "unit": "g/dl",
        "range": "6.0-8.3",
        "meaning": "Measures total serum proteins in blood.",
        "advice_high": "May indicate dehydration, inflammation, or chronic infections.",
        "advice_low": "May indicate malnutrition, liver disease, kidney disease, or protein loss."
    },
    "SERUM ALBUMIN": {
        "unit": "g/dl",
        "range": "3.5-5.0",
        "meaning": "Main protein in blood; reflects liver and kidney health.",
        "advice_high": "Usually not concerning; can rise with dehydration or high protein intake.",
        "advice_low": "May indicate liver/kidney disease, malnutrition, or chronic illness."
    },
    "SERUM GLOBULIN": {
        "unit": "g/dl",
        "range": "2.0-3.5",
        "meaning": "Globulins are proteins in blood, important for immune function.",
        "advice_high": "May indicate chronic inflammation, infection, autoimmune disease, or certain cancers.",
        "advice_low": "May indicate immune deficiency, liver disease, or malnutrition."
    },
    "A/G RATIO": {
        "unit": "ratio",
        "range": "1.0-2.0",
        "meaning": "Albumin to globulin ratio, indicates liver/kidney health.",
        "advice_high": "May indicate low globulin levels, dehydration, or lab variation.",
        "advice_low": "May indicate liver/kidney disease, inflammation, or protein loss."
    },
    "TOTAL BILIRUBIN": {
        "unit": "mg/dl",
        "range": "0.3-1.2",
        "meaning": "Indicates liver function and red blood cell breakdown.",
        "advice_high": "May indicate liver disease, bile duct obstruction, hemolysis, or medication effects. Consult your doctor for further evaluation.",
        "advice_low": "Usually not concerning; may indicate malnutrition or rapid liver clearance."
    },
    "S.G.P.T (AST)": {
        "unit": "U/L",
        "range": "10-40",
        "meaning": "Liver enzyme indicating liver cell injury.",
        "advice_high": "May indicate liver inflammation, hepatitis, fatty liver, or drug-induced liver injury. Consult a doctor for proper diagnosis.",
        "advice_low": "Usually not concerning; may be seen in vitamin B6 deficiency or reduced muscle mass."
    },
    "S.G.O.T (AST)": {
        "unit": "U/L",
        "range": "10-40",
        "meaning": "Liver enzyme indicating liver or muscle injury.",
        "advice_high": "May indicate liver damage, muscle injury, or myocardial injury. Monitor and consult a doctor if persistent.",
        "advice_low": "Usually not concerning; may occur with low muscle mass or inactivity."
    },
    "GAMMA GT (GGT)": {
        "unit": "U/L",
        "range": "9-48",
        "meaning": "Enzyme indicating liver or bile duct health.",
        "advice_high": "May indicate liver disease, bile duct obstruction, alcohol use, or medication effects. Consult a doctor for further assessment.",
        "advice_low": "Usually not concerning; may indicate low enzyme activity or healthy liver function."
    },
    "S ALKALINE PHOSPHATASE": {
        "unit": "U/L",
        "range": "40-129",
        "meaning": "Enzyme related to liver and bone health.",
        "advice_high": "May indicate liver disease, bone disorders, bile duct obstruction, or growing children. Consult your doctor for evaluation.",
        "advice_low": "Usually not concerning; may indicate malnutrition, zinc deficiency, or low bone turnover."
    },
        # ----- Urine -----
    # ----- Urine -----
    "URINE FULL REPORT (UFR)": {
        "unit": "various",
        "range": "",
        "meaning": "Urine analysis to assess kidney and urinary tract health.",
        "advice_high": "Abnormal values may indicate infection, kidney or liver issues, dehydration, or metabolic disorders. Consult a doctor.",
        "advice_low": "Normal values, typically not concerning."
    },
    "COLOUR": {
        "unit": "description",
        "range": "pale yellow",
        "meaning": "Normal urine color indicates hydration and kidney function.",
        "advice_high": "Dark or abnormal color may indicate dehydration, liver disease, hematuria, or certain medications.",
        "advice_low": "Very light urine is usually normal, may indicate high fluid intake."
    },
    "APPEARANCE": {
        "unit": "description",
        "range": "clear",
        "meaning": "Clarity of urine; cloudy may indicate infection.",
        "advice_high": "Cloudy urine may indicate infection, crystals, or mucus.",
        "advice_low": "Normal appearance."
    },
    "SPECIFIC GRAVITY": {
        "unit": "",
        "range": "1.005-1.030",
        "meaning": "Measures urine concentration.",
        "advice_high": "May indicate dehydration, high solute load, or proteinuria.",
        "advice_low": "May indicate dilute urine, overhydration, or diabetes insipidus."
    },
    "PH": {
        "unit": "",
        "range": "4.5-8.0",
        "meaning": "Acidity of urine; reflects kidney function and diet.",
        "advice_high": "Alkaline urine may indicate urinary tract infection, kidney issues, or diet high in vegetables.",
        "advice_low": "Acidic urine may indicate high-protein diet, metabolic acidosis, or dehydration."
    },
    "PROTEIN": {
        "unit": "mg/dl",
        "range": "0-15",
        "meaning": "Presence of protein in urine; may indicate kidney damage.",
        "advice_high": "May indicate kidney disease, infection, or high protein intake. Consult a doctor.",
        "advice_low": "Normal."
    },
    "GLUCOSE": {
        "unit": "mg/dl",
        "range": "0",
        "meaning": "Glucose in urine; should normally be absent.",
        "advice_high": "May indicate diabetes, stress hyperglycemia, or kidney tubular issues.",
        "advice_low": "Normal."
    },
    "KETONE": {
        "unit": "mg/dl",
        "range": "0",
        "meaning": "Presence of ketones in urine; indicates fat metabolism.",
        "advice_high": "May indicate uncontrolled diabetes, fasting, low-carb diet, or starvation.",
        "advice_low": "Normal."
    },
    "BILIRUBIN": {
        "unit": "mg/dl",
        "range": "0",
        "meaning": "Should be absent; indicates liver function.",
        "advice_high": "May indicate liver disease, hemolysis, or bile duct obstruction.",
        "advice_low": "Normal."
    },
    "UROBILINOGEN": {
        "unit": "mg/dl",
        "range": "0.1-1.0",
        "meaning": "Indicates liver function.",
        "advice_high": "May indicate liver disease, hemolytic disorders, or bile duct issues.",
        "advice_low": "Usually normal; low may occur with bile duct obstruction."
    },
    "PUS CELLS": {
        "unit": "cells/hpf",
        "range": "0-5",
        "meaning": "White blood cells in urine; indicates infection if high.",
        "advice_high": "May indicate urinary tract infection, inflammation, or kidney stones.",
        "advice_low": "Normal."
    },
    "RED CELLS": {
        "unit": "cells/hpf",
        "range": "0-3",
        "meaning": "Red blood cells in urine; may indicate bleeding.",
        "advice_high": "May indicate urinary tract or kidney bleeding, infection, or stones.",
        "advice_low": "Normal."
    },
    "EPITHELIAL CELLS": {
        "unit": "cells/hpf",
        "range": "0-5",
        "meaning": "Cells lining urinary tract; slightly present is normal.",
        "advice_high": "May indicate contamination, infection, or kidney disease.",
        "advice_low": "Normal."
    },
    "ORGANISMS": {
        "unit": "description",
        "range": "none",
        "meaning": "Presence of bacteria or yeast in urine; should be absent.",
        "advice_high": "May indicate urinary tract infection, contamination, or fungal infection. Consult a doctor.",
        "advice_low": "Normal."
    },
    "CRYSTALS": {
        "unit": "description",
        "range": "none",
        "meaning": "Urinary crystals may indicate kidney stones.",
        "advice_high": "May indicate risk of kidney stones, dehydration, or metabolic disorders.",
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
    # ----- Hematology differential & RBC indices -----
    "NEU%": {
            "unit": "%",
            "range": "40-70",
            "meaning": "Percentage of neutrophils in white blood cells.",
            "advice_high": "May indicate bacterial infection, inflammation, stress, or corticosteroid effect.",
            "advice_low": "May indicate viral infection, bone marrow suppression, or chemotherapy effect."
        },
        "LYM%": {
            "unit": "%",
            "range": "20-40",
            "meaning": "Percentage of lymphocytes in white blood cells.",
            "advice_high": "May indicate viral infection, chronic inflammation, or lymphocytic leukemia.",
            "advice_low": "May indicate immune suppression, stress response, or corticosteroid therapy."
        },
        "MON%": {
            "unit": "%",
            "range": "2-8",
            "meaning": "Percentage of monocytes in white blood cells.",
            "advice_high": "May indicate chronic infection, inflammation, or hematologic disorder.",
            "advice_low": "May indicate bone marrow suppression or corticosteroid effect."
        },
        "EOS%": {
            "unit": "%",
            "range": "1-4",
            "meaning": "Percentage of eosinophils in white blood cells.",
            "advice_high": "May indicate allergy, parasitic infection, or skin disorders.",
            "advice_low": "Usually normal."
        },
        "BASO%": {
            "unit": "%",
            "range": "0-1",
            "meaning": "Percentage of basophils in white blood cells.",
            "advice_high": "May indicate allergic reaction, inflammation, or myeloproliferative disorder.",
            "advice_low": "Usually normal."
        },
        "NEU#": {
            "unit": "10^3/uL",
            "range": "2.0-7.0",
            "meaning": "Absolute count of neutrophils.",
            "advice_high": "May indicate bacterial infection, inflammation, or stress response.",
            "advice_low": "May indicate neutropenia, viral infection, or bone marrow suppression."
        },
        "LYM#": {
            "unit": "10^3/uL",
            "range": "1.0-3.0",
            "meaning": "Absolute count of lymphocytes.",
            "advice_high": "May indicate viral infection, lymphocytic leukemia, or chronic inflammation.",
            "advice_low": "May indicate immunodeficiency, stress, or corticosteroid therapy."
        },
        "MON#": {
            "unit": "10^3/uL",
            "range": "0.2-0.8",
            "meaning": "Absolute count of monocytes.",
            "advice_high": "May indicate chronic infection, inflammation, or hematologic disorder.",
            "advice_low": "May indicate bone marrow suppression."
        },
        "EOS#": {
            "unit": "10^3/uL",
            "range": "0.02-0.5",
            "meaning": "Absolute count of eosinophils.",
            "advice_high": "May indicate allergy, parasitic infection, or skin disorders.",
            "advice_low": "Usually normal."
        },
        "BASO#": {
            "unit": "10^3/uL",
            "range": "0-0.1",
            "meaning": "Absolute count of basophils.",
            "advice_high": "May indicate inflammation, allergy, or myeloproliferative disorder.",
            "advice_low": "Usually normal."
        },
        "MCV": {
            "unit": "fL",
            "range": "80-100",
            "meaning": "Mean corpuscular volume; average size of red blood cells.",
            "advice_high": "May indicate macrocytic anemia, vitamin B12/folate deficiency, or liver disease.",
            "advice_low": "May indicate microcytic anemia, iron deficiency, or chronic disease."
        },
        "MCH": {
            "unit": "pg",
            "range": "27-33",
            "meaning": "Mean corpuscular hemoglobin; average hemoglobin per RBC.",
            "advice_high": "May indicate macrocytic anemia or vitamin B12/folate deficiency.",
            "advice_low": "May indicate microcytic anemia or iron deficiency."
        },
        "MCHC": {
            "unit": "g/dL",
            "range": "32-36",
            "meaning": "Mean corpuscular hemoglobin concentration.",
            "advice_high": "May indicate spherocytosis or hereditary RBC disorders.",
            "advice_low": "May indicate iron deficiency anemia or chronic blood loss."
        },
        "RDW-CV": {
            "unit": "%",
            "range": "11.5-14.5",
            "meaning": "Red cell distribution width coefficient of variation.",
            "advice_high": "May indicate anemia, mixed deficiency, or recent blood loss.",
            "advice_low": "Usually normal."
        },
        "MPV": {
            "unit": "fL",
            "range": "7.5-11.5",
            "meaning": "Mean platelet volume; indicates platelet size.",
            "advice_high": "May indicate platelet activation, inflammation, or recovery from thrombocytopenia.",
            "advice_low": "Usually normal."
        },
        "*ALY%": {
            "unit": "%",
            "range": "0-0.5",
            "meaning": "Abnormal lymphocytes percentage.",
            "advice_high": "May indicate viral infection or hematologic disorder.",
            "advice_low": "Usually normal."
        },
        "*LIC%": {
            "unit": "%",
            "range": "0-0.5",
            "meaning": "Large immature cells percentage.",
            "advice_high": "May indicate leukemia or hematologic disorder.",
            "advice_low": "Usually normal."
        },
        "*ALY#": {
            "unit": "10^3/uL",
            "range": "0-0.05",
            "meaning": "Absolute count of abnormal lymphocytes.",
            "advice_high": "May indicate viral infection, lymphoproliferative disorder, or hematologic disease.",
            "advice_low": "Usually normal."
        },
        "*LIC#": {
            "unit": "10^3/uL",
            "range": "0-0.05",
            "meaning": "Absolute count of large immature cells.",
            "advice_high": "May indicate leukemia, bone marrow disorder, or hematologic disease.",
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
    "POST PRANDIAL BLOOD GLUCOSE",
    "POST PRANDIAL BLOOD SUGAR",
    "POSTPRANDIAL",
    "PPBS",
    "POSTPRANDIALBLOODSUGAR",
    "POSTPRANDIALBLOODGLUCOSE",
    "POSTPRANDIAL GLUCOSE",
    "PP BLOOD SUGAR",
    "PP BLOOD GLUCOSE",
    "OST PRANDIAL BLOOD GLUCOSE",
    "OST PRANDIAL BLOOD SUGAR"
   ],
    "HBA1C": [
        "HBA1C", "HBAIC", "HBALC", "GLYCATEDHAEMOGLOBIN", "GLYCOSYLATEDHEMOGLOBIN"
    ],
    "VENOUS BLOOD GLUCOSE": [
        "VENOUS BLOOD GLUCOSE", "VBG", "VENOUSGLUCOSE", "VEN BLOOD SUGAR"
    ],
    "RANDOM BLOOD SUGAR": [
        "RANDOM BLOOD SUGAR", "RBS", "RANDOMGLUCOSE", "RANDOMGLUCOSESUGAR" , "RANOOW BLOOD SUGAR OA"
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
 