#!/usr/bin/env bash
# 把某個 claude/* 分支上、main 還沒有的 reports/YYYY-MM-DD[-n].html 同步進目前所在分支（main）。
# 用法：scripts/sync_reports.sh <來源分支名>
# 只新增、從不覆蓋：main 已有的日報一律略過；最後重建 reports/index.html。
set -euo pipefail
BRANCH="${1:?usage: sync_reports.sh <source-branch>}"
SRC="origin/${BRANCH}"
added=()
while IFS= read -r f; do
  if ! git cat-file -e "HEAD:${f}" 2>/dev/null; then added+=("$f"); fi
done < <(git ls-tree -r --name-only "$SRC" -- reports | grep -E '^reports/[0-9]{4}-[0-9]{2}-[0-9]{2}(-[0-9]+)?\.html$' || true)
if [ "${#added[@]}" -eq 0 ]; then echo "沒有新的日報可同步"; exit 0; fi
git checkout "$SRC" -- "${added[@]}"
python3 scripts/publish_report.py --rebuild-index >/dev/null
git add -- reports
if git diff --cached --quiet; then echo "沒有變更"; exit 0; fi
git -c user.name="github-actions[bot]" -c user.email="41898282+github-actions[bot]@users.noreply.github.com" \
  commit -q -m "Sync ${#added[@]} report(s) from ${BRANCH}"
echo "synced: ${added[*]}"
