# Adaptive Task Routing — 사용자 가이드

[English](README.md) · [繁體中文](README.zh-TW.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md)

Adaptive Task Routing은 규모가 큰 작업을 현재 대화에서 계속할지, 다음 단계에 어떤 모델과 추론 강도가 적합한지 AI가 판단하도록 돕는 플러그인입니다. AI는 요청한 분석이나 계획을 먼저 제시하고, 그다음 명확히 구분된 영역에서 리소스 설정을 추천합니다.

## 설치

### Gemini CLI

```bash
gemini extensions install https://github.com/zyzdev/adaptive-task-routing-gemini --ref v0.4.2
```

설치 후 Gemini CLI를 다시 시작하세요.

### Claude Code

공개 디렉터리 신청은 심사 중입니다. 정식 등록 전에는 전용 저장소를 복제하고 플러그인 디렉터리를 지정해 Claude Code를 시작할 수 있습니다.

```bash
git clone --branch v0.4.2 https://github.com/zyzdev/adaptive-task-routing-claude.git
claude --plugin-dir "$PWD/adaptive-task-routing-claude"
```

### ChatGPT 및 Codex

[v0.4.2 Release](https://github.com/zyzdev/adaptive-task-routing/releases/tag/v0.4.2)에서 `adaptive-task-routing-openai-0.4.2.zip`을 다운로드하세요. 로컬 플러그인을 지원하는 화면에서는 압축을 푼 플러그인을 Plugin 또는 Marketplace 기능으로 추가합니다. 공개 디렉터리 제공 여부는 OpenAI 심사 결과에 따릅니다.

## 처음 사용하기

설치 후 새 대화를 열고 일정 규모 이상의 작업을 입력합니다. 예:

> 이 프로젝트의 릴리스 절차, 플랫폼 간 일관성, 테스트 누락을 점검해 주세요.

AI는 유용한 점검 결과나 실행 가능한 계획을 먼저 제시합니다. 다음 단계가 라우팅 대상이면 이어서 **Adaptive Task Routing** 리소스 추천이 표시됩니다.

- 현재 대화를 유지할지 여부
- 최소 충분 모델 및 추론 강도
- 권장 모델 및 추론 강도
- 필요한 경우 업그레이드 가치

기본 `ask` 모드에서는 추천 후 잠시 멈추고 자연스러운 사용자 응답을 기다립니다. 설정을 변경하거나, 현재 설정으로 계속하거나, 다른 방식을 요청할 수 있습니다. 정해진 답변 문구는 필요하지 않습니다.

## 명시적으로 실행하기

- Skill 멘션을 지원하는 Codex: `$adaptive-task-routing`
- Claude Code: `/adaptive-task-routing:adaptive-task-routing`
- 기타 화면: “이 작업을 시작하기 전에 adaptive-task-routing Skill을 사용해 주세요.”라고 요청합니다.

## 모드

- `ask`(기본값): 추천을 표시하고 대규모 실행 전에 사용자 응답을 기다립니다.
- `auto`: 현재 호스트가 허용하고 결과를 검증할 수 있는 변경만 적용한 뒤 계속합니다.
- `off`: 해당 Router를 건너뜁니다.

대화 라우팅과 모델 라우팅 모드는 각각 설정할 수 있습니다. 기본값을 바꾸려면 설치된 플러그인의 `shared/defaults.yaml`을 수정한 뒤 호스트를 다시 시작하세요.

## 제거

Gemini CLI:

```bash
gemini extensions uninstall adaptive-task-routing
```

Claude Code를 `--plugin-dir`로 시작했다면 세션을 종료하고 복제한 디렉터리를 삭제하면 됩니다. ChatGPT 또는 Codex에서는 설치할 때 사용한 Plugin 또는 Marketplace 화면에서 비활성화하거나 제거하세요.

## 문제 해결

- 설치 또는 업데이트 후 새 대화를 시작하세요.
- Skill 목록에 `adaptive-task-routing`, `task-context-router`, `research-model-router`가 있는지 확인하세요.
- 추천이 나타나지 않으면 Skill을 한 번 명시적으로 실행해 보세요.
- 추천이 표시되었다고 해서 모델이나 대화가 전환된 것은 아닙니다. 검증된 자동 변경만 적용 완료로 보고됩니다.

개발 및 검증에 관한 자세한 내용은 [프로젝트 README](../../README.md)를 참고하세요.
