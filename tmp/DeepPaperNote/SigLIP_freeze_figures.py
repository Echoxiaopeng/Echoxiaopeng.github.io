"""Freeze visual review decisions for SigLIP note generation."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, r"C:\Users\kian123\.cursor\skills\deeppapernote\scripts")
from common import file_sha256

path = Path(
    r"C:\Users\kian123\Desktop\cursor_workspace\Echoxiaopeng.github.io\tmp\DeepPaperNote\SigLIP_figure_table_decisions.json"
)
data = json.loads(path.read_text(encoding="utf-8"))

PASS_INSERT = {
    "figure:Figure 1": {
        "decision": "insert",
        "target_section": "方法主线",
        "notes": "三设备 chunked sigmoid 损失示意清晰：本地块、文本轮换、跨设备求和，无正文污染。",
        "preserved": [
            "panels a-d device mesh",
            "I1-I12 T1-T12 similarity blocks",
            "positive diagonal and negative off-diagonal marks",
            "text swap across devices",
            "cross-device sum arrows",
        ],
    },
    "figure:Figure 2": {
        "decision": "insert",
        "target_section": "关键结果",
        "notes": "SigLiT/SigLIP/mSigLIP 三条 batch-size 曲线完整可读，图例与坐标清晰。",
        "preserved": [
            "SigLiT ImageNet 0-shot vs batch size",
            "SigLIP ImageNet 0-shot vs batch size",
            "mSigLIP XM T-to-I 36-lang avg",
            "sigmoid vs softmax legends",
        ],
    },
    "figure:Figure 8": {
        "decision": "insert",
        "target_section": "关键结果",
        "notes": "XM3600 36 语种 I2T/T2I recall@1 柱状图完整，含 *32k 缩放配置。",
        "preserved": [
            "36 language codes plus avg",
            "batch-size color legend including *32k",
            "image-to-text and text-to-image panels",
        ],
    },
    "table:Table 1": {
        "decision": "insert",
        "target_section": "关键结果",
        "notes": "首页 SigLiT/SigLIP 资源与 INet-0 总览表完整，含冻结/解锁标记。",
        "preserved": [
            "SigLiT and SigLIP rows",
            "image text BS TPUv4 days INet-0 columns",
            "frozen and unlocked icons",
        ],
    },
    "table:Table 2": {
        "decision": "insert",
        "target_section": "关键结果",
        "notes": "多语 mSigLIP 不同 batch size 的 INet-0 与 XM 检索表清晰。",
        "preserved": [
            "batch size columns 16k-240k",
            "INet-0 and XM avg/de/en/hi/ru/zh rows",
        ],
    },
    "table:Table 4": {
        "decision": "insert",
        "target_section": "方法主线",
        "notes": "bias b 与 temperature t' 初始化消融表干净可读。",
        "preserved": [
            "b and t-prime init settings",
            "INet-0 Pet-0 C100-0 scores",
            "bold best row b=-10 t'=log10",
        ],
    },
    "table:Table 5": {
        "decision": "insert",
        "target_section": "关键结果",
        "notes": "附录 SigLIP 在 3B/9B seen examples 下 sigmoid vs softmax 分 batch 对照表清晰。",
        "preserved": [
            "3B and 9B seen-example blocks",
            "sigmoid vs softmax columns",
            "batch size rows 512 to 307k",
        ],
    },
    "table:Table 6": {
        "decision": "insert",
        "target_section": "关键结果",
        "notes": "不同 batch 默认/最优 LR 与 WD 超参表短小清晰。",
        "preserved": [
            "BS 8k 16k 32k rows",
            "Default Best Best LR Best WD columns",
        ],
    },
    "table:Table 8": {
        "decision": "insert",
        "target_section": "关键结果",
        "notes": "SigLiT 跨 seen-examples 与 batch size 的 sigmoid/softmax 对照表完整。",
        "preserved": [
            "450M 900M 3B 18B blocks",
            "sigmoid softmax subcolumns",
            "batch rows up to 1024k",
        ],
    },
}

FAIL_DEFECT = {
    "table:Table 9": {
        "failure_reason": "unreadable_source",
        "notes": "36 语种双任务全表字号过密，嵌入笔记后关键数字难以可靠识读；正文用 Table 2 与 Figure 8 及关键均值叙述。",
        "preserved": ["36-language bilingual retrieval grid"],
        "omitted": ["legible per-cell numeric reading at note embed size"],
        "attempts": 0,
    },
}


def make_pass(sha: str, notes: str, preserved: list[str]) -> dict:
    return {
        "status": "pass",
        "reviewed_asset_sha256": sha,
        "preserved_scientific_elements": preserved,
        "omitted_scientific_elements": [],
        "notes": notes,
        "failure_reason": "",
        "repair_attempts": 0,
        "revised_bbox": [],
    }


def make_fail(sha: str, cfg: dict) -> dict:
    return {
        "status": "fail",
        "reviewed_asset_sha256": sha,
        "preserved_scientific_elements": cfg["preserved"],
        "omitted_scientific_elements": cfg["omitted"],
        "notes": cfg["notes"],
        "failure_reason": cfg["failure_reason"],
        "repair_attempts": cfg["attempts"],
        "revised_bbox": [],
    }


for item in data["decisions"]:
    item_id = item.get("item_id", "")
    if item_id in PASS_INSERT:
        cfg = PASS_INSERT[item_id]
        src = item.get("source_image_path", "")
        sha = file_sha256(src)
        item["decision"] = cfg["decision"]
        item["target_section"] = cfg["target_section"]
        item["source_image_sha256"] = sha
        item["visual_review"] = make_pass(sha, cfg["notes"], cfg["preserved"])
        item["materialization_status"] = "pending"
        item["skip_reason"] = ""
    elif item_id in FAIL_DEFECT:
        cfg = FAIL_DEFECT[item_id]
        src = item.get("source_image_path", "")
        sha = file_sha256(src) if src else ""
        item["decision"] = "visual_defect"
        item["skip_reason"] = "visual_quality_gate_rejected_candidate"
        if sha:
            item["source_image_sha256"] = sha
        item["visual_review"] = make_fail(sha, cfg)
        item["materialization_status"] = "skipped"

pending = [i["item_id"] for i in data["decisions"] if i.get("decision") == "review_pending"]
if pending:
    raise SystemExit(f"still pending: {pending}")

# refresh summary
from collections import Counter

counts = Counter(i.get("decision") for i in data["decisions"])
data["summary"] = {
    "total_items": len(data["decisions"]),
    "by_decision": {
        k: counts.get(k, 0)
        for k in ("insert", "low_priority", "placeholder", "review_pending", "skip", "visual_defect")
    },
}

path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("frozen", [(i["item_id"], i["decision"], i.get("target_section", "")) for i in data["decisions"]])
print("summary", data["summary"])
