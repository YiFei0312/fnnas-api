# util

> 自动生成（`python tools/gen_api.py`），共 3 个接口。
> 调用示例：`await client.api.util.crypto_get_rsa_pub(...)`

| 方法 | req | 状态 | 只读 | 已知参数 | 响应字段 |
| --- | --- | --- | --- | --- | --- |
| `crypto_get_rsa_pub` | `util.crypto.getRSAPub` | 已实测通过 | ✅ | - | pub, si |
| `get_si` | `util.getSI` | 已实测通过 | ✅ | - | si |
| `trimacl_notify` | `util.trimaclNotify` | 未实测（写接口） | ⚠️ | - | - |

## 实测样例

### util.crypto.getRSAPub

状态：已实测通过，耗时 4.6ms

```json
{
  "pub": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA3MDkjICvGpYwL4ZUzgLp\nWkZPQwLf/AglHfBPqE5XzbhdGEuyPUzD9eQEXO5GwqalGYO78/iyQ7kFngxANoQA\nuDeIGHRc6QOfVIAITeSySb94i497xu0nisVjjoayqI8L+DQAGKIp1W29CwxU95Vl\ncMlcD7PLyWDpN6S2zAiFrO+roxnjkmSJjGqS9yaW2bFfstyxkFPYeJ8kWPYXfwtb\nisFD5o+h2a66gIO3vucKwv9aK3VKciapdL3k+tCQ1cOG1FugJ9jhtP1aZEqS0Xos\nBeDTrDXoFWI1WdaVACJLumNkuhdeU9DovzELOV20PQXpicobK1gskiI43w6omw+1\n/QIDAQAB\n-----END PUBLIC KEY-----\n",
  "si": "0",
  "result": "succ",
  "reqid": "6ad2385a6ad23836000002da00c9"
}
```

### util.getSI

状态：已实测通过，耗时 2.0ms

```json
{
  "si": "0",
  "result": "succ",
  "reqid": "6ad2385a6ad23836000002da00ca"
}
```
