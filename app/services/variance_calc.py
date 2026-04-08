def calc_variance(data: dict) -> dict:
    """
    差異計算ロジック（基本版）
    実績原価・標準原価・数量から差異金額を計算する
    """

    actual = float(data.get("actual_cost", 0))
    standard = float(data.get("standard_cost", 0))
    qty = float(data.get("quantity", 0))
    variance_type = data.get("variance_type", "不明")

    # 差異金額 = (実績 - 標準) × 数量
    variance_amount = (actual - standard) * qty

    return {
        "variance_amount": variance_amount,
        "variance_type": variance_type
    }

