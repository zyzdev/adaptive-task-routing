# ChatGPT 및 Codex용 Adaptive Task Routing

[English](README.md) · [繁體中文](README.zh-TW.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md)

Adaptive Task Routing은 ChatGPT와 Codex가 다음 주요 작업 단계에 적합한 대화 환경, 모델 및 추론 강도를 선택하도록 돕습니다. AI는 요청한 점검 결과나 계획을 먼저 제시한 뒤 리소스 설정을 추천합니다.

## 설치

공개 Plugin은 OpenAI Plugins portal에서 관리됩니다. 공개 전에는 [최신 릴리스](https://github.com/zyzdev/adaptive-task-routing/releases/tag/v0.4.2)에서 `adaptive-task-routing-openai-0.4.2.zip`을 다운로드하고 압축을 푼 뒤, 해당 디렉터리를 로컬 Plugin 소스 또는 Marketplace로 등록하세요.

Codex CLI에서는 설정된 Marketplace에서 설치할 수 있습니다. 공개된 후에는 ChatGPT와 Codex App의 Plugins Directory에서 선택할 수 있습니다.

## 처음 사용하기

새 대화를 시작하고 규모가 있는 작업을 입력합니다. 예:

> 이 프로젝트의 릴리스 흐름을 점검하고 주요 위험에 대한 구현 계획을 제안해 주세요.

이름이 있는 Skill을 지원하는 화면에서는 `$adaptive-task-routing`으로 명시적으로 활성화할 수 있습니다.

## 대화에서 모드 변경

- “이 대화에서는 Adaptive Task Routing을 auto로 설정해 주세요.”
- “모델 라우팅을 ask로 설정해 주세요.”
- “이 작업에서는 대화 라우팅을 꺼 주세요.”
- “현재 라우팅 모드는 무엇인가요?”

Router를 지정하지 않은 변경은 두 라우터에 모두 적용됩니다. 기본값은 `ask`입니다. `auto`는 현재 OpenAI 화면에서 실행하고 검증할 수 있는 변경만 적용하며, `off`는 지정한 Router를 건너뜁니다.

## 표시되는 내용

아래는 ‘Plugin의 릴리스 과정, 플랫폼 간 일관성 및 테스트 누락을 점검해 주세요’라는 요청의 예시입니다. 실제 계획과 권장 사항은 작업 및 플랫폼에 따라 달라집니다.

### 응답 예시

#### 1. AI 작업 계획

```text
1. 릴리스 스크립트와 Manifest를 확인한다.
2. CI와 테스트 누락을 확인한다.
```

#### 2. Adaptive Task Routing 리소스 권장 사항

```text
---

### Adaptive Task Routing｜작업 리소스 추천

【대화 설정】
* 추천: 현재 대화 유지
* 창 전환: 아니요

【최소 충분 AI 설정】
* Model: GPT-5.6 Sol
* Reasoning: high

【권장 AI 설정】
* Model: GPT-6 Astra
* Reasoning: high
* 업그레이드 가치: 중간. 놓치기 쉬운 파일 간 의존성을 추적하는 데 유리합니다.

현재 환경에서는 설정을 대신 변경할 수 없습니다. 필요한 경우 ChatGPT 또는 Codex App의 모델 및 추론 강도 선택 메뉴를 사용하고, Codex CLI에서는 `/model`을 사용하세요. 변경할지 현재 설정을 사용할지 결정할 때까지 여기서 기다립니다.
```

모델 이름과 강도는 예시입니다. 실제 추천은 현재 OpenAI 환경에서 확인된 선택지만 사용합니다. `ask`는 여기서 멈추며 `auto`는 이미 승인된 작업을 계속할 수 있습니다.

## 제거

Plugins Directory 또는 설정된 Codex Marketplace에서 제거할 수 있습니다. 직접 압축을 푼 로컬 버전은 Marketplace 등록을 해제한 뒤 해당 디렉터리를 삭제하세요.

패키징, 검증 및 공개에 관한 자세한 내용은 [개발 안내](DEVELOPMENT.md)를 참조하세요.
