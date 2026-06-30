# OpenClaw / Hermes Operations

OpenClaw から Blog Agent Kit に記事作成を頼み、完成物を Hermes が read-only で読み取るための運用メモです。

これは任意運用です。Blog Agent Kit の標準フローは local-first のままで、OpenClaw、Hermes、VPS、Discord、CMS、投稿機能を必須にしません。

## 役割

```text
OpenClaw
  -> VPS 上の /home/ubuntu/blog-agent-kit で記事生成を進める
  -> output/artifacts/<run-id>/ に成果物をまとめる

Local Mac
  -> tmp/pull-vps-artifacts.sh <run-id> で成果物だけ回収する
  -> 必要なら scripts/install-auto-pull-launch-agent.sh で定期回収する

Hermes
  -> 回収済み成果物を read-only で読む
  -> 成功パターン、失敗、改善候補を notes / evidence にまとめる
  -> source repo や公開面は自動変更しない
```

## OpenClaw への依頼テンプレ

```text
/home/ubuntu/blog-agent-kit を使って、note向けブログ記事を作ってください。

テーマ:
「ここに記事テーマ」

読者:
「誰に向けた記事か」

目的:
「読後に何が分かる / 何ができるようになるか」

必ず守ること:
- git pull --ff-only してから作業する。
- Blog Agent Kit の AGENTS.md / CHECKS.md / LOOPS.md を読む。
- 新しい topic を topics/YYYY-MM-DD_slug/ に作る。
- output/ の必須ファイルを埋める。
- review-prompt を使い、2回のローカルレビューとブラッシュアップを行う。
- blog-agent check --topic <topic> --json で missing_outputs が空になるまで確認する。
- 公開、投稿、メール送信、CMS更新、外部アップロードはしない。
- 推測で引用、URL、数字、公開状況を作らない。

成果物:
- run_id は YYYY-MM-DD-short-slug にする。
- output/artifacts/<run_id>/ に成果物をまとめる。
- README.md に topic path、実行した確認コマンド、未解決の注意点を書く。
- check.json を置く。
- review_package.md を置く。
- draft.md、x_posts.md、image_prompts.md、handoff.json、claims_table.md、sources.md、review_round_1.md、review_round_2.md、iteration_log.md を置く。
```

## OpenClaw 側で実行する基本コマンド

```bash
cd /home/ubuntu/blog-agent-kit
git pull --ff-only
python3 scripts/observe_truth.py --json
PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_*.py'

PYTHONPATH=src python3 -m blog_agent_kit.cli init --root . --force
PYTHONPATH=src python3 -m blog_agent_kit.cli new "記事テーマ" --root .
PYTHONPATH=src python3 -m blog_agent_kit.cli prompt --topic topics/YYYY-MM-DD_slug
PYTHONPATH=src python3 -m blog_agent_kit.cli review-prompt --topic topics/YYYY-MM-DD_slug
```

記事を書いた後:

```bash
TOPIC=topics/YYYY-MM-DD_slug
RUN_ID=YYYY-MM-DD-short-slug

PYTHONPATH=src python3 -m blog_agent_kit.cli check --topic "$TOPIC" --json > /tmp/blog-agent-check.json
PYTHONPATH=src python3 -m blog_agent_kit.cli package --topic "$TOPIC" --write

mkdir -p "output/artifacts/$RUN_ID/topic-output"
cp "$TOPIC/brief.yml" "output/artifacts/$RUN_ID/"
cp "$TOPIC/agent-prompt.md" "output/artifacts/$RUN_ID/"
cp "$TOPIC/reviewer-prompt.md" "output/artifacts/$RUN_ID/"
cp "$TOPIC/output/review_package.md" "output/artifacts/$RUN_ID/"
cp "$TOPIC/output/"*.md "output/artifacts/$RUN_ID/topic-output/"
cp "$TOPIC/output/handoff.json" "output/artifacts/$RUN_ID/topic-output/"
cp /tmp/blog-agent-check.json "output/artifacts/$RUN_ID/check.json"

cat > "output/artifacts/$RUN_ID/README.md" <<EOF
# Blog Agent Artifact

run_id: $RUN_ID
topic: $TOPIC
source: /home/ubuntu/blog-agent-kit

Checks:
- python3 scripts/observe_truth.py --json
- PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_*.py'
- PYTHONPATH=src python3 -m blog_agent_kit.cli check --topic $TOPIC --json

External actions:
- publish: no
- post: no
- email: no
- CMS update: no
EOF
```

## ローカルへの回収

ローカル Mac 側で実行します。

```bash
cd /Users/takamasa/Projects/コンテンツ/blog-agent-kit
sh tmp/pull-vps-artifacts.sh <run-id>
```

回収先:

```text
output/remote-artifacts/<run-id>/
```

自動回収を設定済みの場合は、OpenClaw が `output/artifacts/<run-id>/` に成果物を置いたあと、次回の定期pullで `output/remote-artifacts/<run-id>/` に反映されます。自動回収は SSH/rsync のみで、LLMトークンや投稿処理は発生しません。

## Hermes が読む成果物ルール

Hermes は回収済み成果物を read-only で読みます。

優先して読むファイル:

```text
output/remote-artifacts/<run-id>/README.md
output/remote-artifacts/<run-id>/check.json
output/remote-artifacts/<run-id>/review_package.md
output/remote-artifacts/<run-id>/topic-output/draft.md
output/remote-artifacts/<run-id>/topic-output/claims_table.md
output/remote-artifacts/<run-id>/topic-output/sources.md
output/remote-artifacts/<run-id>/topic-output/handoff.json
output/remote-artifacts/<run-id>/topic-output/review_round_1.md
output/remote-artifacts/<run-id>/topic-output/review_round_2.md
output/remote-artifacts/<run-id>/topic-output/iteration_log.md
```

Hermes が出すレビューは、次の形にします。

```text
# Blog Agent Review - <run-id>

## Status
- check result:
- publish-ready:
- requires human review:

## Reusable Lessons
- 成功した手順:
- 再利用できるプロンプト/構成:
- 次回から先に確認すべき条件:

## Issues
- 根拠不足:
- 読者導線の弱さ:
- スタイル/文字数/CTA:
- 画像/X投稿案:

## Improvement Candidates
- blog-agent-kit に反映したい改善:
- Hermes 側の記録ルールに反映したい改善:
- 人間承認が必要な変更:

## Evidence
- 読んだファイル:
- 参照した該当箇所:
```

## Hermes の禁止事項

- 成果物を「モデルの自動学習」として扱わない。
- `blog-agent-kit`、Makimono、Hermes 本体を自動で書き換えない。
- Git commit / push / deploy / publish / post / email / CMS update をしない。
- raw logs や個人情報を無断で深掘りしない。
- `check.json` が失敗している成果物を完成扱いしない。

## 完了条件

- OpenClaw が `output/artifacts/<run-id>/` に成果物をまとめている。
- ローカルに `output/remote-artifacts/<run-id>/` として回収できる。
- `check.json` に `missing_outputs: []` がある。
- Hermes が read-only のレビューを作れる。
- 改善候補は人間確認後にだけ workflow、skill、prompt、repo へ反映する。
