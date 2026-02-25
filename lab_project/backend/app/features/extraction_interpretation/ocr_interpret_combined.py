def generate_full_combined_interpretation(results, filenames):
    """
    Generate detailed combined interpretation JSON for lab results.
    - results: list of dicts with keys: test, value, unit, range, meaning, advice
    - filenames: list of report images
    Returns a dict with filenames, results (non-combined), and combined_interpretation
    """

    # Map results by normalized test name for easy lookup
    test_map = {r['test'].upper(): r for r in results}
    used_tests = set()
    combined_interpretation_list = []

    # Helper: check if a value is high, low, or normal
    def high_low_text(value, range_str):
        try:
            low, high = [float(x) for x in range_str.replace(" ", "").split("-")]
            if value < low:
                return "low"
            elif value > high:
                return "high"
            else:
                return "normal"
        except:
            return "normal"

    # ----------------------
    # 1️⃣ FBS + HbA1C (Diabetes control)
    # ----------------------
    fbs = test_map.get("FASTING BLOOD SUGAR")
    hba1c = test_map.get("HBA1C")
    if fbs and hba1c:
        used_tests.update(["FASTING BLOOD SUGAR", "HBA1C"])
        fbs_val = fbs["value"]
        hba_val = hba1c["value"]
        fbs_range = fbs["range"]
        hba_range = hba1c["range"]
        fbs_status = high_low_text(fbs_val, fbs_range)
        hba_status = high_low_text(hba_val, hba_range)

        fbs_clean = {k: v for k, v in fbs.items() if k != "advice"}
        hba_clean = {k: v for k, v in hba1c.items() if k != "advice"}

        interpretation_text = (
            f"Your FASTING BLOOD SUGAR is {fbs_val} mg/dL, which is {fbs_status} compared to the normal range of {fbs_range}, "
            f"but your HbA1c is {hba_val}%, which is {hba_status} compared to the normal range of {hba_range}. "
            f"This pattern shows that your blood sugar {'rises at times during the day, but your overall long-term sugar levels are within a normal range' if fbs_status=='high' and hba_status=='normal' else 'needs attention'}. "
            f"These changes can happen due to irregular meal timing, eating high-sugar foods, stress, or not being physically active. "
            f"To manage this, reduce sugar intake, increase physical activity, maintain a healthy weight, and monitor your blood sugar regularly. "
            f"Consult a doctor if high blood sugar persists."
        )

        combined_interpretation_list.append({
            "tests": ["FASTING BLOOD SUGAR", "HBA1C"],
            "results": [fbs_clean, hba_clean],
            "interpretation": interpretation_text
        })

    # ----------------------
    # 2️⃣ LDL + HDL + Total Cholesterol (Cardio risk)
    # ----------------------
    ldl = test_map.get("LDL CHOLESTEROL")
    hdl = test_map.get("HDL CHOLESTEROL")
    tc = test_map.get("TOTAL CHOLESTEROL")
    if ldl and hdl and tc:
        used_tests.update(["LDL CHOLESTEROL", "HDL CHOLESTEROL", "TOTAL CHOLESTEROL"])
        ldl_val, hdl_val, tc_val = ldl["value"], hdl["value"], tc["value"]
        ldl_range, hdl_range, tc_range = ldl["range"], hdl["range"], tc["range"]
        ldl_status = high_low_text(ldl_val, ldl_range)
        hdl_status = high_low_text(hdl_val, hdl_range)
        tc_status = high_low_text(tc_val, tc_range)

        ldl_clean = {k: v for k, v in ldl.items() if k != "advice"}
        hdl_clean = {k: v for k, v in hdl.items() if k != "advice"}
        tc_clean = {k: v for k, v in tc.items() if k != "advice"}

        interpretation_text = (
            f"Your LDL cholesterol is {ldl_val} mg/dL ({ldl_status}), HDL is {hdl_val} mg/dL ({hdl_status}), "
            f"and Total Cholesterol is {tc_val} mg/dL ({tc_status}). "
            f"This combination indicates your cardiovascular risk is "
            f"{'elevated, consider lifestyle changes and consult your doctor' if ldl_status=='high' or hdl_status=='low' or tc_status=='high' else 'within normal limits'}. "
            f"Maintain a healthy diet, regular exercise, and follow up with your doctor as needed."
        )

        combined_interpretation_list.append({
            "tests": ["LDL CHOLESTEROL", "HDL CHOLESTEROL", "TOTAL CHOLESTEROL"],
            "results": [ldl_clean, hdl_clean, tc_clean],
            "interpretation": interpretation_text
        })

    # ----------------------
    # 3️⃣ Creatinine + eGFR (Kidney function)
    # ----------------------
    creat = test_map.get("CREATININE")
    egfr = test_map.get("E-GFR")
    if creat and egfr:
        used_tests.update(["CREATININE", "E-GFR"])
        creat_val, egfr_val = creat["value"], egfr["value"]
        creat_range, egfr_range = creat["range"], egfr["range"]
        creat_status = high_low_text(creat_val, creat_range)
        egfr_status = high_low_text(egfr_val, egfr_range)

        creat_clean = {k: v for k, v in creat.items() if k != "advice"}
        egfr_clean = {k: v for k, v in egfr.items() if k != "advice"}

        interpretation_text = (
            f"Your creatinine is {creat_val} mg/dL ({creat_status}) and eGFR is {egfr_val} ml/min/1.73m2 ({egfr_status}). "
            f"This combination provides insight into kidney function. "
            f"{'Consult a doctor for kidney evaluation' if creat_status=='high' or egfr_status=='low' else 'Your kidney function appears normal.'}"
        )

        combined_interpretation_list.append({
            "tests": ["CREATININE", "E-GFR"],
            "results": [creat_clean, egfr_clean],
            "interpretation": interpretation_text
        })

    # ----------------------
    # 4️⃣ ALT + AST + Bilirubin (Liver panel)
    # ----------------------
    alt = test_map.get("S.G.P.T (ALT)")
    ast = test_map.get("S.G.O.T (AST)")
    bilirubin = test_map.get("TOTAL BILIRUBIN")
    if alt or ast or bilirubin:
        for t in ["S.G.P.T (ALT)", "S.G.O.T (AST)", "TOTAL BILIRUBIN"]:
            if t in test_map: used_tests.add(t)
        alt_val, ast_val, bil_val = (alt["value"] if alt else None,
                                     ast["value"] if ast else None,
                                     bilirubin["value"] if bilirubin else None)
        alt_range, ast_range, bil_range = (alt["range"] if alt else None,
                                           ast["range"] if ast else None,
                                           bilirubin["range"] if bilirubin else None)
        alt_status = high_low_text(alt_val, alt_range) if alt_val is not None else None
        ast_status = high_low_text(ast_val, ast_range) if ast_val is not None else None
        bil_status = high_low_text(bil_val, bil_range) if bil_val is not None else None

        alt_clean = {k: v for k, v in alt.items() if k != "advice"} if alt else None
        ast_clean = {k: v for k, v in ast.items() if k != "advice"} if ast else None
        bil_clean = {k: v for k, v in bilirubin.items() if k != "advice"} if bilirubin else None

        results_list = [x for x in [alt_clean, ast_clean, bil_clean] if x]

        interpretation_text = (
            f"Liver panel results: "
            f"{'ALT ' + str(alt_val) + ' (' + alt_status + ')' if alt_val else ''} "
            f"{'AST ' + str(ast_val) + ' (' + ast_status + ')' if ast_val else ''} "
            f"{'Bilirubin ' + str(bil_val) + ' (' + bil_status + ')' if bil_val else ''}. "
            f"This pattern indicates "
            f"{'possible liver stress, consult a doctor' if (alt_status=='high' or ast_status=='high' or bil_status=='high') else 'normal liver function'}."
        )

        combined_interpretation_list.append({
            "tests": [x["test"] for x in results_list],
            "results": results_list,
            "interpretation": interpretation_text
        })

    # ----------------------
    # Non-combined individual tests
    # ----------------------
    individual_results = []
    for test_name, test_info in test_map.items():
        if test_name not in used_tests:
            individual_results.append(test_info)

    # Build full JSON
    output_json = {
        "filenames": filenames,
        "results": individual_results,  # only non-combination tests
    }

   # Only add combined_interpretation if there are combined results
    if combined_interpretation_list:
        output_json["combined_interpretation"] = combined_interpretation_list

    return output_json
 