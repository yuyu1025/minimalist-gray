# gray-release

一个轻量、通用、与业务无关的 Kubernetes 蓝绿发布 CLI 工具。

> 当前状态：`v0.1` 脚手架已初始化，已具备 Deployment + Service 的基础蓝绿 YAML 生成能力，以及最小运行时命令骨架。

## 1. 背景

当前很多团队在 Kubernetes 上做蓝绿发布时，依赖人工手工改 YAML、改 selector、查 Pod 和日志：

- 发布标准不统一
- 回滚路径不一致
- 易出错，且难复用

`gray-release` 的目标是把这一过程工具化、标准化：

- 输入普通 Deployment + Service YAML
- 自动转换为蓝绿结构
- 提供基础运行时操作（状态、切流、回滚等）

## 2. 你要做什么（需求范围）

### 第一阶段（MVP）

支持资源：

- Deployment
- Service

支持命令：

- `gray-release init -f deployment.yml [-o out.yml]`
- `gray-release render -f deployment.yml [-o out.yml]`
- `gray-release apply -f out.yml`
- `gray-release status --name <app> --namespace <ns>`
- `gray-release switch --name <app> --namespace <ns> --to blue|green`
- `gray-release rollback --name <app> --namespace <ns>`
- `gray-release pods --name <app> --namespace <ns> [--color blue|green]`
- `gray-release exec --namespace <ns> --pod <pod> [-c <container>] [command]`
- `gray-release log --name <app> --namespace <ns> [--trace <traceId>]`

### 第二阶段（规划中）

ConfigMap 蓝绿策略：

- `shared`
- `copy`

## 3. 为什么这么做

- **统一发布标准**：统一标签与切流方式
- **降低接入成本**：基于现有 YAML 直接生成
- **降低人为错误**：避免手工改 selector/标签
- **提升运维能力**：状态、切流、回滚、日志、exec 命令统一
- **可扩展**：后续接 ConfigMap / diff / 校验等能力

## 4. 核心模型

- Blue / Green：两套并存 Deployment
- 稳定 Service：保持原服务名，通过 `selector.track` 指向 active color
- 预览 Service（可选）：`<name>-blue`、`<name>-green`
- Active Color：当前正式流量颜色

## 5. 生成规则（第一阶段）

输入：

- `Deployment/<name>`
- `Service/<name>`

输出：

- `Deployment/<name>-blue`
- `Deployment/<name>-green`
- `Service/<name>`（稳定入口）
- 可选 `Service/<name>-blue` / `Service/<name>-green`

规则：

- 两个 Deployment 增加 `track=blue|green`
- 稳定 Service 的 `selector.track` 指向 active color
- 默认 `blue replicas = 原副本数`，`green replicas = 0`

## 6. 目录结构

```text
gray_release/
  cli.py
  commands/
    init.py
    render.py
    apply.py
    status.py
    switch.py
    rollback.py
    pods.py
    exec.py
    log.py
  k8s/
    loader.py
    kubectl.py
  transform/
    deployment.py
    service.py
  io/
    yaml.py
  models.py
  config.py
```

## 7. 快速开始

### 安装依赖

```bash
pip install -e .
```

### 渲染蓝绿 YAML

```bash
gray-release render -f deployment.yml -o blue-green.yml
```

### 应用并切流

```bash
gray-release apply -f blue-green.yml
gray-release status --name app --namespace ns
gray-release switch --name app --namespace ns --to green
gray-release rollback --name app --namespace ns
```

## 8. 配置文件（可选）

文件名：`gray-release.yaml`

```yaml
apiVersion: gray-release/v1alpha1
kind: ReleaseConfig
metadata:
  name: demo-app
spec:
  namespace: demo-ns
  appName: demo-app
  activeColor: blue
  previewServices: true
```

## 9. 当前实现进度

已实现：

- ✅ CLI 主入口与子命令注册
- ✅ YAML 读取/写入（`ruamel.yaml`）
- ✅ Deployment 蓝绿转换
- ✅ Service 稳定/预览转换
- ✅ `render/init/apply/status/switch/rollback` 最小可运行实现
- ✅ `pods/exec/log` 基础命令封装

待完善（下一步）：

- Deployment readiness 校验后再切流
- `status` 输出更多字段（replicas/image/endpoints）
- `exec/log` 交互式选择
- traceId 检索范围与输出格式增强
- ConfigMap `shared/copy`

## 10. 里程碑

- `v0.1`：init/render/status/switch/rollback
- `v0.2`：pods/exec/log
- `v0.3`：ConfigMap shared/copy
- `v0.4`：diff/校验/模板化
