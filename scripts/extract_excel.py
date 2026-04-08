import openpyxl
import re

# 理由文っぽい列名の候補
REASON_COL_KEYWORDS = [
    "理由", "原因", "要因", "コメント", "備考", "説明", "背景", "詳細"
]

def looks_like_reason(text: str) -> bool:
    """理由文として成立しているかの判定"""
    if not text:
        return False
    if len(text) < 5:
        return False
    if re.fullmatch(r"[0-9\.\-]+", text):
        return False
    if len(re.sub(r"[0-9\.\-]", "", text)) == 0:
        return False
    return True

def extract_text_from_excel(filepath: str):
    """
    Excel から「理由文らしいテキスト」を抽出する強化版
    """
    texts = []

    try:
        wb = openpyxl.load_workbook(filepath, data_only=True)

        for sheet in wb.worksheets:
            rows = list(sheet.iter_rows(values_only=True))
            if not rows:
                continue

            header = rows[0]
            reason_cols = []

            # ① 理由文っぽい列を推定
            for idx, col_name in enumerate(header):
                if not col_name:
                    continue
                col_name = str(col_name)
                if any(key in col_name for key in REASON_COL_KEYWORDS):
                    reason_cols.append(idx)

            # ② 見つからなければ全列を対象に fallback
            if not reason_cols:
                reason_cols = list(range(len(header)))

            # ③ 抽出
            for row in rows[1:]:
                for col_idx in reason_cols:
                    if col_idx >= len(row):
                        continue
                    cell = row[col_idx]
                    if not cell:
                        continue

                    text = str(cell).strip()
                    if looks_like_reason(text):
                        texts.append(text)

        return texts

    except Exception as e:
        return [f"Excel抽出エラー: {str(e)}"]

