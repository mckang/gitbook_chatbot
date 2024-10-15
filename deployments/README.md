### namespace 생성

```
kubectl apply -f namespace_socialbiz-chatbot.yaml
```

### ConfigMap 생성

```
configmap은 chromadb는 envFrom으로 넣고 be는 volume mount로 넣는다 (코드 내부에 env를 직접 가져다 쓰는 코드가 있기 때문)
- kubectl create -f configmap_socialbiz_chromadb.yaml
- kubectl create -f configmap_socialbiz_be.yaml
```

### service 생성

```
chromadb 서비스는 외부노출하지 않기 때문에 ClusterIP 서비스로 생성. be,fe 서버는 NodePort로 생성하여 외부통신 가능하게 조치
deployment의 경우 replica 설정 3 및 cpu, memory를 높여서 속도향상을 할 수 있게 조치
- kubectl apply -f service_socialbiz-chorma.yaml
- kubectl apply -f service_socialbiz-be.yaml
- kubectl apply -f service_socialbiz-fe.yaml
```

### ingress 설정

```
ingress는 외부 서비스가 필요한 2개의 서버만 작성
- kubectl apply -f ingress_socialbiz_be.yaml
- kubectl apply -f ingress_socialbiz_fe.yaml
```

### kubenetes 환경설정 확인 명령어

```
파드리스트: kubectl get pod -n socialbiz-gitbook-chatbot
세부파드확인: kubectl describe pod -n socialbiz-gitbook-chatbot [pod name]
로그확인: kubectl logs -n socialbiz-gitbook-chatbot [pod name]
```

### 문제점/조치중인 방향

```
서비스 배포완료
```
