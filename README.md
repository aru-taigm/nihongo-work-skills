# nihongo-work-skills

**日本の仕事で毎日使う文書を、Claude に任せるための Agent Skills 集。**
議事録、請求書（インボイス対応）、見積書、稟議書、敬語メール、確定申告の下ごしらえまで。20 本、すべて入力例と出力例つきで、構造をテストで検証しています。

*English: Claude Agent Skills for everyday Japanese business documents (minutes, invoices with Japan's qualified-invoice rules, quotations, ringi proposals, keigo emails, tax-return prep, ...). Each skill ships with a worked example and is validated by tests.*

## できること

<!-- skills:start -->
| スキル | できること |
|---|---|
| `jp-apology-email` | ミスや遅延について、相手の信頼を損なわないお詫びのメール・文書を書く |
| `jp-business-email` | 要件から、社外・社内向けの自然な敬語のビジネスメールを書く |
| `jp-contract-check` | 業務委託契約・NDA・利用規約などの日本語の契約書について、確認すべき論点と不利な条項を洗い出す |
| `jp-daily-report` | 一日の作業メモから、上司や同僚が読みやすい日報を作る |
| `jp-entry-sheet` | 就職・転職の志望動機、ガクチカ、自己PRなどのエントリーシート（ES）の文章を、具体例と企業への接続が伝わる形で書く・直す |
| `jp-expense-report` | 出張や立替の領収書・メモから、経理に差し戻されにくい経費精算書を作る |
| `jp-invoice` | 日本のインボイス制度（適格請求書）の記載事項を満たした請求書の内容を作る・点検する |
| `jp-job-posting` | 採用したい人物像・業務内容から、応募が集まりやすい日本語の求人票・募集要項を書く |
| `jp-meeting-minutes` | 会議のメモ・文字起こし・箇条書きから、決定事項とToDoが一目で分かる日本語の議事録を作る |
| `jp-press-release` | 新サービスや発表内容から、日本のメディア向けのプレスリリース（タイトル、リード文、本文、会社概要）を書く |
| `jp-proposal-doc` | 企画・提案の内容から、課題・解決策・効果・スケジュール・費用が通る順で並んだ日本語の企画書の構成と本文を作る |
| `jp-quotation` | 依頼内容から日本のビジネス慣行に沿った見積書の内容を作る |
| `jp-request-email` | 相手に何かを頼む・お願いする丁寧なメール（依頼、日程調整、資料送付の依頼、お断りを含む返信）を書く |
| `jp-ringi` | 日本の会社で使う稟議書（購入・契約・採用・予算の承認申請）を、決裁者が判断しやすい形で書く |
| `jp-sop-manual` | 業務のやり方のメモから、新人が一人で再現できる手順書・業務マニュアルを日本語で作る |
| `jp-tax-return-prep` | 個人事業主・フリーランスの確定申告に向けて、売上と経費を勘定科目に仕分けし、不足書類や相談点を洗い出す |
| `jp-thanks-letter` | 商談後、面接後、お世話になった相手へのお礼のメール・手紙を、定型文ではなく具体的な内容で書く |
| `jp-translate-business` | 日本語と英語のビジネス文書・メールを、相手との関係と目的に合わせて翻訳する |
| `jp-weekly-report` | 一週間の作業・数字・課題から、上司やチームに送る週報を作る |
| `jp-work-history` | 経歴のメモから、日本の転職で使う職務経歴書（職務要約・職務経歴・活かせる経験・自己PR）を、成果が伝わる形で書く |
<!-- skills:end -->

## 入れ方

```bash
git clone https://github.com/aru-taigm/nihongo-work-skills
cd nihongo-work-skills
python scripts/install.py              # ~/.claude/skills に全部入れる
python scripts/install.py --project    # このプロジェクトだけ（./.claude/skills）
python scripts/install.py jp-invoice jp-ringi   # 必要なものだけ
```

入れたら Claude Code を開き直し、「議事録を作って」「請求書をインボイス対応で作って」のように頼むだけです。スキル名を覚える必要はありません。

## 他の日本語スキルとの違い

- **網羅**：議事録や敬語メールだけでなく、請求書、見積書、稟議、確定申告、契約書の確認、求人票まで、仕事の書類を広くそろえています。
- **作り話をしない**：どのスキルにも「入力に無い数字や固有名詞を作らない。足りなければ聞く」を入れています。
- **例つき**：すべてに入力と出力の例があり、期待する出力が一目で分かります。
- **テスト済み**：名前、説明文、必須の見出し、例の有無を CI で検証します。壊れたスキルは入りません。

## 使うときの注意

税務・法務・労務に関わるスキル（`jp-invoice`、`jp-tax-return-prep`、`jp-contract-check`）は、下ごしらえと論点の洗い出しまでです。制度は改正されるため、最終判断は国税庁などの最新の案内や、税理士・弁護士で確認してください。

## 作る・直す

```bash
python scripts/build_index.py          # この表を skills/ から作り直す
python -m unittest discover -s tests -v
```

新しいスキルは `skills/jp-〇〇/SKILL.md` を追加します。必須の見出しは「先に確認すること」「手順」「出力形式」「例」「注意」です。

## ライセンス

MIT
