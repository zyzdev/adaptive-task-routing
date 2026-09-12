# Adaptive Task Routing for Gemini CLI

[English](README.md) · [繁體中文](README.zh-TW.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md)

Adaptive Task Routing은 Gemini가 다음 주요 작업 단계에 적합한 대화 환경과 모델을 선택하도록 돕습니다. Gemini는 요청한 점검 결과나 계획을 먼저 제시한 뒤 리소스 설정을 추천합니다.

## 설치

```bash
gemini extensions install https://github.com/zyzdev/adaptive-task-routing-gemini --ref v0.4.2
```

설치 후 Gemini CLI를 다시 시작하고 `gemini extensions list`로 확인하세요.

## 처음 사용하기

새 세션에서 일정 규모 이상의 작업을 입력합니다. 예:

> 이 프로젝트의 릴리스 절차를 점검하고 주요 위험에 대한 구현 계획을 작성해 주세요.

명시적으로 실행하려면 Gemini에게 `adaptive-task-routing` Skill을 사용하라고 요청하세요.

## 대화에서 모드 변경하기

- “이 대화에서는 Adaptive Task Routing을 auto로 설정해 주세요.”
- “모델 라우팅을 ask로 설정해 주세요.”
- “이번 작업에서만 대화 라우팅을 off로 설정해 주세요.”
- “현재 두 라우팅 모드는 무엇인가요?”

Router를 지정하지 않은 변경은 두 라우터에 모두 적용됩니다. 기본값은 `ask`이고, `auto`는 Gemini가 실행하고 검증할 수 있는 변경만 적용하며, `off`는 지정한 Router를 건너뜁니다.

## 표시되는 내용

아래는 ‘Plugin의 릴리스 과정, 플랫폼 간 일관성 및 테스트 누락을 점검해 주세요’라는 요청의 예시입니다. 실제 계획과 권장 사항은 작업 및 플랫폼에 따라 달라집니다.

### 응답 예시

#### 1. AI 작업 계획

```text
1. 릴리스 스크립트와 Manifest를 확인한다.
2. CI와 테스트 누락을 확인한다.
3. 위험을 정리하고 수정 순서를 제안한다.
```

#### 2. Adaptive Task Routing 리소스 권장 사항

```text
---

### Adaptive Task Routing｜작업 리소스 추천

【대화 설정】
* 추천: 현재 대화 유지
* 창 전환: 아니요

【최소 충분 AI 설정】
* Model: Flash
* Reasoning: 모델 기본값

【권장 AI 설정】
* Model: Pro
* Reasoning: 모델 기본값
* 업그레이드 가치: 중간. 놓치기 쉬운 파일 간 의존성을 추적하는 데 유리합니다.

현재 환경에서는 모델을 대신 변경할 수 없습니다. 권장 모델을 사용하려면 /model에서 선택하세요. 변경할지 현재 설정을 사용할지 결정할 때까지 여기서 기다립니다.
```

모델 별칭은 예시이며 현재 Gemini 계정에 따라 해석됩니다. 세션에서 명확한 사고 설정을 제공할 때만 해당 값을 표시하고, 그렇지 않으면 모델 기본값을 사용합니다. `ask`는 여기서 멈추며 `auto`는 이미 승인된 작업을 계속할 수 있습니다.

## 제거

```bash
gemini extensions uninstall adaptive-task-routing
```

제거 후 Gemini CLI를 다시 시작하세요.

검증과 Gallery에 관한 내용은 [개발 정보](DEVELOPMENT.md)를 참고하세요. 공식 소스는 [메인 프로젝트](https://github.com/zyzdev/adaptive-task-routing)에 있습니다.
