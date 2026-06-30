# VPS Artifact Workflow

VPS 上の clone で重い処理を実行し、記事レビュー用 bundle、画像、動画、ZIP などの成果物だけをローカルへ戻すための任意運用です。

Blog Agent Kit の標準方針は local-first です。この手順は、長時間の生成、動画レンダリング、大きな ZIP 作成など、ローカル Mac で実行しにくい処理を VPS に逃がす場合だけ使います。

## 考え方

```text
local repo
  -> git push
GitHub private repo
  -> git clone / git pull
VPS clone
  -> generate files under output/artifacts/<run-id>/
local output/remote-artifacts/<run-id>/
  <- rsync / scp pull
```

VPS はローカルのファイルを直接編集しません。VPS 側の作業コピーで処理し、完成した成果物だけをローカルにコピーします。

## 前提

- ローカル repo の必要な変更が GitHub に push 済み。
- VPS から private repo を clone / pull できる。
- ローカル Mac から VPS へ SSH 接続できる。
- ローカル Mac に `rsync` がある。
- 秘密情報、実ホスト名、個人パスは repo に commit しない。

## VPS 側の準備

```bash
git clone https://github.com/Takamasa045/blog-agent-kit.git
cd blog-agent-kit
python3 scripts/observe_truth.py --json
PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_*.py'
```

既に clone 済みなら:

```bash
cd blog-agent-kit
git pull --ff-only
python3 scripts/observe_truth.py --json
PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_*.py'
```

## VPS 側で成果物を作る

成果物は Git 管理対象にせず、VPS 側の `output/artifacts/<run-id>/` に置きます。

```bash
mkdir -p output/artifacts/2026-06-30-demo
```

記事 bundle、画像、動画、ZIP などの出力先を、このディレクトリに向けます。成果物の横に、できれば確認用のメモも置きます。

```bash
printf '%s\n' "source: VPS clone" > output/artifacts/2026-06-30-demo/README.txt
```

## ローカルへ成果物だけ戻す

ローカル側で実行します。

```bash
sh scripts/pull-remote-artifacts.sh \
  user@host.example \
  /home/user/blog-agent-kit/output/artifacts/2026-06-30-demo \
  output/remote-artifacts/2026-06-30-demo
```

この script は、記事、画像、音声、動画、ZIP、JSON、Markdown、text、CSV 系だけをコピーします。`--delete` は使わないため、ローカル成果物を消しません。

## やらないこと

- VPS からローカル repo を直接マウントして編集しない。
- `rsync --delete` で双方向同期しない。
- `.git/`、仮想環境、認証情報、キャッシュを成果物としてコピーしない。
- 大きな動画や ZIP を通常の commit に入れない。
- Blog Agent Kit の標準フローに VPS 必須の前提を混ぜない。

## 完了確認

- VPS 側 clone で対象処理が完了している。
- 成果物が `output/artifacts/<run-id>/` にまとまっている。
- ローカルの `output/remote-artifacts/<run-id>/` に必要ファイルだけコピーされている。
- ローカル repo の `git status --short` に、成果物コピー由来の tracked 変更が出ていない。
- 必要なら、成果物のハッシュ、サイズ、再生成手順を README.txt などに残している。
