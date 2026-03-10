import re
from .config import TEST_ALIASES


def generate_full_combined_interpretation(results, filenames):
    """
    Generate detailed combined interpretation JSON for lab results.

    Args:
        results: list of dicts with keys like:
            test, value, unit, range, meaning, advice
        filenames: list of report image/file names

    Returns:
        dict with:
            filenames
            results (only non-combined individual tests)
            combined_interpretation (if any)
    """

    def normalize_test_name(name):
        """Basic normalization."""
        if not name:
            return ""
        name = str(name).strip().upper()
        name = name.replace(".", "")
        name = name.replace("_", " ")
        name = re.sub(r"\s+", " ", name)
        return name

    def simplify_test_name(name):
        """
        Strong normalization for OCR-tolerant matching.
        Removes spaces and punctuation.
        """
        name = normalize_test_name(name)
        name = re.sub(r"[^A-Z0-9]", "", name)
        return name

    def clean_result(result):
        """Remove advice field from combined result entries."""
        return {k: v for k, v in result.items() if k != "advice"}

    def high_low_text(value, range_str):
        """Return 'high', 'low', or 'normal' based on numeric range."""
        try:
            if value is None or range_str is None:
                return "normal"

            cleaned_range = str(range_str).replace(" ", "")
            if "-" not in cleaned_range:
                return "normal"

            low, high = [float(x) for x in cleaned_range.split("-")]
            numeric_value = float(value)

            if numeric_value < low:
                return "low"
            elif numeric_value > high:
                return "high"
            return "normal"
        except Exception:
            return "normal"

    def build_alias_lookup():
        """
        Build canonical alias lookup from TEST_ALIASES in config.py
        """
        alias_lookup = {}

        for canonical_name, aliases in TEST_ALIASES.items():
            all_names = [canonical_name] + aliases
            for alias in all_names:
                alias_lookup[simplify_test_name(alias)] = canonical_name

        return alias_lookup

    def find_canonical_test(results_list, canonical_name, alias_lookup):
        """
        Find a test result by canonical name using:
        1. exact alias matching
        2. OCR-tolerant contains matching
        """
        canonical_aliases = TEST_ALIASES.get(canonical_name, [])
        alias_simples = {simplify_test_name(canonical_name)}
        alias_simples.update(simplify_test_name(a) for a in canonical_aliases)

        for item in results_list:
            raw_name = item.get("test", "")
            simplified_raw = simplify_test_name(raw_name)
            normalized_raw = normalize_test_name(raw_name)

            # Exact simplified match
            if simplified_raw in alias_simples:
                return item

            # Resolved alias lookup
            resolved = alias_lookup.get(simplified_raw)
            if resolved == canonical_name:
                return item

            # OCR-tolerant fuzzy rules for important tests
            if canonical_name == "POST PRANDIAL BLOOD GLUCOSE":
                if (
                    ("PRANDIAL" in normalized_raw and "GLUCOSE" in normalized_raw)
                    or ("PRANDIAL" in normalized_raw and "SUGAR" in normalized_raw)
                    or ("PPBS" in normalized_raw)
                    or ("POSTPRANDIAL" in simplified_raw and ("GLUCOSE" in simplified_raw or "SUGAR" in simplified_raw))
                    or ("OSTPRANDIALBLOODGLUCOSE" in simplified_raw)
                    or ("OSTPRANDIALBLOODSUGAR" in simplified_raw)
                ):
                    return item

            if canonical_name == "FASTING BLOOD SUGAR":
                if (
                    ("FASTING" in normalized_raw and "SUGAR" in normalized_raw)
                    or ("FASTING" in normalized_raw and "GLUCOSE" in normalized_raw)
                    or simplified_raw == "FBS"
                ):
                    return item

            if canonical_name == "HBA1C":
                if "HBA1C" in normalized_raw or "A1C" in normalized_raw:
                    return item

            if canonical_name == "E-GFR":
                if "EGFR" in simplified_raw or "EGFR" in normalized_raw.replace("-", ""):
                    return item

            if canonical_name == "S.G.P.T (ALT)":
                if "SGPT" in simplified_raw or normalized_raw == "ALT":
                    return item

            if canonical_name == "S.G.O.T (AST)":
                if "SGOT" in simplified_raw or normalized_raw == "AST":
                    return item

        return None

    alias_lookup = build_alias_lookup()
    used_tests = set()
    combined_interpretation_list = []

    # ----------------------
    # 1️⃣ Sugar profile combinations
    # Priority:
    # 1. FBS + HbA1C + PPBS
    # 2. FBS + HbA1C
    # 3. FBS + PPBS
    # 4. HbA1C + PPBS
    # ----------------------
    fbs = find_canonical_test(results, "FASTING BLOOD SUGAR", alias_lookup)
    hba1c = find_canonical_test(results, "HBA1C", alias_lookup)
    ppbs = find_canonical_test(results, "POST PRANDIAL BLOOD GLUCOSE", alias_lookup)

    if fbs and hba1c and ppbs:
        used_tests.update({
            normalize_test_name(fbs["test"]),
            normalize_test_name(hba1c["test"]),
            normalize_test_name(ppbs["test"]),
        })

        fbs_val = fbs.get("value")
        hba_val = hba1c.get("value")
        ppbs_val = ppbs.get("value")

        fbs_range = fbs.get("range")
        hba_range = hba1c.get("range")
        ppbs_range = ppbs.get("range")

        fbs_status = high_low_text(fbs_val, fbs_range)
        hba_status = high_low_text(hba_val, hba_range)
        ppbs_status = high_low_text(ppbs_val, ppbs_range)

        fbs_clean = clean_result(fbs)
        hba_clean = clean_result(hba1c)
        ppbs_clean = clean_result(ppbs)

        if fbs_status == "normal" and hba_status == "normal" and ppbs_status == "normal":
            sugar_pattern = "your fasting, post-meal, and long-term blood sugar control are all within the normal range"
        elif fbs_status == "high" and hba_status == "normal" and ppbs_status == "normal":
            sugar_pattern = "your fasting blood sugar is high, but your post-meal and long-term sugar levels are still within the normal range"
        elif fbs_status == "normal" and hba_status == "normal" and ppbs_status == "high":
            sugar_pattern = "your blood sugar rises mainly after meals, while fasting and long-term sugar levels remain within the normal range"
        elif fbs_status == "high" and ppbs_status == "high" and hba_status == "normal":
            sugar_pattern = "both your fasting and post-meal sugar levels are high, but your long-term sugar average is still within the normal range, which may suggest an early blood sugar imbalance"
        elif hba_status == "high" and (fbs_status == "normal" or ppbs_status == "normal"):
            sugar_pattern = "your long-term blood sugar average is high, which suggests that your blood sugar has been elevated over the past 2 to 3 months even if one of the current readings is normal"
        elif fbs_status == "high" and hba_status == "high" and ppbs_status == "high":
            sugar_pattern = "your fasting, post-meal, and long-term blood sugar levels are all high, which suggests persistent poor blood sugar control"
        else:
            sugar_pattern = "your blood sugar control needs attention"

        interpretation_text = (
            f"This pattern shows that {sugar_pattern}. "
            f"These changes can happen due to irregular meal timing, eating high-sugar foods, insulin resistance, stress, or not being physically active. "
            f"To manage this, reduce sugar intake, increase physical activity, maintain a healthy weight, and monitor your blood sugar regularly. "
            f"Consult a doctor if abnormal blood sugar levels persist."
        )

        combined_interpretation_list.append({
            "tests": [fbs["test"], hba1c["test"], ppbs["test"]],
            "results": [fbs_clean, hba_clean, ppbs_clean],
            "interpretation": interpretation_text
        })

    elif fbs and hba1c:
        used_tests.update({
            normalize_test_name(fbs["test"]),
            normalize_test_name(hba1c["test"]),
        })

        fbs_val = fbs.get("value")
        hba_val = hba1c.get("value")
        fbs_range = fbs.get("range")
        hba_range = hba1c.get("range")

        fbs_status = high_low_text(fbs_val, fbs_range)
        hba_status = high_low_text(hba_val, hba_range)

        fbs_clean = clean_result(fbs)
        hba_clean = clean_result(hba1c)

        if fbs_status == "high" and hba_status == "high":
            sugar_pattern = "both your fasting blood sugar and long-term blood sugar average are high, which suggests that elevated glucose levels may have been present for some time"
        elif fbs_status == "high" and hba_status == "normal":
            sugar_pattern = "your fasting blood sugar is high, while your long-term blood sugar average remains within the normal range, which may suggest an early change in glucose control"
        elif fbs_status == "normal" and hba_status == "high":
            sugar_pattern = "your long-term blood sugar average is high even though your current fasting blood sugar is within the normal range"
        else:
            sugar_pattern = "your fasting and long-term blood sugar values are within the normal range"

        interpretation_text = (
            f"This pattern suggests that {sugar_pattern}. "
            f"These changes may occur due to long-term elevated glucose levels, insulin resistance, high carbohydrate intake, or reduced glucose regulation by the body. "
            f"To manage this, reduce sugar intake, increase physical activity, maintain a healthy weight, and monitor your blood sugar regularly. "
            f"Consult a doctor if high blood sugar persists."
        )

        combined_interpretation_list.append({
            "tests": [fbs["test"], hba1c["test"]],
            "results": [fbs_clean, hba_clean],
            "interpretation": interpretation_text
        })

    elif fbs and ppbs:
        used_tests.update({
            normalize_test_name(fbs["test"]),
            normalize_test_name(ppbs["test"]),
        })

        fbs_val = fbs.get("value")
        ppbs_val = ppbs.get("value")
        fbs_range = fbs.get("range")
        ppbs_range = ppbs.get("range")

        fbs_status = high_low_text(fbs_val, fbs_range)
        ppbs_status = high_low_text(ppbs_val, ppbs_range)

        fbs_clean = clean_result(fbs)
        ppbs_clean = clean_result(ppbs)

        interpretation_text = (
            f"Your FASTING BLOOD SUGAR is {fbs_val} {fbs.get('unit', '')}, which is {fbs_status} compared to the normal range of {fbs_range}, "
            f"and your {ppbs.get('test', 'POST PRANDIAL BLOOD GLUCOSE')} is {ppbs_val} {ppbs.get('unit', '')}, which is {ppbs_status} compared to the normal range of {ppbs_range}. "
            f"This pattern shows that your blood sugar "
            f"{'is elevated both in the fasting state and after meals, which suggests poor current blood sugar control' if fbs_status == 'high' and ppbs_status == 'high' else 'may be rising mainly after meals or during fasting, which needs attention'}. "
            f"These changes can happen due to irregular meal timing, eating excess carbohydrates, stress, or lack of physical activity. "
            f"To manage this, reduce sugar intake, improve meal planning, exercise regularly, maintain a healthy weight, and monitor your blood sugar. "
            f"Consult a doctor if abnormal blood sugar values continue."
        )

        combined_interpretation_list.append({
            "tests": [fbs["test"], ppbs["test"]],
            "results": [fbs_clean, ppbs_clean],
            "interpretation": interpretation_text
        })

    elif hba1c and ppbs:
        used_tests.update({
            normalize_test_name(hba1c["test"]),
            normalize_test_name(ppbs["test"]),
        })

        hba_val = hba1c.get("value")
        ppbs_val = ppbs.get("value")
        hba_range = hba1c.get("range")
        ppbs_range = ppbs.get("range")

        hba_status = high_low_text(hba_val, hba_range)
        ppbs_status = high_low_text(ppbs_val, ppbs_range)

        hba_clean = clean_result(hba1c)
        ppbs_clean = clean_result(ppbs)

        interpretation_text = (
            f"Your HbA1c is {hba_val} {hba1c.get('unit', '')}, which is {hba_status} compared to the normal range of {hba_range}, "
            f"and your {ppbs.get('test', 'POST PRANDIAL BLOOD GLUCOSE')} is {ppbs_val} {ppbs.get('unit', '')}, which is {ppbs_status} compared to the normal range of {ppbs_range}. "
            f"This pattern shows that your blood sugar "
            f"{'rises after meals and may be affecting your long-term sugar control' if ppbs_status == 'high' or hba_status == 'high' else 'is currently within the normal range both after meals and over the long term'}. "
            f"These changes can happen due to high-sugar meals, insulin resistance, stress, or not being physically active. "
            f"To manage this, reduce sugar intake, improve meal choices, exercise regularly, maintain a healthy weight, and monitor your blood sugar regularly. "
            f"Consult a doctor if abnormal blood sugar levels persist."
        )

        combined_interpretation_list.append({
            "tests": [hba1c["test"], ppbs["test"]],
            "results": [hba_clean, ppbs_clean],
            "interpretation": interpretation_text
        })

    # ----------------------
    # 2️⃣ LDL + HDL + Total Cholesterol
    # ----------------------
    ldl = find_canonical_test(results, "LDL CHOLESTEROL", alias_lookup)
    hdl = find_canonical_test(results, "HDL CHOLESTEROL", alias_lookup)
    tc = find_canonical_test(results, "TOTAL CHOLESTEROL", alias_lookup)

    if ldl and hdl and tc:
        used_tests.update({
            normalize_test_name(ldl["test"]),
            normalize_test_name(hdl["test"]),
            normalize_test_name(tc["test"]),
        })

        ldl_val, hdl_val, tc_val = ldl.get("value"), hdl.get("value"), tc.get("value")
        ldl_range, hdl_range, tc_range = ldl.get("range"), hdl.get("range"), tc.get("range")

        ldl_status = high_low_text(ldl_val, ldl_range)
        hdl_status = high_low_text(hdl_val, hdl_range)
        tc_status = high_low_text(tc_val, tc_range)

        ldl_clean = clean_result(ldl)
        hdl_clean = clean_result(hdl)
        tc_clean = clean_result(tc)

        interpretation_text = (
            f"Your LDL cholesterol is {ldl_val} {ldl.get('unit', '')} ({ldl_status}), "
            f"HDL is {hdl_val} {hdl.get('unit', '')} ({hdl_status}), "
            f"and Total Cholesterol is {tc_val} {tc.get('unit', '')} ({tc_status}). "
            f"This combination indicates your cardiovascular risk is "
            f"{'elevated, consider lifestyle changes and consult your doctor' if ldl_status == 'high' or hdl_status == 'low' or tc_status == 'high' else 'within normal limits'}. "
            f"Maintain a healthy diet, regular exercise, and follow up with your doctor as needed."
        )

        combined_interpretation_list.append({
            "tests": [ldl["test"], hdl["test"], tc["test"]],
            "results": [ldl_clean, hdl_clean, tc_clean],
            "interpretation": interpretation_text
        })

    # ----------------------
    # 3️⃣ Creatinine + eGFR
    # ----------------------
    creat = find_canonical_test(results, "CREATININE", alias_lookup)
    egfr = find_canonical_test(results, "E-GFR", alias_lookup)

    if creat and egfr:
        used_tests.update({
            normalize_test_name(creat["test"]),
            normalize_test_name(egfr["test"]),
        })

        creat_val, egfr_val = creat.get("value"), egfr.get("value")
        creat_range, egfr_range = creat.get("range"), egfr.get("range")

        creat_status = high_low_text(creat_val, creat_range)
        egfr_status = high_low_text(egfr_val, egfr_range)

        creat_clean = clean_result(creat)
        egfr_clean = clean_result(egfr)

        interpretation_text = (
            f"Your creatinine is {creat_val} {creat.get('unit', '')} ({creat_status}) "
            f"and eGFR is {egfr_val} {egfr.get('unit', '')} ({egfr_status}). "
            f"This combination provides insight into kidney function. "
            f"{'Consult a doctor for kidney evaluation' if creat_status == 'high' or egfr_status == 'low' else 'Your kidney function appears normal.'}"
        )

        combined_interpretation_list.append({
            "tests": [creat["test"], egfr["test"]],
            "results": [creat_clean, egfr_clean],
            "interpretation": interpretation_text
        })

    # ----------------------
    # 4️⃣ ALT + AST + Bilirubin
    # ----------------------
    alt = find_canonical_test(results, "S.G.P.T (ALT)", alias_lookup)
    ast = find_canonical_test(results, "S.G.O.T (AST)", alias_lookup)
    bilirubin = find_canonical_test(results, "TOTAL BILIRUBIN", alias_lookup)

    if alt or ast or bilirubin:
        present_results = []

        for item in [alt, ast, bilirubin]:
            if item:
                used_tests.add(normalize_test_name(item["test"]))
                present_results.append(clean_result(item))

        alt_val = alt.get("value") if alt else None
        ast_val = ast.get("value") if ast else None
        bil_val = bilirubin.get("value") if bilirubin else None

        alt_range = alt.get("range") if alt else None
        ast_range = ast.get("range") if ast else None
        bil_range = bilirubin.get("range") if bilirubin else None

        alt_status = high_low_text(alt_val, alt_range) if alt else None
        ast_status = high_low_text(ast_val, ast_range) if ast else None
        bil_status = high_low_text(bil_val, bil_range) if bilirubin else None

        parts = []
        if alt:
            parts.append(f"ALT {alt_val} {alt.get('unit', '')} ({alt_status})")
        if ast:
            parts.append(f"AST {ast_val} {ast.get('unit', '')} ({ast_status})")
        if bilirubin:
            parts.append(f"Bilirubin {bil_val} {bilirubin.get('unit', '')} ({bil_status})")

        abnormal_liver = any(status == "high" for status in [alt_status, ast_status, bil_status] if status is not None)

        interpretation_text = (
            f"Liver panel results: {', '.join(parts)}. "
            f"This pattern indicates "
            f"{'possible liver stress, consult a doctor' if abnormal_liver else 'normal liver function'}."
        )

        combined_interpretation_list.append({
            "tests": [r["test"] for r in present_results],
            "results": present_results,
            "interpretation": interpretation_text
        })

    # ----------------------
    # Non-combined individual tests
    # ----------------------
    individual_results = []
    for test_info in results:
        original_test_name = normalize_test_name(test_info.get("test", ""))
        if original_test_name not in used_tests:
            individual_results.append(test_info)

    output_json = {
        "filenames": filenames,
        "results": individual_results,
    }

    if combined_interpretation_list:
        output_json["combined_interpretation"] = combined_interpretation_list

    return output_json 