# 第6回 解答

## 演習

- STEP 1 のツールの名前：
  - 従来のエージェント：`search_materials`
  - MCP対応エージェント：`glossary_search_glossary`

- STEP 2 の [tool call]：
  - `glossary_search_glossary({'query': '3レベル'})`

- STEP 3 の [tool call]：
  - `fetch_fetch({'url': 'https://modelcontextprotocol.io/'})`

- STEP 4 の [tool call]：
  - `aws_aws___search_documentation({'search_phrase': 'Amazon S3 versioning overview'})`

- 気づき・疑問：
  - 従来のエージェントでは関数を直接登録していたが、MCPではサーバー側が公開するツールをエージェントが取得し、同じ形式で利用できることを確認した。
  - `uvx` によるローカルMCPサーバーの起動と、URL指定によるリモートMCPサーバーへの接続を試し、設定ファイルの変更だけでツールを追加できた。
  - MCPによるツールの共通化は、複数のAIエージェントで同じ情報源を利用する際に有効だと感じた。一方、外部MCPサーバーの説明文や権限、送信するデータの管理には注意が必要だと考えた。

## 宿題

- 取り組んだレベル：実装

- やったこと：
  - 第3回で作成した `make_quiz` をGit履歴から復元し、`app/tools.py` に追加した。
  - `app/mcp_server.py` で `make_quiz` と `get_lecture_summary` をMCPツールとして公開した。
  - 存在しない講義回が指定された場合、利用可能な講義回を提示するようエラー処理を改善した。
  - `--trace` を利用し、第2回のクイズ生成と存在しない第99回を指定した場合の動作を確認した。

- 結果：
  - MCP経由で利用可能なツールが7個から9個に増え、`glossary_make_quiz` と `glossary_get_lecture_summary` が追加された。
  - 正常系では `glossary_make_quiz({'lecture': 2})` が呼び出され、LoRAのランクに関する確認問題が生成された。
  - 異常系では `glossary_make_quiz({'lecture': 99})` が呼び出され、「第99回の用語は登録されていません。利用可能な講義回: 1, 2, 3, 4, 6。」というメッセージが返された。
  - モデルは存在しない問題を生成せず、利用可能な講義回を案内した。
  - `uv run pytest -q` で22件すべてのテストに成功した。

- 気づき・疑問：
  - 既存のPython関数をMCPサーバーに登録するだけで、エージェント側のコードを変更せずに機能を追加できることが分かった。
  - エラーを単に通知するのではなく、利用可能な選択肢を返すことで、モデルが適切な代替案を提示できることを確認した。
  - ネットワーク機器の設定情報やメーカーの技術資料などをMCP経由で参照できれば、複数のエージェントから共通の情報源を活用できると考えた。一方、ツールの権限管理や取得情報の正確性をどのように担保するかが今後の課題だと感じた。